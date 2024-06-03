-- 創建資料表並定義架構
CREATE TABLE IF NOT EXISTS Owner (
    OwnerID INTEGER PRIMARY KEY AUTOINCREMENT,
    OwnerName TEXT,
    OwnerPassword TEXT,
    OwnerPhoneNumber TEXT,
    OwnerEmail TEXT,
    OwnerAddress TEXT
);

CREATE TABLE IF NOT EXISTS Pet (
    PetID INTEGER PRIMARY KEY AUTOINCREMENT,
    OwnerID INTEGER,
    PetType TEXT,
    PetName TEXT,
    PetSize TEXT,
    PetBreed TEXT,
    PetAge INTEGER,
    VaccinationStatus TEXT,
    MedicalRecord TEXT,
    Habits TEXT,
    SpecialNeed TEXT,
    FOREIGN KEY (OwnerID) REFERENCES Owner(OwnerID)
);

CREATE TABLE IF NOT EXISTS PetSitter (
    SitterID INTEGER PRIMARY KEY AUTOINCREMENT,
    SitterGender TEXT,
    SitterLineID TEXT,
    SitterName TEXT,
    SitterResidence TEXT,
    SitterRating REAL,
    ExperienceInPetCare INTEGER,
    ExperienceInVeterinaryWork INTEGER,
    ExperienceYears INTEGER,
    AcceptedPetTypes TEXT,
    ServiceTypes TEXT,
    FacilitiesProvided TEXT,
    PetSpaceSize INTEGER
);

CREATE TABLE IF NOT EXISTS Reservation (
    ReservationID INTEGER PRIMARY KEY AUTOINCREMENT,
    ReviewID INTEGER,
    PetID INTEGER,
    SitterID INTEGER,
    ReservationType TEXT,
    FOREIGN KEY (PetID) REFERENCES Pet(PetID),
    FOREIGN KEY (SitterID) REFERENCES PetSitter(SitterID)
);

CREATE TABLE IF NOT EXISTS Review (
    ReviewID INTEGER PRIMARY KEY AUTOINCREMENT,
    ReservationID INTEGER,
    SitterID INTEGER,
    OwnerID INTEGER,
    SitterRating REAL,
    OwnerRating REAL,
    OwnerComment TEXT,
    SitterComment TEXT,
    FOREIGN KEY (ReservationID) REFERENCES Reservation(ReservationID),
    FOREIGN KEY (SitterID) REFERENCES PetSitter(SitterID),
    FOREIGN KEY (OwnerID) REFERENCES Owner(OwnerID)
);

CREATE TABLE IF NOT EXISTS Fostercare (
    FostercareID INTEGER PRIMARY KEY AUTOINCREMENT,
    ReservationID INTEGER,
    StartDate DATE,
    EndDate DATE,
    FOREIGN KEY (ReservationID) REFERENCES Reservation(ReservationID)
);

CREATE TABLE IF NOT EXISTS Walk (
    WalkID INTEGER PRIMARY KEY AUTOINCREMENT,
    ReservationID INTEGER,
    Frequency TEXT,
    Duration INTEGER,
    FOREIGN KEY (ReservationID) REFERENCES Reservation(ReservationID)
);
