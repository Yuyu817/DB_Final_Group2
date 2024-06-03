from backend import app
from flask import render_template, redirect, url_for, flash, request, session
from backend.models import Pet, Owner, Petsitter, Review_sitter, Review_owner, Walk, Fostercare, Reservation
from backend.form import RegisterForm_owner, RegisterForm_pet, RegisterForm_petsitter, owner_LoginForm, sitter_LoginForm, OwnerReservationWalkForm, OwnerReservationFosterForm,editForm_owner,editForm_pet, editForm_sitter,commentForm_owner,commentForm_sitter
from backend import db
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy.orm import aliased
from sqlalchemy import func


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('Home.html')

#owner or petsitter
@app.route('/login_mode', methods=['GET', 'POST'])
def login_mode():      ###更改前端的網頁url即可
    return render_template('login-mode.html')
    
#owner/pet register
@app.route('/owner_register', methods=['GET', 'POST'])
def owner_register_page():

    form1 = RegisterForm_pet() 
    form2 = RegisterForm_owner()
    if form2.validate_on_submit():
        user_to_create2 = Owner(OwnerName=form2.ownerusername.data,
                              OwnerEmail=form2.owneremail_address.data,
                              OwnerPassword=form2.ownerpassword.data,
                              OwnerPhoneNumber=form2.ownerphonenumber.data,
                              OwnerAddress=form2.owneraddress.data
                              )
    
        db.session.add(user_to_create2)
        db.session.commit()
    
        user_to_create1 = Pet(PetName=form1.petusername.data,
                              PetType=form1.pettype.data,
                              PetSize=form1.petsize.data,
                              PetAge=form1.petage.data,
                              Habits=form1.pethabit.data,
                              VaccinationStatus=form1.petvacinnationstatus.data,
                              SpecialNeed=form1.petspecialneed.data,
                              ownerID=user_to_create2.OwnerID
                              )   
        db.session.add(user_to_create1)   
        db.session.commit()
        


        login_user(user_to_create2)
        session['type'] = 'Owner'
        return redirect(url_for('owner_login_page')) ####註冊後到哪
    
    return render_template('OwnerSignUp.html', form2=form2, form1 = form1)


#sitter
@app.route('/sitter_register', methods=['GET', 'POST'])
def sitter_register_page():
    form = RegisterForm_petsitter()
    if form.validate_on_submit():
        user_to_create = Petsitter(SitterName=form.sitterusername.data,
                              SitterEmail=form.sitteremail.data,
                              SitterPassword=form.sitterpassword.data,
                              SitterPhoneNumber=form.sitterphonenumber.data,
                              SitterAddress=form.sitteraddress.data,
                              SitterLineID=form.sitterlineid.data,
                              SitterPetCareExp=form.SitterPetCareExp.data,
                              SitterVetExp=form.SitterVetExp.data,
                              SitterAccPet=form.sitterAcceptedPetTypes.data,
                              SitterServiceType=form.sitterServiceTypes.data,
                              SitterSpace=form.sitterPetSpaceSize.data,
                              PetFeeder=form.PetFeeder.data,
                              CatTree=form.CatTree.data,
                              PetBed=form.PetBed.data,
                              Toy=form.Toy.data,
                              SecurityCamera=form.SecurityCamera.data)
        
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        session['type'] = 'Sitter'
        #flash(f"Account created successfully! You are now logged in as {user_to_create.sitterusername}", category='success')
        return redirect(url_for('sitter_login_page')) ####

    return render_template('SitterSignUp.html', form=form)



#OwnerLogin
@app.route('/owner_login', methods=['GET', 'POST'])
def owner_login_page():
    form = owner_LoginForm()
    if form.validate_on_submit():
        attempted_user = Owner.query.filter_by(OwnerName=form.ownerusername.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_ownerpassword = form.ownerpassword.data
        ):  
            
            login_user(attempted_user)
            #session.permanent = True
            session['type'] = 'Owner'
            #flash(f'Success! You are logged in as: {attempted_user.ownerusername}', category='success')
            return redirect(url_for('babyowner'))  ###登入成功連的網頁(之後要改)
        #else:
           #flash('Username and password are not match! Please try again', category='danger')

    return render_template('Login-Owner.html', form=form)

