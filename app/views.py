from django.shortcuts import redirect, render
from django.views import View
from .models import Donar,Volunteer, Donation, DonationArea, Gallery, Payment
from .forms import UserForm, DonarSignupForm,VolunteerSignupForm,LoginForm, MyPasswordChangeForm, DonateNowForm, DonationAreaForm, PaymentForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout as auth_logout
from datetime import date
from django.db.models import Sum
import uuid
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.http import JsonResponse  



# Create your views here.
def index(request):
    return render(request, "index.html")


def gallery(request):
    gallery = Gallery.objects.all()
    return render(request, "gallery.html",locals())


class login_admin(View):
    def get(self,request):
      form = LoginForm()
      return render(request, "login-admin.html",locals())
    
    def post(self,request):
        form = LoginForm(request.POST)
        us = request.POST.get('username')
        pwd = request.POST.get('password')

        try:
            user = authenticate(username = us ,password = pwd)
            if user:
                if user.is_staff:
                    login(request, user)
                    messages.success(request, 'Login Successfully')
                    return redirect('/index-admin')
                else:
                    messages.warning(request,"Invalid Admin User")
            else:
                messages.warning(request,"invalid username and password")
        except:
            messages.warning(request,'Login Failed')
        return render(request,'login-admin.html',locals())

class login_donar(View):
    def get(self,request):
        form = LoginForm()
        return render(request, "login-donar.html",locals())
    
    def post(self,request):
        form = LoginForm(request.POST)
        us=request.POST.get('username')
        pwd =request.POST.get('password')
        try:
            user = authenticate(username = us, password = pwd)
            if user:
                donar_user = Donar.objects.filter(user_id = user.id)
                if donar_user:
                    login(request,user)
                    messages.success(request,'Login Successfully')
                    return redirect('/index-donar')
                else:
                    messages.warning(request,'Invalid Donar User')

            else:
                messages.warning(request,'Invalid Username and Password')
        except:
            messages.warning(request,'Login Failed')
        return render(request,'login-donar.html',locals())
                 

class login_volunteer(View):
    def get(self,request):
        form = LoginForm()
        return render(request, "login-volunteer.html",locals())
    
    def post(self,request):
        form = LoginForm(request.POST)
        us=request.POST.get('username')
        pwd =request.POST.get('password')
        try:
            user = authenticate(username = us, password = pwd)
            if user:
                volunteer_user = Volunteer.objects.filter(user_id = user.id)
                if volunteer_user:
                    login(request,user)
                    messages.success(request,'Login Successfully')
                    return redirect('/index-volunteer')
                else:
                    messages.warning(request,'Invalid Volunteer User')

            else:
                messages.warning(request,'Invalid Username and Password')
        except:
            messages.warning(request,'Login Failed')
        return render(request,'login-volunteer.html',locals())


class signup_donar(View):
    def get(self,request):
        form1 = UserForm()
        form2 = DonarSignupForm()
       # context={
       #    'form1': form1,
       #     'form2': form2
       # }
        return render(request, "signup-donar.html",locals())
    
    def post(self,request):
        form1 = UserForm(request.POST)
        form2 = DonarSignupForm(request.POST, request.FILES)
        if form1.is_valid() & form2.is_valid():
            fn = request.POST.get('first_name')
            ln = request.POST.get('last_name')
            em = request.POST.get('email')
            us = request.POST.get('username')
            pwd = request.POST.get('password1')
            contact = request.POST.get('contact')
            userpic = request.FILES.get('userpic')
            address = request.POST.get('address')

            try:
                user = User.objects.create_user(first_name = fn, last_name=ln, username=us, email=em, password=pwd)
                Donar.objects.create(user = user, contact = contact, userpic = userpic, address = address)
                messages.success(request, 'Congratulations !! Donar Profile Created Successfully.')
            except  :
               messages.warning(request,'Profile Not Created')
        
        return render(request, "signup-donar.html",locals())
    

