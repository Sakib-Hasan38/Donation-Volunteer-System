from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Donar(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contact = models.CharField(max_length=15, null=True)
    address = models.CharField(max_length=300, null=True)
    userpic = models.ImageField(upload_to='Donar', null=True, blank=True)
    regdate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    

class Volunteer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contact = models.CharField(max_length=15, null=True)
    address = models.CharField(max_length=300, null=True)
    userpic = models.ImageField(upload_to='Volunteer', null=True, blank=True)
    idpic = models.ImageField(upload_to='Volunteer', null=True, blank=True )
    aboutme = models.CharField(max_length=300, null=True)
    status = models.CharField(max_length=20, null=True)
    regdate = models.DateTimeField(auto_now_add=True)
    adminremark = models.CharField(max_length=300, null=True)
    updationdate = models.DateField(null=True)

    def __str__(self):
        return self.user.username
    
class DonationArea(models.Model):
    areaname = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    creationdate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.areaname

DONATION_CHOICES=(
    ('Food Donation','Food Donation'),
    ('Cloth Donation','Cloth Donation'),
    ('Footwear Donation','Footwear Donation'),
    ('Books Donation','Books Donation'),
    ('Furniture Donation','Furniture Donation'),
    ('Vessel Donation','Vessel Donation'),
    ('Other','Other'),
) 


class Donation(models.Model):
    donar = models.ForeignKey(Donar, on_delete=models.CASCADE)
    donationname = models.CharField(choices= DONATION_CHOICES,max_length=100, null=True, blank= True)
    donationpic = models.ImageField(upload_to='donation', null=True, blank=True )
    collectionlocation = models.CharField(max_length=300, null=True)
    description = models.CharField(max_length=300, null=True)
    status = models.CharField(max_length=30, null=True)
    donationdate = models.DateField(null=True)
    adminremark = models.CharField(max_length=200, null=True)
    volunteer = models.ForeignKey(Volunteer, on_delete=models.CASCADE, null=True)
    donationarea = models.ForeignKey(DonationArea, on_delete=models.CASCADE, null=True)
    volunteerremark = models.CharField(max_length=200, null=True)
    updationdate = models.DateField(null=True)

    def __str__(self):
        return str(self.id)
    
class Gallery(models.Model):
    donation = models.ForeignKey(Donation, on_delete=models.CASCADE)
    deliverypic = models.FileField(upload_to='gallery/', null=True, blank=True)
    creationdate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

PAYMENT_METHOD_CHOICES=(
    ('bKash', 'bKash'),
    ('Nagad', 'Nagad'),
    ('Card', 'Card'),
    ('Bank Transfer', 'Bank Transfer'),
)

PAYMENT_STATUS_CHOICES=(
    ('Pending', 'Pending'),
    ('Success', 'Success'),
    ('Failed', 'Failed'),
    ('Cancelled', 'Cancelled'),
)

class Payment(models.Model):
    donar = models.ForeignKey(Donar, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=30, choices= PAYMENT_METHOD_CHOICES)
    transaction_id = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=20, choices= PAYMENT_STATUS_CHOICES, default='Pending')
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.donar.user.username} - {self.amount}"






    



