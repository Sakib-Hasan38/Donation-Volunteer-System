from django.contrib import admin
from .models import Donar, Volunteer, DonationArea, Donation, Gallery

# Register your models here.
@admin.register(Donar)
class DonarAdmin(admin.ModelAdmin):
    list_display = ('id','user','contact','address','regdate')

@admin.register(Volunteer)
class VolunteerAdmin(admin.ModelAdmin):
    list_display = ('id','user','contact','address','regdate')

@admin.register(DonationArea)
class DonationAreaAdmin(admin.ModelAdmin):
    list_display = ('id','areaname','description','creationdate')

@admin.register(Donation)
class DonationAreaAdmin(admin.ModelAdmin):
    list_display = ('id','donar','volunteer','donationarea','donationname')

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ('id','donation','deliverypic','creationdate')