class signup_volunteer(View):
    def get(self,request):
        form1 = UserForm()
        form2 = VolunteerSignupForm()

        return render(request, "signup-volunteer.html",locals())
      
     
    def post(self,request):
        form1 = UserForm(request.POST)
        form2 = VolunteerSignupForm(request.POST, request.FILES)
        if form1.is_valid() and form2.is_valid():
            fn = request.POST.get('first_name')
            ln = request.POST.get('last_name')
            em = request.POST.get('email')
            us = request.POST.get('username')
            pwd = request.POST.get('password1')
            contact = request.POST.get('contact')
            userpic = request.FILES.get('userpic')
            idpic = request.FILES.get('idpic')
            address = request.POST.get('address')
            aboutme = request.POST.get('aboutme')


            try:
                user = User.objects.create_user(first_name = fn, last_name=ln, username=us, email=em, password=pwd)
                Volunteer.objects.create(user = user, contact = contact, userpic = userpic, idpic = idpic, address = address, aboutme = aboutme, status = 'pending')
                messages.success(request, 'Congratulations !! Volunteer Profile Created Successfully.')
            except  :
                messages.warning(request,'Profile Not Created')

        return render(request, "signup-volunteer.html",locals())
    


def index_admin(request):
    if not request.user.is_authenticated:
         return redirect('login-admin')
    totaldonations = Donation.objects.all().count()
    totaldonars = Donar.objects.all().count()
    totalvolunteers = Volunteer.objects.all().count()
    totalpendingdonations = Donation.objects.filter(status = 'pending').count()
    totalaccepteddonations = Donation.objects.filter(status = 'accept').count()
    totaldelivereddonations = Donation.objects.filter(status = 'Donation Delivered Successfully').count()
    totaldonationarea = DonationArea.objects.all().count()

    totalpayments = Payment.objects.all().count()
    totalamounts = Payment.objects.filter(status='Success').aggregate(total=Sum('amount'))['total'] or 0

    return render(request, "index-admin.html",locals())


# admin dashboard
def pending_donation(request):
    if not request.user.is_authenticated:
        return redirect('/login-admin')
    donation = Donation.objects.filter(status = 'pending')
    return render(request, "pending-donation.html",locals())


def accepted_donation(request):
    if not request.user.is_authenticated:
        return redirect('/login-admin')
    donation = Donation.objects.filter(status = 'accept')
    return render(request, "accepted-donation.html",locals())


def rejected_donation(request):
    if not request.user.is_authenticated:
         return redirect('/login-admin')
    donation = Donation.objects.filter(status = 'reject')
    return render(request, "rejected-donation.html",locals())


def volunteerallocated_donation(request):
    if not request.user.is_authenticated:
        return redirect('/login-admin')
    donation = Donation.objects.filter(status = 'Volunteer Allocated')
    return render(request, "volunteerallocated-donation.html",locals())


def donationrec_admin(request):
    if not request.user.is_authenticated:
        return redirect('/login-admin')
    donation = Donation.objects.filter(status = 'Donation Received')
    return render(request, "donationrec-admin.html",locals())


def donationnotrec_admin(request):
    if not request.user.is_authenticated:
        return redirect('/login-admin')
    donation = Donation.objects.filter(status = 'Donation Not Received')
    return render(request, "donationnotrec-admin.html",locals())


def donationdelivered_admin(request):
    if not request.user.is_authenticated:
        return redirect('/login-admin')
    donation = Donation.objects.filter(status = 'Donation Delivered Successfully')
    return render(request, "donationdelivered-admin.html",locals())


def all_donations(request):
    if not request.user.is_authenticated:
        return redirect('/login-admin')
    donation = Donation.objects.all()
    return render(request, "all-donations.html",locals())


def delete_donation(request,pid):
    donation = Donation.objects.get(id=pid)
    donation.delete()
    return redirect('all_donations')


def manage_donar(request):
    if not request.user.is_authenticated:
        return redirect('/login-admin')
    donar = Donar.objects.all()
    return render(request, "manage-donar.html",locals())