#SitterLogin
@app.route('/sitter_login', methods=['GET', 'POST'])
def sitter_login_page():
    form = sitter_LoginForm()
    if form.validate_on_submit():
        attempted_user =Petsitter.query.filter_by(SitterName=form.sitterusername.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_sitterpassword=form.sitterpassword.data):

            login_user(attempted_user)
            #session.permanent = True
            session['type'] = "Sitter"
            #flash(f'Success! You are logged in as: {attempted_user.sitterusername}', category='success')
            return redirect(url_for('babysitter')) ###登入成功連的網頁(之後要改)
        #else:
           #flash('Username and password are not match! Please try again', category='danger')

    return render_template('Login-sitter.html', form=form)

@app.route('/babysitter', methods=['GET'])
def babysitter():
    if current_user.is_authenticated:
        actual_user = current_user._get_current_object()
        if isinstance(actual_user, Petsitter):
            SitterID = actual_user.SitterID  # Get the SitterID from the current user
            Reservations = Reservation.query.filter_by(sitterID=SitterID).all()
            reservation_data = []

            for reservation in Reservations:
                petID = reservation.petID
                ownerID = reservation.ownerID
                pet = Pet.query.filter_by(petID=petID).first()
                owner = Owner.query.filter_by(OwnerID=ownerID).first()
                reservation_data.append({
                    'reservation': reservation,
                    'pet': pet,
                    'owner': owner
                })       
        else:
            return redirect(url_for('sitter_login_page'))
    else:
        return redirect(url_for('sitter_login_page'))
    
    return render_template('BabySitter.html', reservations=reservation_data)

