from flask import session
from backend import db, login_manager
#from Petservice import bcrypt
from flask_login import UserMixin


@login_manager.user_loader 
def load_user(user_id):
    if 'type' in session:
        if session['type'] == 'Owner':
            return db.session.get(Owner, int(user_id))
        elif session['type'] == 'Sitter':
            return db.session.get(Petsitter, int(user_id))
    return None


#Pet
class Pet(db.Model, UserMixin):
    petID = db.Column(db.Integer(), primary_key=True)
    PetType= db.Column(db.String(length=50), nullable=False)
    PetName = db.Column(db.String(length=60), nullable=False)
    PetSize= db.Column(db.String(length=60), nullable=False)
    PetAge = db.Column(db.Integer(), nullable=False)
    VaccinationStatus= db.Column(db.Integer(), nullable=False)
    Habits = db.Column(db.String(length=20), nullable=False)
    SpecialNeed = db.Column(db.String(length=20), nullable=False)
    # pet:fk -> owner:pk
    ownerID = db.Column(db.Integer(), db.ForeignKey('owner.OwnerID')) #class model lower case!
    # relationship with reservations
    pet_reservation = db.relationship("Reservation", backref="pet_reservation", lazy=True)

class Owner(db.Model, UserMixin):
    OwnerID = db.Column(db.Integer(), primary_key=True)
    OwnerName = db.Column(db.String(length=60), nullable=False)
    OwnerAddress = db.Column(db.String(length=100), nullable=False)
    OwnerPhoneNumber = db.Column(db.Integer(), nullable=False)
    OwnerEmail = db.Column(db.String(length=60), nullable=False)
    OwnerPassword = db.Column(db.String(length=60), nullable=False)
    # relationship with pets
    pet = db.relationship("Pet", backref="owner", lazy=True) #for : foreign key query !!!
    # relationship with reservations
    owner_reservation = db.relationship("Reservation", backref="owner_reservation", lazy=True)
    # relationship with review_sitter
    sitter_reviews = db.relationship("Review_sitter", backref="sitter_reviews", lazy=True)
    # relationship with review_owner
    owner_reviews = db.relationship("Review_owner", backref="owner_reviews", lazy=True)
    def get_id(self):
        return str(self.OwnerID) 
        
    @property
    def password(self):
        return self.OwnerPassword
    
    def check_password_correction(self, attempted_ownerpassword):
        if attempted_ownerpassword == self.OwnerPassword:
            return True






class Petsitter(db.Model, UserMixin):
    SitterID = db.Column(db.Integer(), primary_key=True)
    SitterName = db.Column(db.String(length=60), nullable=False)
    SitterPassword = db.Column(db.String(length=60), nullable=False)
    SitterPhoneNumber = db.Column(db.Integer(), nullable=False)
    SitterLineID = db.Column(db.String(length=60), nullable=False)
    SitterEmail = db.Column(db.String(length=60), nullable=False)
    SitterAddress = db.Column(db.String(length=100), nullable=False)
    SitterAccPet = db.Column(db.String(length=50), nullable=False)
    SitterServiceType = db.Column(db.String(length=50), nullable=False)
    SitterSpace = db.Column(db.Integer(), nullable=False)
    SitterPetCareExp = db.Column(db.String(length=60), nullable=False)
    SitterVetExp = db.Column(db.String(length=60), nullable=False)
    PetFeeder = db.Column(db.String(length=60), nullable=False)
    CatTree = db.Column(db.String(length=60), nullable=False)
    PetBed = db.Column(db.String(length=60), nullable=False)
    Toy = db.Column(db.String(length=60), nullable=False)
    SecurityCamera = db.Column(db.String(length=60), nullable=False)
    # relationship with reservations
    sitter_reservation = db.relationship("Reservation", backref="sitter_reservation", lazy=True)
    # relationship with Review_sitter
    sitter_reviews = db.relationship("Review_sitter", backref="sitterreviews", lazy=True)
    # relationship with Review_owner
    owner_reviews = db.relationship("Review_owner", backref="ownerreviews", lazy=True)
    def get_id(self):
        return str(self.SitterID)
    
    @property
    def password(self):
        return self.SitterPassword
    
    def check_password_correction(self, attempted_sitterpassword):
        if attempted_sitterpassword == self.SitterPassword:
            return True    
        
# Review
class Review_sitter(db.Model, UserMixin):
    reviewid = db.Column(db.Integer(), primary_key=True)
    sitterrating = db.Column(db.Integer(), nullable=False)
    sittercomment = db.Column(db.String(length=255), nullable=False)
    # Review: fk -> owner/sitter/reservation :pk
    ownerid = db.Column(db.Integer(), db.ForeignKey('owner.OwnerID'), nullable=False)
    sitterid = db.Column(db.Integer(), db.ForeignKey('petsitter.SitterID'), nullable=False)
    reservationid = db.Column(db.Integer(), db.ForeignKey('reservation.reservationid'), nullable=False)

class Review_owner(db.Model, UserMixin):
    reviewid = db.Column(db.Integer(), primary_key=True)
    ownerrating = db.Column(db.Integer(), nullable=False)
    ownercomment = db.Column(db.String(length=255), nullable=False)
    # Review: fk -> owner/sitter/reservation :pk
    ownerid = db.Column(db.Integer(), db.ForeignKey('owner.OwnerID'), nullable=False)
    sitterid = db.Column(db.Integer(), db.ForeignKey('petsitter.SitterID'), nullable=False)
    reservationid = db.Column(db.Integer(), db.ForeignKey('reservation.reservationid'), nullable=False)

class Walk(db.Model, UserMixin):
    walkid = db.Column(db.Integer(), primary_key=True)
    startdate = db.Column(db.Date(), nullable=False)
    duration = db.Column(db.Integer(), nullable=False)
    frequency = db.Column(db.Integer(), nullable=False)
    # walk:fk -> reservation:pk
    reservationid = db.Column(db.Integer(), db.ForeignKey('reservation.reservationid'))
  
class Fostercare(db.Model, UserMixin):
    fostercareid = db.Column(db.Integer(), primary_key=True)
    startdate = db.Column(db.Date(), nullable=False)
    enddate = db.Column(db.Date(), nullable=False)
    # Fostercare:fk -> reservation:pk
    reservationid = db.Column(db.Integer(), db.ForeignKey('reservation.reservationid'))
    
class Reservation(db.Model, UserMixin):
    reservationid = db.Column(db.Integer(), primary_key=True)
    # Reservation:fk -> all:pk
    petID = db.Column(db.Integer(), db.ForeignKey('pet.petID'), nullable=False)
    ownerID = db.Column(db.Integer(), db.ForeignKey('owner.OwnerID'), nullable=False)
    sitterID = db.Column(db.Integer(), db.ForeignKey('petsitter.SitterID'), nullable=False)
    reservationtype = db.Column(db.String(length=255), nullable=False)
    # relatinship with Walk & Fostercare & review
    walk = db.relationship("Walk", backref="walk", lazy=True)
    fostercare = db.relationship("Fostercare", backref="fostercare", lazy=True)
    # relationship with Review_owner
    owner_reviews = db.relationship("Review_owner", backref="reviews_owner", lazy=True)
    # relationship with Review_sitter
    sitter_reviews = db.relationship("Review_sitter", backref="reviews_sitter", lazy=True)