def new_volunteer(request):
    if not request.user.is_authenticated:
        return redirect('/login-admin')
    volunteer = Volunteer.objects.filter(status = 'pending')
    return render(request, "new-volunteer.html",locals())


def accepted_volunteer(request):
    if not request.user.is_authenticated:
        return redirect('/login-admin')
    volunteer = Volunteer.objects.filter(status = 'accept')
    return render(request, "accepted-volunteer.html",locals())


def rejected_volunteer(request):
    if not request.user.is_authenticated:
        return redirect('/login-admin')
    volunteer = Volunteer.objects.filter(status = 'reject')
    return render(request, "rejected-volunteer.html",locals())


def all_volunteer(request):
    if not request.user.is_authenticated:
        return redirect('/login-admin')
    volunteer = Volunteer.objects.all()
    return render(request, "all-volunteer.html",locals())

def delete_volunteer(request,pid):
    user = User.objects.get(id=pid)
    user.delete()
    return redirect('all-volunteer')

class add_area(View):
    def get(self,request):
        form = DonationAreaForm()
        return render(request, "add-area.html",locals())

    def post(self,request):
        form = DonationAreaForm(request.POST)
        if not request.user.is_authenticated:
            return redirect('login-admin')
        areaname = request.POST['areaname']
        description = request.POST['description']
        try:
            DonationArea.objects.create(areaname = areaname, description = description)
            messages.success(request,'Area Added Successfully')
        except:
            messages.warning(request,'Area Not Added')
        return render(request, "add-area.html",locals())


class edit_area(View):
    def get(self,request,pid):
        form = DonationAreaForm()
        area = DonationArea.objects.get(id = pid)
        return render(request, "edit-area.html",locals()) 

    def post(self,request,pid):
            if not request.user.is_authenticated:
                return redirect('/login-admin')
            form = DonationAreaForm(request.POST)
            area = DonationArea.objects.get(id = pid)
            areaname = request.POST['areaname']
            description = request.POST['description']

            area.areaname = areaname
            area.description = description


            try:
                area.save()
                messages.success(request,'Area Updated Successfully')
                return redirect('/manage-area/')
            except:
                messages.warning(request,'Area Not Updated')
            return render(request, "edit-area.html")


def manage_area(request):
    if not request.user.is_authenticated:
        return redirect('/login-admin')
    area = DonationArea.objects.all()
    return render(request, "manage-area.html",locals())

def delete_area(request,pid):
    if not request.user.is_authenticated:
        return redirect('/login-admin')
    area = DonationArea.objects.get(id=pid)
    area.delete()
    return redirect('/manage-area/')


class changepwd_admin(View):
    def get(self,request):
      form = MyPasswordChangeForm(request.user)
      return render(request, "changepwd-admin.html",locals())
    
    def post(self,request):
        form = MyPasswordChangeForm(request.user,request.POST)
        if not request.user.is_authenticated:
            return redirect('/login_admin')
        
        old = request.POST.get('old_password')
        newpass = request.POST.get('new_password1')
        confirmpass = request.POST.get('new_password2')
        try:
            if newpass == confirmpass:
                user = User.objects.get(id=request.user.id)
                if user.check_password(old):
                    if user.check_password(newpass):
                        messages.warning(request,'New Password Cannot be Same as Old Password')
                    else:
                        user.set_password(newpass)
                        user.save()
                        messages.success(request,'Change Password Successfully')
                        #return redirect('index-admin')
                else:
                    messages.warning(request,'Old Password not matched')
            else:
                messages.warning(request,'New Password and Confirm Password are Different')
        except:
            messages.warning(request,'Failed to Change Password')
        return render(request,'changepwd-admin.html',locals())
    

def logout(request):
    auth_logout(request)
    return redirect("index")