# 路由用於編輯登入者資料
@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    # 如果是 Owner，顯示 owner 和 pet 表單
    actual_user = current_user._get_current_object()
    if isinstance(actual_user, Owner):
        owner_form = editForm_owner()
        pet_form = editForm_pet()
        sitter_form = None
        # 在 GET 請求中填充 owner 表單字段
        if request.method == 'GET':
            owner_form.ownerusername.data = actual_user.OwnerName
            owner_form.ownerpassword.data = actual_user.OwnerPassword 
            owner_form.owneremail_address.data = actual_user.OwnerEmail
            owner_form.ownerphonenumber.data = actual_user.OwnerPhoneNumber
            owner_form.owneraddress.data = actual_user.OwnerAddress
           
            pet = Pet.query.filter_by(ownerID=actual_user.OwnerID ).first()
            if pet:
                pet_form.pettype.data = pet.PetType
                pet_form.petname .data = pet.PetName
                pet_form.petsize.data = pet.PetSize
                pet_form.petage.data = pet.PetAge
                pet_form.vaccinationstatus.data = pet.VaccinationStatus
                pet_form.habits.data = pet.Habits
                pet_form.specialneed.data = pet.SpecialNeed
    # 處理表單提交
        if request.method == 'POST':
            # 處理 owner 表單提交
                actual_user.OwnerName = owner_form.ownerusername.data
                actual_user.OwnerPassword =owner_form.ownerpassword.data
                actual_user.OwnerEmail= owner_form.owneremail_address.data
                actual_user.OwnerPhoneNumber = owner_form.ownerphonenumber.data
                actual_user.OwnerAddress = owner_form.owneraddress.data
                pet = Pet.query.filter_by(ownerID=actual_user.OwnerID).first()
                if pet:
                    pet.PetType = pet_form.pettype.data
                    pet.PetName = pet_form.petname.data
                    pet.PetSize = pet_form.petsize.data
                    pet.PetAge = pet_form.petage .data
                    pet.VaccinationStatus = pet_form.vaccinationstatus .data
                    pet.Habits = pet_form.habits.data
                    pet.SpecialNeed = pet_form.specialneed .data
                    db.session.commit()
                    flash('Your pet information has been updated successfully.', 'success')
                    return redirect(url_for('babyowner'))##回到編輯者頁面
                else:
                    flash('No pet information found for the current user.', 'warning')
    # 如果是 Sitter，只顯示 sitter 表單
    elif isinstance(actual_user,Petsitter ):
        owner_form = None
        pet_form = None
        sitter_form = editForm_sitter()
        # 在 GET 請求中填充 sitter 表單字段
        if request.method == 'GET':
            sitter_form.sitterusername.data = actual_user.SitterName
            sitter_form.sitterlineid.data = actual_user.SitterLineID
            sitter_form.sitterpassword.data= actual_user.SitterPassword
            sitter_form.sitterphonenumber.data = actual_user.SitterPhoneNumber
            sitter_form.sitteraddress.data = actual_user. SitterAddress
            sitter_form.sitteremail.data = actual_user. SitterEmail 
            sitter_form.sitterExperienceInVet.data = actual_user.SitterVetExp
            sitter_form.sitterExperienceInPetCare.data = actual_user.SitterPetCareExp
            sitter_form.sitterAcceptedPetTypes.data =  actual_user.SitterAccPet
            sitter_form.sitterServiceTypes.data = actual_user.SitterServiceType
            sitter_form.sitterPetSpaceSize.data = actual_user.SitterSpace
            sitter_form.sitterPetFeeder.data=  actual_user.PetFeeder
            sitter_form.sitterCatTree.data =  actual_user.CatTree
            sitter_form.sitterPetBed.data =  actual_user.PetBed
            sitter_form.sitterToy.data =  actual_user.Toy
            sitter_form.sitterSecurityCamera.data=actual_user.SecurityCamera

        if request.method == 'POST':
                # 處理 sitter 表單提交
            actual_user.SitterName = sitter_form.sitterusername.data
            actual_user.SitterPassword= sitter_form.sitterpassword.data
            actual_user.SitterLineID= sitter_form.sitterlineid.data
            actual_user.SitterPhoneNumber = sitter_form.sitterphonenumber.data
            actual_user.SitterAddress = sitter_form.sitteraddress.data
            actual_user.SitterEmail  = sitter_form.sitteremail.data
            actual_user.SitterVetExp=sitter_form.sitterExperienceInVet.data 
            actual_user.SitterPetCareExp=sitter_form.sitterExperienceInPetCare.data
            actual_user.SitterAccPet =sitter_form.sitterAcceptedPetTypes.data
            actual_user.SitterServiceType=sitter_form.sitterServiceTypes.data
            actual_user.SitterSpace=sitter_form.sitterPetSpaceSize.data
            actual_user.PetFeeder=sitter_form.sitterPetFeeder.data
            actual_user.CatTree=sitter_form.sitterCatTree.data
            actual_user.PetBed=sitter_form.sitterPetBed.data
            actual_user.Toy=sitter_form.sitterToy.data
            actual_user.SecurityCamera=sitter_form.sitterSecurityCamera.data
            db.session.commit()
            # 重定向到 'dashboard' 路由
            return redirect(url_for('babysitter'))##回到編輯者頁面
    # 其他情況下，重定向到登入頁面
    #else:
        #return redirect(url_for('owner_search_filter_page')) # 回到登入者頁面

    # 在 GET 請求中，呈現編輯資料頁面
    return render_template('edit_profile.html', owner_form=owner_form, pet_form=pet_form, sitter_form=sitter_form)



