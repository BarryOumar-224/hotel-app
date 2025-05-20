import streamlit as st
import sqlite3
from datetime import date
from PIL import Image

st.set_page_config(page_title="Gestion Hôtel", page_icon="🏨")

DB = "hotel.db"

def get_conn():
    return sqlite3.connect(DB)

# Page d'accueil
def page_accueil():
    col1, col2 = st.columns([1, 4])
    with col1:
        try:
            logo = Image.open("logo.png")
            st.image(logo, width=100)
        except:
            st.warning("Logo non trouvé.")
    with col2:
        st.markdown("##   **Bienvenue dans l'application de gestion hôtelière**")
    st.markdown("""
---
Gérez les :
- 👤 Clients
- 📅 Réservations
- 🛏️ Chambres disponibles
- 🎁 Prestations
- 📝 Évaluations

Naviguez avec le menu à gauche.
---
*Développé avec ❤️ en Python & Streamlit*
""")


def afficher_reservations():
    conn = get_conn()
    req = """
        SELECT R.id_Reservation AS "ID",
               C.nom_complet AS "Client",
               R.date_arrivee AS "Arrivée",
               R.date_depart AS "Départ",
               CASE WHEN E.id_Evaluation IS NOT NULL THEN '✅ Oui' ELSE '❌ Non' END AS "Évaluation faite"
        FROM Reservation R
        JOIN Client C ON R.id_Client = C.id_Client
        LEFT JOIN Evaluation E ON R.id_Reservation = E.id_Reservation
        ORDER BY R.id_Reservation ASC;
    """
    df = pd.read_sql_query(req, conn)
    conn.close()
    st.subheader("📅 Réservations + Évaluations")
    st.dataframe(df)




import pandas as pd  # Ajoute ça en haut de ton fichier

def afficher_clients():
    conn = get_conn()
    query = "SELECT id_Client, nom_complet, adresse, ville, code_postal, email, telephone FROM Client"
    df = pd.read_sql_query(query, conn)
    conn.close()
    st.subheader("👤 Clients")
    st.dataframe(df)  # Utilise st.dataframe pour scroll + tri

def chambres_disponibles(start, end):
    conn = sqlite3.connect("hotel.db")  # Ou le nom de ta base
    req = """
        SELECT 
            Chambre.id_Chambre AS "ID", 
            Chambre.numero AS "Numéro", 
            Chambre.etage AS "Étage", 
            TypeChambre.tarif AS "Prix (€)"
        FROM Chambre 
        JOIN TypeChambre ON Chambre.id_Type = TypeChambre.id_Type
        WHERE Chambre.id_Chambre NOT IN (
            SELECT RC.id_Chambre
            FROM ReservationChambre RC
            JOIN Reservation R ON RC.id_Reservation = R.id_Reservation
            WHERE NOT (R.date_depart < ? OR R.date_arrivee > ?)
        );
    """
    df = pd.read_sql_query(req, conn, params=(start, end))
    conn.close()
    
    # Affichage ou traitement
    st.write("### Chambres disponibles")
    st.dataframe(df)



def afficher_prestations():
    conn = sqlite3.connect("hotel.db")
    req = """
        SELECT id_Prestation AS "ID", description AS "Description", prix AS "Prix (€)"
        FROM Prestation;
    """
    df = pd.read_sql_query(req, conn)
    conn.close()

    st.write("### Liste des prestations disponibles")
    st.dataframe(df)



def afficher_evaluations():
    conn = get_conn()
    req = """
        SELECT E.date AS "Date",
               E.note AS "Note",
               E.commentaire AS "Commentaire",
               C.nom_complet AS "Client"
        FROM Evaluation E
        JOIN Reservation R ON R.id_Reservation = E.id_Reservation
        JOIN Client C ON C.id_Client = R.id_Client
        ORDER BY E.date DESC;
    """
    df = pd.read_sql_query(req, conn)
    conn.close()
    st.subheader("📝 Évaluations")
    st.dataframe(df)

def nouvelle_reservation():
    st.subheader("📌 Nouvelle réservation (client + chambre)")
    st.markdown("### 👤 Informations du client")
    nom = st.text_input("Nom complet")
    adresse = st.text_input("Adresse")
    ville = st.text_input("Ville")
    cp = st.number_input("Code postal", step=1)
    email = st.text_input("Email")
    tel = st.text_input("Téléphone")

    st.markdown("### 🗓️ Dates")
    d1 = st.date_input("Date d'arrivée", value=date.today())
    d2 = st.date_input("Date de départ", value=date.today())

    st.markdown("### 🛏️ Choix de la chambre")
    conn = get_conn()
    chambre_req = """
        SELECT id_Chambre, numero, etage FROM Chambre
        WHERE id_Chambre NOT IN (
            SELECT RC.id_Chambre FROM ReservationChambre RC
            JOIN Reservation R ON RC.id_Reservation = R.id_Reservation
            WHERE NOT (R.date_depart < ? OR R.date_arrivee > ?)
        );
    """
    chambres = conn.execute(chambre_req, (str(d1), str(d2))).fetchall()
    conn.close()

    if not chambres:
        st.warning("Aucune chambre disponible pour cette période.")
        return

    choix = {f"N°{c[1]} - Étage {c[2]}": c[0] for c in chambres}
    chambre_selection = st.selectbox("Choisir une chambre", list(choix.keys()))

    if st.button("Valider la réservation ✅"):
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Client (nom_complet, adresse, ville, code_postal, email, telephone)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (nom, adresse, ville, cp, email, tel))
        client_id = cursor.lastrowid

        cursor.execute("""
            INSERT INTO Reservation (date_arrivee, date_depart, id_Client)
            VALUES (?, ?, ?)
        """, (str(d1), str(d2), client_id))
        reservation_id = cursor.lastrowid

        chambre_id = choix[chambre_selection]
        cursor.execute("""
            INSERT INTO ReservationChambre (id_Reservation, id_Chambre)
            VALUES (?, ?)
        """, (reservation_id, chambre_id))

        conn.commit()
        conn.close()
        st.success(f"✅ Réservation confirmée pour {nom}, chambre {chambre_selection}")

# Menu principal
menu = st.sidebar.selectbox("📋 Menu", [
    "🏠 Accueil",
    "📅 Réservations",
    "👤 Clients",
    "🛏️ Disponibilité des chambres",
    "🎁 Prestations",
    "📝 Évaluations",
    "📌 Nouvelle réservation"
])

if menu == "🏠 Accueil":
    page_accueil()
elif menu == "📅 Réservations":
    afficher_reservations()
elif menu == "👤 Clients":
    afficher_clients()
elif menu == "🛏️ Disponibilité des chambres":
    debut = st.date_input("Date d'arrivée")
    fin = st.date_input("Date de départ")
    if debut <= fin:
        chambres_disponibles(str(debut), str(fin))
    else:
        st.error("⛔ Erreur de dates.")
elif menu == "🎁 Prestations":
    afficher_prestations()
elif menu == "📝 Évaluations":
    afficher_evaluations()
elif menu == "📌 Nouvelle réservation":
    nouvelle_reservation()