# admin view details
class accepted_donationdetail(View):
    def get(self,request,pid):
      donation = Donation.objects.get(id = pid)
      donationarea = DonationArea.objects.all()
      volunteer = Volunteer.objects.filter(status = 'accept')
      #volunteer = Volunteer.objects.all()
      return render(request, "accepted-donationdetail.html",locals())

    def post(self,request,pid):
        if not request.user.is_authenticated:
            return redirect('/login_admin')

        donation = Donation.objects.get(id=pid)
        donationareaid = request.POST['donationareaid']
        volunteerid = request.POST['volunteerid']
        adminremark = request.POST['adminremark']

        da = DonationArea.objects.get(id=donationareaid)
        vo = Volunteer.objects.get(id=volunteerid)

        try:
            donation.donationarea = da
            donation.volunteer = vo
            donation.adminremark = adminremark
            donation.status = 'Volunteer Allocated'
            donation.volunteerremark = 'Not Updated Yet'
            donation.updationdate = date.today()
            donation.save()
            messages.success(request,'Volunteer Allocated Successfully')
        except:
            messages.warning(request,'Failed to Allocated Volunteer')
        return render(request, "accepted-donationdetail.html",locals())


class view_volunteerdetail(View):
    def get(self,request,pid):
        if not request.user.is_authenticated:
            return redirect('/login_admin')
        volunteer = Volunteer.objects.get(id = pid)
        return render(request, "view-volunteerdetail.html",locals())

    def post(self,request,pid):
        if not request.user.is_authenticated:
            return redirect('/login_admin')
        volunteer = Volunteer.objects.get(id = pid)
        status = request.POST['status']
        adminremark = request.POST['adminremark']
        try :
            volunteer.adminremark = adminremark
            volunteer.status = status
            volunteer.updationdate = date.today()
            volunteer.save()
            messages.success(request,'Volunteer Updated Successfully')
        except:
            messages.warning(request,'Volunteer Not Updated Successfully')
        return render(request, "view-volunteerdetail.html",locals())


def view_donardetail(request, pid):
    if not request.user.is_authenticated:
        return redirect('/login_admin')
    donar = Donar.objects.get(id = pid)
    return render(request, "view-donardetail.html",locals())


class view_donationdetail(View):
    def get(self,request,pid):
        donation = Donation.objects.get(id = pid)
        return render(request, "view-donationdetail.html",locals())

    def post(self,request,pid):
        if not request.user.is_authenticated:
            return redirect('/login_admin')
        donation = Donation.objects.get(id = pid)
        status = request.POST['status']
        adminremark = request.POST['adminremark']
        try :
            donation.adminremark = adminremark
            donation.status = status
            donation.updationdate = date.today()
            donation.save()
            messages.success(request,'Status & Remark Updated Successfully')
        except:
            messages.warning(request,'Failed to Update Status & Remark')
            #return render(request, "view-donationdetail.html",locals())
        return render(request, "view-donationdetail.html",locals())

def delete_donar(request,pid):
    user = User.objects.get(id=pid)
    user.delete()
    return redirect('/manage_donar')
       

# donar dashboard
def index_donar(request):
    if not request.user.is_authenticated:
        return redirect('/login_donar')
    user = request.user
    try:
        donar = Donar.objects.get(user = user)
    except Donar.DoesNotExist:
        return redirect('/signup_donar')
    donationcount = Donation.objects.filter(donar = donar).count()
    acceptedcount = Donation.objects.filter(donar = donar, status = 'accept').count()
    rejectedcount = Donation.objects.filter(donar = donar, status = 'reject').count()
    pendingcount = Donation.objects.filter(donar = donar, status = 'pending').count()
    deliveredcount = Donation.objects.filter(donar = donar, status = 'Donation Delivered Successfully').count()
    return render(request, "index-donar.html",locals())