@app.route('/SitterOrderList',methods = ["GET"])
def SitterOrderList_Page():
    reservation_id = request.args.get('reservation_id')
    # assume walk or Fostercare ID input
    if Reservation.query.filter_by(reservationid = reservation_id).first().reservationtype == 'foster':
        fostercareid = Fostercare.query.filter_by(reservationid=reservation_id).first().fostercareid
        fostercareitem =Fostercare.query.filter_by(fostercareid=fostercareid).first()
        # type 
        type = Reservation.query.filter_by(reservationid = reservation_id).first().reservationtype
        # date
        fostercare = [fostercareitem]
        #pet
        reserveid = fostercareitem.reservationid
        res = Reservation.query.filter_by(reservationid = reserveid).first()
        pet = [res.pet_reservation]
        #owner f
        owner = [res.owner_reservation]
        #rating
        ownerid = res.owner_reservation.OwnerID
        rating = Review_owner.query.filter_by(ownerid=ownerid).all()
        ratings = [i.ownerrating for i in rating]
        average_rating = sum(ratings) / len(ratings)
        #petsitterid stored in session for reviews
        test1 = res.ownerID
        test2 = res.reservationid
        session["ownerid"] = res.ownerID
        session["reservationid"] = res.reservationid
        return render_template('SitterOrderList.html', pet=pet ,fostercare = fostercare, type = type, 
                            avg_rating = average_rating, owner=owner,test1 = test1,test2 = test2)
    else:
        walk_id = Walk.query.filter_by(reservationid=reservation_id).first().walkid
        walkitem =Walk.query.filter_by(walkid=walk_id).first()
        # type 
        type = Reservation.query.filter_by(reservationid = reservation_id).first().reservationtype
        # date & duration & frequency
        walk = [walkitem]
        #pet
        reserveid = walkitem.reservationid
        res = Reservation.query.filter_by(reservationid = reserveid).first()
        pet = [res.pet_reservation]
        #owner f
        owner = [res.owner_reservation]
        #rating
        ownerid = res.owner_reservation.OwnerID
        rating = Review_owner.query.filter_by(ownerid=ownerid).all()
        ratings = [i.ownerrating for i in rating]
        average_rating = sum(ratings) / len(ratings)
        #petsitterid stored in session for reviews
        session["ownerid"] = res.ownerID
        session["reservationid"] = res.reservationid
        return render_template('SitterOrderList.html', pet=pet ,walk = walk, type = type,
                            avg_rating = average_rating, owner=owner)

@app.route('/OwnerReviewPage')
def OwnerReview_Page():
        ownerid = session["ownerid"]
        reservationid = session["reservationid"]
        reviews = Review_owner.query.filter_by(ownerid=ownerid).all()
        #owner
        owner = Owner.query.filter_by(OwnerID=ownerid).first().OwnerName 
        #rating
        rating = Review_owner.query.filter_by(ownerid=ownerid).all()
        ratings = [i.ownerrating for i in rating]
        average_rating = sum(ratings) / len(ratings)
        return render_template('OwnerReview.html',reviews=reviews,
                                avg_rating = average_rating,owner = owner,reservation_id = reservationid)

@app.route('/comment', methods=['GET', 'POST'])
def comment():
    if request.method == 'GET':
        actual_user = current_user._get_current_object()
        if isinstance(actual_user, Owner):
            form = commentForm_owner()
            return render_template('comment.html', form=form)
        elif isinstance(actual_user, Petsitter):
            form = commentForm_sitter()
            return render_template('comment.html', form=form)
    if request.method == 'POST':
        actual_user = current_user._get_current_object()
    # 從 URL 參數中獲取 'seller_id'
        reservationid = session["reservationid"]#抓reservation_id
        # 根據當前用戶的身份確定 owner_id 和 sitter_id
        if isinstance(actual_user, Owner):
            form = commentForm_owner()
            owner_id = actual_user.OwnerID
            sitter_id = Reservation.query.filter_by(reservationid = reservationid).first().sitterID
            form.sitterrating.data = request.form['sitterrating']
            form.sittercomment.data = request.form['sittercomment']
            form.reservationid.data= reservationid#抓reservation_id
            newdata=Review_sitter(ownerid=owner_id,
                           sitterid=sitter_id,
                           sittercomment=form.sittercomment.data,
                           reservationid=form.reservationid.data,
                           sitterrating=form.sitterrating.data)
            db.session.add(newdata)
            db.session.commit()
            
            return redirect(url_for('babyowner'))  # 返回到個人頁面
        elif isinstance(actual_user, Petsitter):
            form = commentForm_sitter()
            owner_id = Reservation.query.filter_by(reservationid = reservationid).first().ownerID
            sitter_id = actual_user.SitterID
            form.ownerrating.data = request.form['ownerrating']
            form.ownercomment.data = request.form['ownercomment']
            form.reservationid.data= reservationid#抓reservation_id
            newdata=Review_owner(ownerid=owner_id,
                           sitterid=sitter_id,
                           ownercomment=form.ownercomment.data,
                           reservationid=form.reservationid.data,
                           ownerrating=form.ownerrating.data )
            db.session.add(newdata)
            db.session.commit()
            
            return redirect(url_for('babysitter'))  # 返回到個人頁面
        else:
            flash('Invalid commented user ID!', 'danger')
    return render_template('comment.html', form=form)

