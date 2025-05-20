import sqlite3

def create_database():
    conn = sqlite3.connect("hotel.db")
    cursor = conn.cursor()

    # === Tables principales ===

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Hotel (
        id_Hotel INTEGER PRIMARY KEY AUTOINCREMENT,
        ville TEXT NOT NULL,
        pays TEXT NOT NULL,
        code_postal INTEGER
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Client (
        id_Client INTEGER PRIMARY KEY AUTOINCREMENT,
        nom_complet TEXT NOT NULL,
        adresse TEXT,
        ville TEXT,
        code_postal INTEGER,
        email TEXT,
        telephone TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Prestation (
        id_Prestation INTEGER PRIMARY KEY AUTOINCREMENT,
        prix REAL,
        description TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS TypeChambre (
        id_Type INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT,
        tarif REAL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Chambre (
        id_Chambre INTEGER PRIMARY KEY AUTOINCREMENT,
        numero INTEGER,
        etage INTEGER,
        fumeur BOOLEAN,
        id_Hotel INTEGER,
        id_Type INTEGER,
        FOREIGN KEY (id_Hotel) REFERENCES Hotel(id_Hotel),
        FOREIGN KEY (id_Type) REFERENCES TypeChambre(id_Type)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Reservation (
        id_Reservation INTEGER PRIMARY KEY AUTOINCREMENT,
        date_arrivee DATE,
        date_depart DATE,
        id_Client INTEGER,
        FOREIGN KEY (id_Client) REFERENCES Client(id_Client)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ReservationChambre (
        id_Reservation INTEGER,
        id_Chambre INTEGER,
        PRIMARY KEY (id_Reservation, id_Chambre),
        FOREIGN KEY (id_Reservation) REFERENCES Reservation(id_Reservation),
        FOREIGN KEY (id_Chambre) REFERENCES Chambre(id_Chambre)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Evaluation (
        id_Evaluation INTEGER PRIMARY KEY AUTOINCREMENT,
        date DATE,
        note INTEGER,
        commentaire TEXT,
        id_Reservation INTEGER,
        FOREIGN KEY (id_Reservation) REFERENCES Reservation(id_Reservation)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Offre (
        id_Hotel INTEGER,
        id_Prestation INTEGER,
        PRIMARY KEY (id_Hotel, id_Prestation),
        FOREIGN KEY (id_Hotel) REFERENCES Hotel(id_Hotel),
        FOREIGN KEY (id_Prestation) REFERENCES Prestation(id_Prestation)
    );
    """)

    # === Données d'exemple ===

    cursor.executemany("INSERT INTO Hotel (ville, pays, code_postal) VALUES (?, ?, ?);", [
        ('Paris', 'France', 75001),
        ('Lyon', 'France', 69002)
    ])

    cursor.executemany("INSERT INTO Client (nom_complet, adresse, ville, code_postal, email, telephone) VALUES (?, ?, ?, ?, ?, ?);", [
        ('Jean Dupont', '12 Rue de Paris', 'Paris', 75001, 'jean.dupont@email.fr', '0612345678'),
        ('Marie Leroy', '5 Avenue Victor Hugo', 'Lyon', 69002, 'marie.leroy@email.fr', '0623456789'),
        ('Paul Moreau', '8 Boulevard Saint-Michel', 'Marseille', 13005, 'paul.moreau@email.fr', '0634567890'),
        ('Lucie Martin', '27 Rue Nationale', 'Lille', 59800, 'lucie.martin@email.fr', '0645678901'),
        ('Emma Giraud', '3 Rue des Fleurs', 'Nice', 6000, 'emma.giraud@email.fr', '0656789012')
    ])

    cursor.executemany("INSERT INTO Prestation (prix, description) VALUES (?, ?);", [
        (15, 'Petit-déjeuner'),
        (30, 'Navette aéroport'),
        (0, 'Wi-Fi gratuit'),
        (50, 'Spa et bien-être'),
        (20, 'Parking sécurisé')
    ])

    cursor.executemany("INSERT INTO TypeChambre (type, tarif) VALUES (?, ?);", [
        ('Simple fumeur', 100),
        ('Double fumeur', 120),
        ('Simple non-fumeur', 90),
        ('Double non-fumeur', 110)
        
    ])

    cursor.executemany("INSERT INTO Chambre (numero, etage, fumeur, id_Hotel, id_Type) VALUES (?, ?, ?, ?, ?);", [
        (201, 2, 0, 1, 1),
        (502, 5, 1, 1, 2),
        (305, 3, 0, 2, 1),
        (410, 4, 0, 2, 2),
        (104, 1, 1, 2, 2),
        (202, 2, 0, 1, 1),
        (307, 3, 1, 1, 2),
        (101, 1, 0, 1, 1)
    ])

    cursor.executemany("INSERT INTO Reservation (date_arrivee, date_depart, id_Client) VALUES (?, ?, ?);", [
        ('2025-06-15', '2025-06-18', 1),
        ('2025-07-01', '2025-07-05', 2),
        ('2025-08-10', '2025-08-14', 3),
        ('2025-09-05', '2025-09-07', 4),
        ('2025-09-20', '2025-09-25', 5)
    ])

    cursor.executemany("INSERT INTO Evaluation (date, note, commentaire, id_Reservation) VALUES (?, ?, ?, ?);", [
        ('2025-06-15', 5, 'Excellent séjour, personnel très accueillant.', 1),
        ('2025-07-01', 4, 'Chambre propre, bon rapport qualité/prix.', 2),
        ('2025-08-10', 3, 'Séjour correct mais bruyant la nuit.', 3),
        ('2025-09-05', 5, 'Service impeccable, je recommande.', 4),
        ('2025-09-20', 4, 'Très bon petit-déjeuner, hôtel bien situé.', 5)
    ])

    conn.commit()
    conn.close()
    print("✅ Base SQLite créée et remplie avec succès selon le MLD.")

if __name__ == "__main__":
    create_database()