class donate_now(View):
    def get(self,request):
        form = DonateNowForm()
        return render(request, "donate-now.html",locals())

    def post(self,request):
        form = DonateNowForm(request.POST,request.FILES)
        if not request.user.is_authenticated:
            return redirect('/login_donar')
        if form.is_valid():
            user = request.user
            donar = Donar.objects.get(user=user)
            donationname = request.POST.get('donationname')
            donationpic = request.FILES.get('donationpic')
            collectionlocation = request.POST.get('collectionlocation')
            description = request.POST.get('description')

            try:
                Donation.objects.create(donar = donar, donationname = donationname, donationpic = donationpic, collectionlocation = collectionlocation, description = description, status = 'pending', donationdate = date.today())
                messages.success(request,'Donation Save Successfully')
            except:
                messages.warning(request,'Failed to Donation')
        return render(request,'donate-now.html',locals())


def donation_history(request):
    if not request.user.is_authenticated:
         return redirect('/login_donar')
    user = request.user
    donar = Donar.objects.get(user = user)
    donation = Donation.objects.filter(donar = donar)
    return render(request, "donation-history.html",locals())


class profile_donar(View):
    def get(self,request):
        form1 = UserForm()
        form2 = DonarSignupForm()
        user = request.user
        donar = Donar.objects.get(user= user)
        return render(request, "profile-donar.html",locals())

    def post(self,request):
        if not request.user.is_authenticated:
            return redirect('/login_donar')

        form1 = UserForm(request.POST)
        form2 = DonarSignupForm(request.POST)

        user = request.user
        donar = Donar.objects.get(user = user)

        fn = request.POST.get('firstname')
        ln = request.POST.get('lastname')
        contact = request.POST.get('contact')
        address = request.POST.get('address')

        donar.user.first_name = fn
        donar.user.last_name = ln
        donar.contact = contact
        donar.address = address

        try:
            userpic = request.FILES['userpic']
            donar.userpic = userpic
            donar.save()
            donar.user.save()
            messages.success(request,'Profile Updated Successfully')
        except Exception as e:
            messages.warning(request,f'Profile Update Failed+ : {e}')
        return render(request,'profile-donar.html',locals())



class changepwd_donar(View):
    def get(self,request):
      form = MyPasswordChangeForm(request.user)
      return render(request, "changepwd-donar.html",locals())
    
    def post(self,request):
        form = MyPasswordChangeForm(request.user,request.POST)

        if not request.user.is_authenticated:
            return redirect('/login_donar')
        
        old = request.POST.get('old_password')
        newpass = request.POST.get('new_password1')
        confirmpass = request.POST.get('new_password2')
        try:
            if newpass == confirmpass:
                user = User.objects.get(id=request.user.id)
                if user.check_password(old):
                    if user.check_password(newpass):
                        messages.warning(request,'New Password Cannot be Same as Old Password')
                    else:
                        user.set_password(newpass)
                        user.save()
                        messages.success(request,'Change Password Successfully')
                        #return redirect('index-donar')
                else:
                    messages.warning(request,'Old Password not matched')
            else:
                messages.warning(request,'New Password and Confirm Password are Different')
        except:
              messages.warning(request,'Failed to Change Password')    
        return render(request,'changepwd-donar.html',locals())

# volunteer dashboard
def index_volunteer(request):
    if not request.user.is_authenticated:
        return redirect('/login_volunteer')

    user = request.user
    volunteer = Volunteer.objects.get(user = user)
    totalCollectionRequest = Donation.objects.filter(volunteer = volunteer, status = 'Volunteer Allocated').count()
    totalReceivedDonation = Donation.objects.filter(volunteer = volunteer, status = 'Donation Received').count()
    totalNotReceivedDonation = Donation.objects.filter(volunteer = volunteer, status = 'Donation Not Received').count()
    totalDonationDelivered = Donation.objects.filter(volunteer = volunteer, status = 'Donation Delivered Successfully').count()
    return render(request, "index-volunteer.html",locals())


def collection_req(request):
    if not request.user.is_authenticated:
        return redirect('/login_volunteer')
    user = request.user
    volunteer = Volunteer.objects.get(user = user)
    donation = Donation.objects.filter(volunteer = volunteer, status = 'Volunteer Allocated')
    return render(request, "collection-req.html",locals())