@app.route('/babyowner',methods=['GET'])
def babyowner():
    if current_user.is_authenticated:
        acutal_user = current_user._get_current_object()
        if isinstance(acutal_user, Owner):
            OwnerID = acutal_user.OwnerID
            Reservations = Reservation.query.filter_by(ownerID=OwnerID).all()
            reservation_data = []

            for reservation in Reservations:
                petID = reservation.petID
                sitterID = reservation.sitterID
                pet = Pet.query.filter_by(petID=petID).first()
                sitter = Petsitter.query.filter_by(SitterID=sitterID).first()
                reservation_data.append({
                    'reservation': reservation,
                    'pet': pet,
                    'sitter': sitter
                })

            session["ownerid"] = OwnerID
            session["petid"] = Pet.query.filter_by(ownerID=OwnerID).first().petID    
                
    return render_template('BabyOwner.html', reservations=reservation_data)


@app.route('/owner_search_filter', methods=['GET', 'POST'])
def owner_search_filter_page():
    return render_template('OwnerSearchFilter.html')

@app.route('/owner_search_reservation', methods=['GET', 'POST'])
def owner_search_reservation_page(): 
    condition1 = request.args.get('condition1')
    condition2 = request.args.get('condition2')
    condition3 = request.args.get('condition3')
    condition4 = request.args.get('condition4')

    # 根據篩選條件獲取篩選結果
    avg_rating_subquery = (
        db.session.query(
            Review_sitter.sitterid,
            func.avg(Review_sitter.sitterrating).label('avg_rating')
        )
        .group_by(Review_sitter.sitterid)
        .subquery()
    )
    query = db.session.query(Petsitter, avg_rating_subquery.c.avg_rating).join(avg_rating_subquery, Petsitter.SitterID == avg_rating_subquery.c.sitterid)

    if condition1 :
        query = query.filter(Petsitter.SitterServiceType == condition1)
    if condition2:
        query = query.filter(avg_rating_subquery.c.avg_rating >= float(condition2))
    if condition3:
         query = query.filter(Petsitter.SitterAccPet == condition3)
    if condition4 == 'yes':
        query = query.filter(Petsitter.SitterVetExp == 'yes')

    filtered_data = query.all()  

    filter = []
    for petsitter, avg_rating in filtered_data:
        sitterid = petsitter.SitterID
        sittername = petsitter.SitterName
        avgrating = avg_rating
        servicetype = petsitter.SitterServiceType  # 直接從 Petsitter 對象中獲取
        filter.append({
            'sitterid': sitterid,
            'sittername': sittername,
            'avgrating': avgrating,
            'servicetype': servicetype
        })   

    return render_template('OwnerSearchResult.html',filterdata = filter)
    
#PlaceOrderPage-Walk
@app.route('/place_order_page_walk', methods=['GET', 'POST'])
def owner_search_reservation_walk_page():
    form = OwnerReservationWalkForm()
    sitter_id = request.args.get('sitterid')
    session["sitterid"] = sitter_id
    owner_id = session["ownerid"]
    petid = session["petid"]
    sittername = Petsitter.query.filter_by(SitterID=sitter_id).first().SitterName

    
    if form.validate_on_submit():
        reservation_to_create = Reservation(ownerID = owner_id, 
                                            sitterID = sitter_id, 
                                            petID =petid,
                                            reservationtype="walk")        
                 
        db.session.add(reservation_to_create)  
        db.session.commit()    

        walkreservation_to_create = Walk(startdate = form.startdate.data,
                                            duration = form.duration.data,
                                            frequency = form.frequency.data,
                                            reservationid = reservation_to_create.reservationid)
        
        db.session.add(walkreservation_to_create)  
        db.session.commit()
    
        session["reservationid"] = reservation_to_create.reservationid
        session["sitterid"] = sitter_id 

        print("Form is valid and submitted successfully!")
        return redirect(url_for('babyowner')) 
                                            
    return render_template('PlaceOrderPage-Walk.html',form = form, sittername =sittername, sitter_id = sitter_id  ) 
    
