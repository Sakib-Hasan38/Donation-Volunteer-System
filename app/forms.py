from django import forms
from django.contrib.auth.models import User
from .models import Donar, Payment
from .models import Volunteer, Donation, DonationArea
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,UsernameField, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth import password_validation

class LoginForm(AuthenticationForm):
    username = UsernameField(required=True,widget=forms.TextInput(attrs={'autofocus ': 'True', 'class':'form-control','placeholder': 'Username'}))
    password = forms.CharField(required=True,widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}))


class UserForm (UserCreationForm):    #(forms.ModelForm) : #(UserCreationForm):
    password1 = forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Enter Password'}))
    password2 = forms.CharField(label='Confirm Password (again)', widget=forms.PasswordInput(attrs={'class' : 'form-control', 'placeholder': 'Enter Password Again'}) )

   #  password = cleaned_data.get('password')
      #  confirm_password = cleaned_data.get('confirm_password')

       # if password and confirm_password and password != confirm_password:
            #self.add_error('confirm_password','Password donot match')
      #  return cleaned_data
    
        

    class Meta:
        model = User
        fields=['first_name', 'last_name', 'username', 'email', 'password1','password2']
        widgets={
            'first_name' : forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Enter First Name'}),
            'last_name' : forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Enter last Name'}),
            'username' : forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Username'}),
            'email' : forms.EmailInput(attrs={'class':'form-control', 'placeholder': 'Email ID'})
        }

    def clean(self):
       cleaned_data = super().clean()
       password1 = cleaned_data.get('password1')
       password2 = cleaned_data.get('password2')
       if password1 and password2 and password1 != password2:
           self.add_error('password2','Passwords Donot Match')
        
       return cleaned_data

class DonarSignupForm(forms.ModelForm):
    userpic = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control'})),
    class Meta:
        model = Donar
        fields=['contact', 'userpic', 'address']
        widgets={
            'contact' : forms.NumberInput(attrs={'class':'form-control', 'placeholder': 'Contact Number'}),
            'address' : forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Full Address'})
        }

class VolunteerSignupForm(forms.ModelForm):
    userpic = forms.ImageField(),
    idpic = forms.ImageField(),
    class Meta:
        model =Volunteer
        fields=['contact', 'userpic','idpic','address','aboutme']
        widgets={
            'contact' : forms.NumberInput(attrs={'class':'form-control', 'placeholder': 'Contact Number'}),
            'address' : forms.Textarea(attrs={'class':'form-control', 'rows':4 ,'placeholder': 'Full Address'}),
            'aboutme' : forms.Textarea(attrs={'class':'form-control', 'rows':4, 'placeholder': 'About Me'}),
            'userpic' : forms.FileInput(attrs={'class':'form-control'}),
            'idpic' : forms.FileInput(attrs={'class':'form-control'})
        }

        labels={
            'userpic' : 'User Picture',
            'idpic' : 'Id Proof Picture',
            'aboutme' : 'About Me'
        }

    def clean(self):
       cleaned_data = super().clean()
       password1 = cleaned_data.get('password1')
       password2 = cleaned_data.get('password2')
       if password1 and password2 and password1 != password2:
           self.add_error('password2','Passwords Donot Match')
        
       return cleaned_data
    

class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label='Old Password', strip= False, widget=forms.PasswordInput(attrs=
      {'autocomplete' : 'current_password', 'autofocus':True, 'class':'form-control','placeholder':'Old Password'}))
    new_password1 = forms.CharField(label='New Password', strip= False, widget=forms.PasswordInput(attrs=
      {'autocomplete' : 'new_password','class':'form-control','placeholder':'New Password'}),
       help_text = password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label='Confirm Password', strip= False, widget=forms.PasswordInput(attrs=
      {'autocomplete' : 'new_password','class':'form-control','placeholder':'Confirm Password'}))
    
class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label='Email', max_length=254, widget=forms.EmailInput(attrs=
    {'autocomplete':'email','class':'form-control','placeholder':'Enter Your Email'}))

class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label='New Password', strip=False, widget=forms.PasswordInput(attrs=
    {'autocomplete': 'new-password','class':'form-control','placeholder':'Enter New Password'}),help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label='Confirm New Password', strip= False,widget=forms.PasswordInput(attrs=
    {'autocomplete': 'new-password','class':'form-control','placeholder':'Confirm New Password'}))


DONATION_CHOICES=(
    ('Food Donation','Food Donation'),
    ('Cloth Donation','Cloth Donation'),
    ('Footwear Donation','Footwear Donation'),
    ('Books Donation','Books Donation'),
    ('Furniture Donation','Furniture Donation'),
    ('Vessel Donation','Vessel Donation'),
    ('Other','Other'),
) 

class DonateNowForm(forms.ModelForm):
    donationpic = forms.ImageField(label='Donation Image(that you want to donate)',required=True,widget=forms.ClearableFileInput(attrs={'class':'form-control'}))
    class Meta:
        model = Donation
        fields = ['donationname','donationpic','collectionlocation','description']
        widgets={
            'donationname': forms.Select(choices=[('', 'Choose Your Donation')]+list(DONATION_CHOICES),attrs={'class':'form-control'}),
            'collectionlocation': forms.TextInput(attrs={'class':'form-control','placeholder':'Donation Collection Address'}),
            'description': forms.TextInput(attrs={'class':'form-control','placeholder':'Description (Special Note)'}),
            #'donationpic': forms.ClearableFileInput(attrs={'class':'form-control'}),
        }
        labels={
            'donationpic':'Donation Image(that you want to donate)',
            'donationname':'Donation Name',
            'collectionlocation':'Donation Collection Address',
            'description':'Description (Special Note)',
        }

class DonationAreaForm(forms.ModelForm):
    class Meta:
        model = DonationArea
        fields = ['areaname','description']
        widgets ={
            'areaname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Donation Area'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Description'}),
        }
        labels ={
            'areaname' : 'Donation Area Name',
            'description' : 'Description',
        }


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['amount']

        widgets ={
            'amount' : forms.NumberInput(attrs={'class': 'form-control','Placeholder': 'Enter Donation Amount (e.g. 500)', 'min': '10'}),
            #'payment_method' : forms.Select(attrs={'class' : 'form-control','id':'payment_method'}),
            #'transaction_id' : forms.TextInput(attrs={'class' : 'form-control', 'Placeholder' : 'Enter bKash/Nagad Transaction ID'}),
        }

        labels ={
            'amount' : 'Donation Amount (BDT)',
           # 'payment_method' : 'Select Payment Method',
           # 'transaction_id' : 'Transaction ID',
        }
    