def donationrec_volunteer(request):
    if not request.user.is_authenticated:
        return redirect('/login_volunteer')
    user = request.user
    volunteer = Volunteer.objects.get(user = user)
    donation = Donation.objects.filter(volunteer = volunteer, status = 'Donation Received')
    return render(request, "donationrec-volunteer.html",locals())


def donationnotrec_volunteer(request):
    if not request.user.is_authenticated:
        return redirect('/login_volunteer')
    user = request.user
    volunteer = Volunteer.objects.get(user = user)
    donation = Donation.objects.filter(volunteer = volunteer, status = 'Donation Not Received')
    return render(request, "donationnotrec-volunteer.html",locals())


def donationdelivered_volunteer(request):
    if not request.user.is_authenticated:
        return redirect('/login_volunteer')
    user = request.user
    volunteer = Volunteer.objects.get(user = user)
    donation = Donation.objects.filter(volunteer = volunteer, status = 'Donation Delivered Successfully')
    return render(request, "donationdelivered-volunteer.html",locals())


class profile_volunteer(View):
    def get(self,request):
        form1 = UserForm()
        form2 = VolunteerSignupForm()
        user = request.user
        volunteer =Volunteer.objects.get(user= user)
        return render(request, "profile-volunteer.html",locals())

    def post(self,request):
        if not request.user.is_authenticated:
          return redirect('/login_volunteer')
    
        form1 = UserForm(request.POST)
        form2 = VolunteerSignupForm(request.POST)
    
        user = request.user
        volunteer = Volunteer.objects.get(user = user)
    
        fn = request.POST.get('firstname')
        ln = request.POST.get('lastname')
        contact = request.POST.get('contact')
        address = request.POST.get('address')
        aboutme = request.POST.get('aboutme')
    
        volunteer.user.first_name = fn
        volunteer.user.last_name = ln
        volunteer.contact = contact
        volunteer.address = address
        volunteer.aboutme = aboutme
    
        try:
            userpic = request.FILES['userpic']
            volunteer.userpic = userpic
            idpic = request.FILES['idpic']
            volunteer.idpic = idpic
            volunteer.save()
            volunteer.user.save()
            messages.success(request,'Profile Updated Successfully')
        except Exception as e:
            messages.warning(request,f'Profile Update Failed + : {e}')
        return render(request,'profile-volunteer.html',locals())


class changepwd_volunteer(View):
    def get(self,request):
       form = MyPasswordChangeForm(request.user)
       return render(request, "changepwd-volunteer.html",locals())
     
    def post(self,request):
        form = MyPasswordChangeForm(request.user,request.POST)
        if not request.user.is_authenticated:
            return redirect('/login_volunteer')
        
        old = request.POST.get('old_password')
        newpass = request.POST.get('new_password1')
        confirmpass = request.POST.get('new_password2')
        try:
            if newpass == confirmpass:
                user = User.objects.get(id=request.user.id)
                if user.check_password(old):
                    if user.check_password(newpass):
                        messages.warning(request,'New Password Cannot be Same as Old Password')
                    else:
                        user.set_password(newpass)
                        user.save()
                        messages.success(request,'Change Password Successfully')
                        #return redirect('index-volunteer')
                else:
                    messages.warning(request,'Old Password not matched')
            else:
                messages.warning(request,'New Password and Confirm Password are Different')
        except:
              messages.warning(request,'Failed to Change Password')
        return render(request,'changepwd-volunteer.html',locals())
     
   
# view details
def donationdetail_donar(request, pid):
    if not request.user.is_authenticated:
         return redirect('login_donar')
    donation = Donation.objects.get(id = pid)
    return render(request, "donationdetail-donar.html",locals())