#PlaceOrderPage-Foster
@app.route('/place_order_page_foster', methods=['GET', 'POST'])
def owner_search_reservation_foster_page():
    form = OwnerReservationFosterForm()
    sitter_id = request.args.get('sitterid')
    session["sitterid"] = sitter_id 
    owner_id = session["ownerid"]
    petid = session["petid"]


    sittername = Petsitter.query.filter_by(SitterID=sitter_id).first().SitterName

    if form.validate_on_submit():
        reservation_to_create = Reservation(ownerID = owner_id, 
                                            sitterID = sitter_id, 
                                            petID =petid,
                                            reservationtype="foster")        
                 
        db.session.add(reservation_to_create)  
        db.session.commit()    

        fosterreservation_to_create = Fostercare(startdate = form.startdate.data,
                                            enddate = form.enddate.data,
                                            reservationid = reservation_to_create.reservationid)
        
        db.session.add(fosterreservation_to_create)  
        db.session.commit()
    
        session["reservationid"] = reservation_to_create.reservationid
        

        #print("Form is valid and submitted successfully!")
        return redirect(url_for('babyowner')) 
                                            
    return render_template('PlaceOrderPage-Foster.html',form = form, sittername =sittername, sitter_id = sitter_id)



@app.route('/OwnerOrderListPage')
def OwnerOrderList_Page():
    # assume walk or Fostercare ID input
    reservation_id = session["reservationid"]  ####
    #reservation_id = request.args.get('reservation_id')
    if Reservation.query.filter_by(reservationid = reservation_id).first().reservationtype == 'foster':
        fostercareid = Fostercare.query.filter_by(reservationid=reservation_id).first().fostercareid
        fostercareitem =Fostercare.query.filter_by(fostercareid=fostercareid).first()
        # type 
        type = Reservation.query.filter_by(reservationid = reservation_id).first().reservationtype
        # date
        fostercare = [fostercareitem]
        #pet
        reserveid = fostercareitem.reservationid
        res = Reservation.query.filter_by(reservationid = reserveid).first()
        pet = res.pet_reservation
        #owner
        owner = res.owner_reservation
        #sitter
        sitter = [res.sitter_reservation]
        # for comments
        session["reservationid"] = res.reservationid
        return render_template('OwnerOrderList.html',fostercare = fostercare, 
                               pet=pet,owner = owner,sitter=sitter,type = type)
    else:
        walk_id = Walk.query.filter_by(reservationid=reservation_id).first().walkid
        walkitem =Walk.query.filter_by(walkid=walk_id).first()
        # type 
        type = Reservation.query.filter_by(reservationid = reservation_id).first().reservationtype
        # date & duration & frequency
        walk = [walkitem]
        #pet
        reserveid = walkitem.reservationid
        res = Reservation.query.filter_by(reservationid = reserveid).first()
        pet = res.pet_reservation
        #owner
        owner = res.owner_reservation
        #sitter
        sitter = [res.sitter_reservation]
        # for reviews
        session["reservationid"] = res.reservationid
        return render_template('OwnerOrderList.html',walk = walk, 
                               pet=pet,owner = owner,sitter=sitter,type = type)





@app.route('/SitterReviewPage', methods=['GET', 'POST'])
def SitterReview_Page():
        sitterid = session["sitterid"]
        sitter = [Petsitter.query.filter_by(SitterID=sitterid).first()]
        #ratings
        rating = Review_sitter.query.filter_by(sitterid=sitterid).all()
        ratings = [i.sitterrating for i in rating]
        average_rating = sum(ratings) / len(ratings)
        return render_template('SitterReview.html',sitter=sitter, avg_rating = average_rating)



@app.route('/logout')
def logout_page():
    logout_user()
    session.pop('type', None) 
    flash("You have been logged out!", category='info')
    return redirect(url_for("home_page"))



