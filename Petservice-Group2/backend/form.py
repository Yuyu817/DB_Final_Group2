from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, HiddenField, DateTimeField, IntegerField
from wtforms.validators import DataRequired
from backend.models import Pet, Owner, Petsitter, Review_sitter, Review_owner, Walk, Fostercare, Reservation

#OwnerRegister
class RegisterForm_owner(FlaskForm):
    ownerusername = StringField(label='User Name:')
    owneremail_address = StringField(label='Email Address:')
    ownerpassword = PasswordField(label='Password:')
    ownerphonenumber = StringField(label='phonenumber:')
    owneraddress = StringField(label='address:')
    submit = SubmitField(label='Create Account')

#PetRegister
class RegisterForm_pet(FlaskForm):
    petusername = StringField(label='User Name:')
    pettype = StringField(label='Type:')
    petsize = StringField(label='Size:')
    petage = StringField(label='Age:')
    pethabit = StringField(label='Habit:')
    petvacinnationstatus = StringField(label='VacinnationStatus:')
    petspecialneed = StringField(label='Specialneed :')


#SitterRegister
class RegisterForm_petsitter(FlaskForm):
    
    sitterusername =  StringField(label='username:')
    sitterpassword = PasswordField(label='password:')
    sitterphonenumber =  StringField(label='phonenumber:')
    sitteraddress =  StringField(label='address:')
    sitterlineid =  StringField(label='lineid:')
    sitteremail=  StringField(label='email:')
    SitterPetCareExp =  StringField(label='SitterPetCareExperience :')
    SitterVetExp =  StringField(label='SitterVetExp:')
    sitterAcceptedPetTypes =  StringField(label='AcceptedPetTypes:')
    sitterServiceTypes =  StringField(label='ServiceTypes:')
    sitterPetSpaceSize =  StringField(label='PetSpaceSize:')
    PetFeeder = StringField(label='PetFeeder:')
    CatTree = StringField(label='CatTree:')
    PetBed = StringField(label='PetBed:')
    Toy  = StringField(label='Toy:')
    SecurityCamera = StringField(label=' SecurityCamera:')
    submit = SubmitField(label='Create Account')

#OwnerLogin
class owner_LoginForm(FlaskForm):
    ownerusername = StringField(label='User Name:', validators=[DataRequired()])
    ownerpassword = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Sign in')
    
#SitterLogin
class sitter_LoginForm(FlaskForm):
    sitterusername = StringField(label='User Name:', validators=[DataRequired()])
    sitterpassword = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Sign in')

class editForm_owner(FlaskForm):
    ownerusername= StringField(label='user:')
    owneremail_address = StringField(label='Email Address:')
    ownerpassword = StringField(label='Password:')
    ownerphonenumber = StringField(label='phonenumber:')
    owneraddress = StringField(label='address:')
    #submit = SubmitField(label='Update') #

class editForm_pet(FlaskForm):
    pettype= StringField(label='PetType:')
    petname = StringField(label=' PetName:')
    petsize= StringField(label=' PetSize:')
    petage = StringField(label='PetAge :')
    vaccinationstatus= StringField(label='VaccinationStatus:')
    habits = StringField(label='Habits :')
    specialneed = StringField(label='SpecialNeed:')
    #submit = SubmitField(label='Update')#

class editForm_sitter(FlaskForm):

   sitterusername =  StringField(label='username:')
   sitterlineid =  StringField(label='lineid:')
   sitterpassword = StringField(label='password:')
   sitterphonenumber =  StringField(label='phonenumber:')
   sitteraddress =  StringField(label='address:')
   sitteremail=  StringField(label='email:')
   sitterExperienceInVet =  StringField(label='ExperienceInVet :')
   sitterExperienceInPetCare =  StringField(label='ExperienceInPetCare:')
   sitterAcceptedPetTypes =  StringField(label='AcceptedPetTypes:')
   sitterServiceTypes =  StringField(label='ServiceTypes:')
   sitterPetSpaceSize =  StringField(label='PetSpaceSize:')
   sitterPetFeeder= StringField(label='PetFeeder:')
   sitterCatTree = StringField(label='CatTree:')
   sitterPetBed = StringField(label='PetBed:')
   sitterToy = StringField(label='Toy:')
   sitterSecurityCamera = StringField(label='SecurityCamera:')
   #submit = SubmitField(label='Update')


class commentForm_owner(FlaskForm):
    sitterrating = IntegerField(label='Sitter Rating', validators=[DataRequired()])
    sittercomment = StringField(label='Sitter Comment', validators=[DataRequired()])
    # 隐藏字段用于表示預約的 ID
    reservationid=  HiddenField(validators=[DataRequired()])
    submit = SubmitField(label='Submit Review')

class commentForm_sitter(FlaskForm):
    ownerrating = IntegerField(label='Owner Rating', validators=[DataRequired()])
    ownercomment = StringField(label='Owner Comment', validators=[DataRequired()])
    # 隐藏字段用于表示預約的 ID
    reservationid=  HiddenField(validators=[DataRequired()])
    submit = SubmitField(label='Submit Review')



#OwnerReservationWalkForm(決定要預約散步)
class OwnerReservationWalkForm(FlaskForm):
    startdate = DateTimeField(label='StartDate(YYYY-MM-DD)', format='%Y-%m-%d')
    frequency = StringField(label='Frequency')
    duration = StringField(label='Duration')
    submit = SubmitField(label='Confirm Walk Reservation')

#OwnerReservationFosterForm(決定要預約寄養)
class OwnerReservationFosterForm(FlaskForm):
    startdate = DateTimeField(label='StartDate(YYYY-MM-DD)', format='%Y-%m-%d')
    enddate = DateTimeField(label='EndDate(YYYY-MM-DD)', format='%Y-%m-%d')
    submit = SubmitField(label='Confirm Foster Reservation')