class donationcollection_detail(View):
    def get(self,request,pid):
        if not request.user.is_authenticated:
            return redirect('/login_admin')
        donation = Donation.objects.get(id = pid)
        return render(request, "donationcollection-detail.html",locals())
    
    def post(self,request,pid):
        if not request.user.is_authenticated:
            return redirect('/login_admin')
        donation = Donation.objects.get(id = pid)
        status = request.POST['status']
        volunteerremark = request.POST['volunteerremark']

        try:
            donation.status = status
            donation.volunteerremark = volunteerremark
            donation.updationdate = date.today()
            donation.save()
            messages.success(request,'Volunteer Status & Remark Updated Successfully')
        except:
            messages.warning(request,'Failed to Update Volunteer Status & Remark')

        return render(request, "donationcollection-detail.html",locals())


class donationrec_detail(View):
    def get(self,request,pid):
        if not request.user.is_authenticated:
            return redirect('/login_admin')
        donation = Donation.objects.get(id = pid)
        return render(request, "donationrec-detail.html",locals())

    def post(self,request,pid):
        if not request.user.is_authenticated:
            return redirect('/login_admin')
        donation = Donation.objects.get(id = pid)
        status = request.POST['status']
        deliverypic = request.FILES.get('deliverypic')
    
        try:
            donation.status = status
            donation.updationdate = date.today()
            donation.save()
            Gallery.objects.create(donation = donation, deliverypic = deliverypic)
            messages.success(request,'Donation Delivered Successfully')
        except:
            messages.warning(request,'Donation Delivered Failed')
    
        return render(request, "donationrec-detail.html",locals())

#class make_payment(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('/login-donar')
        form = PaymentForm()
        return render(request, 'make-payment.html', locals())

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('/login-donar')

        form = PaymentForm(request.POST)
        if form.is_valid():
            try:
                donar = Donar.objects.get(user=request.user)

                # ১. ডেটাবেজে সরাসরি Success হিসেবে পেমেন্টটি সেভ করা
                payment = form.save(commit=False)
                payment.donar = donar
                payment.transaction_id = f"TXN-{uuid.uuid4().hex[:10].upper()}"
                payment.payment_method = 'bKash Online'
                payment.status = 'Success'  # পপআপ শেষে ইউজার সাবমিট করলেই এটি সফল হবে
                payment.save()

                # ২. ডাটা পাস করার সুবিধার্থে রিডাইরেক্ট ইউআরএল প্রিপেয়ার করা
                import urllib.parse
                host = request.build_absolute_uri('/')[:-1]
                success_route = f"{host}/payment-success/"
                query_params = urllib.parse.urlencode({
                    'tran_id': payment.transaction_id,
                    'card_type': 'bKash Online',
                    'amount': payment.amount
                })
                return HttpResponseRedirect(f"{success_route}?{query_params}")

            except Donar.DoesNotExist:
                messages.warning(request, 'Donar Profile Not Found')
        return render(request, 'make-payment.html', locals())

# 4. Success Endpoint: Gateway safely submits POST data here upon successful transaction
@csrf_exempt
@csrf_exempt
# views.py ফাইলের payment_success ফাংশনটি সম্পূর্ণ রিপ্লেস করুন:

@csrf_exempt
def payment_success(request):
    # ইউজার লগইন থাকা বাধ্যতামূলক
    if not request.user.is_authenticated:
        return redirect('/login-donar')

    try:
        # ১. বর্তমান লগইন থাকা ইউজারের ডোনার প্রোফাইল খুঁজে বের করা
        donar = Donar.objects.get(user=request.user)
        
        # ২. এই ডোনারের ডাটাবেজে থাকা একদম সর্বশেষ 'Pending' পেমেন্টটি খুঁজে বের করা
        last_pending_payment = Payment.objects.filter(donar=donar, status='Pending').latest('payment_date')
        
        # ৩. কোনো অনলাইন কুয়েরি এরর ছাড়াই সরাসরি ডাটাবেজে স্ট্যাটাস Success এবং মেথড আপডেট করা
        last_pending_payment.status = 'Success'
        last_pending_payment.payment_method = 'bKash/Nagad Online'
        last_pending_payment.save()  # ডাটাবেজে সফলভাবে সংরক্ষণ হলো
        
        # ৪. সফলতার টেমপ্লেটে রেন্ডার করার জন্য ভ্যারিয়েবল সেটআপ
        payment = last_pending_payment
        status = 'Success'
        messages.success(request, '🎉 Thank you! Your donation was completed successfully.')
        
        return render(request, 'payment-success.html', locals())

    except (Donar.DoesNotExist, Payment.DoesNotExist):
        # যদি কোনো কারণে পেন্ডিং পেমেন্ট খুঁজে না পাওয়া যায়
        messages.warning(request, 'কোনো পেন্ডিং ট্রানজেকশন রেকর্ড খুঁজে পাওয়া যায়নি।')
        return redirect('make-payment')
    
# 5. Failure Endpoint
@csrf_exempt
def payment_fail(request):
    if request.method == 'POST':
        tran_id = request.POST.get('tran_id')
        try:
            payment = Payment.objects.get(transaction_id=tran_id)
            payment.status = 'Failed'
            payment.save()
        except Payment.DoesNotExist:
            pass
    messages.error(request, '❌ The transaction could not be processed. Please try again.')
    status = 'Failed'
    return render(request, 'payment-success.html', locals())


# 6. Cancellation Endpoint
@csrf_exempt
def payment_cancel(request):
    if request.method == 'POST':
        tran_id = request.POST.get('tran_id')
        try:
            payment = Payment.objects.get(transaction_id=tran_id)
            payment.status = 'Cancelled'
            payment.save()
        except Payment.DoesNotExist:
            pass
    messages.warning(request, '⚠️ Payment process was cancelled by user.')
    status = 'Cancelled'
    return render(request, 'payment-success.html', locals())

def payment_success(request):

    payment_id = request.session.get("last_payment_id")

    if not payment_id:
        messages.error(
            request,
            "Payment information not found."
        )
        return redirect("payment-history")

    try:
        payment = Payment.objects.get(id=payment_id)

    except Payment.DoesNotExist:
        messages.error(
            request,
            "Payment record not found."
        )
        return redirect("payment-history")

    return render(
        request,
        "payment-success.html",
        {
            "payment": payment
        }
    )

def payment_history(request):
    if not request.user.is_authenticated:
        return redirect('/login_donar')

    user = request.user
    donar = Donar.objects.get(user = request.user)

    payments = Payment.objects.filter(donar = donar).order_by('-payment_date')

    return render(request,'payment-history.html',locals())


def payment_detail(request,pid):
    if not request.user.is_authenticated:
        return redirect('/login_donar')

    user = request.user
    donar = Donar.objects.get(user = request.user)

    payment = Payment.objects.get(id = pid, donar = donar)

    return render(request,'payment-detail.html',locals())


def manage_payment(request):
    if not request.user.is_authenticated:
        return redirect('/login_admin')

    payments = Payment.objects.all().order_by('-payment_date')

    return render(request,'manage-payment.html',locals())

def payment_detail_admin(request, pid):

    if not request.user.is_authenticated:
        return redirect('/login_admin')
    
    payment = Payment.objects.get(id = pid)

    if request.method == 'POST':
        payment.status = request.POST.get('status')
        payment.save()
        messages.success(request,'Payment Status Updated Successfully')

        return redirect('payment_detail_admin', pid=payment.id)
    

    return render(request,'payment-detail-admin.html',locals())


def delete_payment_admin(request, pid):

    if not request.user.is_authenticated:
        return redirect('/login_admin')
    
    payment = Payment.objects.get(id = pid)

    payment.delete()

    messages.success(request,'Payment Deleted Successfully.')
    return redirect('manage_payment')


def delete_payment(request, pid):

    if not request.user.is_authenticated:
        return redirect('/login_donar')
    try:
        payment = Payment.objects.get(id = pid)
        payment.delete()
        messages.success(request,'Payment Deleted Successfully.')
    except Payment.DoesNotExist:
        messages.warning(request,'Payment Record Not Found')
    return redirect('payment-history')


