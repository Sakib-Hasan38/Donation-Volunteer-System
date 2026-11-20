"""
URL configuration for donation project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from app.forms import MyPasswordResetForm, MySetPasswordForm


urlpatterns = [

    path("admin/", admin.site.urls),
    path("", views.index, name="index"),
    path("gallery/", views.gallery, name="gallery"),
    path("login-admin/", views.login_admin.as_view(), name="login_admin"),
    path("login-donar/", views.login_donar.as_view(), name="login_donar"),
    path("login-volunteer/", views.login_volunteer.as_view(), name="login_volunteer"),
    path("signup-donar/", views.signup_donar.as_view(), name="signup_donar"),
    path("signup-volunteer/", views.signup_volunteer.as_view(), name="signup_volunteer"),
    path("index-admin/", views.index_admin, name="index_admin"),

    path("password-reset/",auth_views.PasswordResetView.as_view(template_name='password_reset.html',form_class=MyPasswordResetForm), name="password_reset"),
    path("password-reset-done/",auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name="password_reset_done"),
    path("password-reset-confirm/<uidb64>/<token>/",auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html',form_class=MySetPasswordForm), name="password_reset_confirm"),
    path("password-reset-complete/",auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name="password_reset_complete"),


    # admin dashboard
    path("pending-donation/", views.pending_donation, name="pending_donation"),
    path("accepted-donation/", views.accepted_donation, name="accepted_donation"),
    path("rejected-donation/", views.rejected_donation, name="rejected-donation"),
    path(
        "volunteerallocated-donation/",
        views.volunteerallocated_donation,
        name="volunteerallocated_donation"
    ),
    path("donationrec-admin/", views.donationrec_admin, name="donationrec_admin"),
    path(
        "donationnotrec-admin/", views.donationnotrec_admin, name="donationnotrec_admin"
    ),
    path(
        "donationdelivered-admin/",
        views.donationdelivered_admin,
        name="donationdelivered_admin",
    ),
    path("all-donations/", views.all_donations, name="all_donations"),
    path("manage-donar/", views.manage_donar, name="manage_donar"),
    path("new-volunteer/", views.new_volunteer, name="new_volunteer"),
    path("accepted-volunteer/", views.accepted_volunteer, name="accepted_volunteer"),
    path("rejected-volunteer/", views.rejected_volunteer, name="rejected_volunteer"),
    path("all-volunteer/", views.all_volunteer, name="all-volunteer"),
    path("add-area/", views.add_area.as_view(), name="add_area"),
    path("edit-area/<int:pid>", views.edit_area.as_view(), name="edit-area"),
    path("manage-area/", views.manage_area, name="manage_area"),
    path("changepwd-admin/", views.changepwd_admin.as_view(), name="changepwd_admin"),
    path("logout/", views.logout, name="logout"),

    path("manage-payment/", views.manage_payment, name="manage_payment"),
    path("payment-detail-admin/<int:pid>", views.payment_detail_admin, name="payment_detail_admin"),
    
    
    # view details
    path(
        "accepted-donationdetail/<int:pid>",
        views.accepted_donationdetail.as_view(),
        name="accepted_donationdetail",
    ),
    path(
        "view-volunteerdetail/<int:pid>",
        views.view_volunteerdetail.as_view(),
        name="view-volunteerdetail",
    ),
    path("view-donardetail/<int:pid>", views.view_donardetail, name="view_donardetail"),
    path(
        "view-donationdetail/<int:pid>",
        views.view_donationdetail.as_view(),
        name="view_donationdetail",
    ),


    # donar dashboard
    path("index-donar/", views.index_donar, name="index-donar"),
    path("donate-now/", views.donate_now.as_view(), name="donate-now"),
    path("donation-history/", views.donation_history, name="donation-history"),
    path("payment-history/", views.payment_history, name="payment-history"),
    path("payment-detail/<int:pid>", views.payment_detail, name="payment_detail"),
    path("profile-donar/", views.profile_donar.as_view(), name="profile-donar"),
    path("changepwd-donar/", views.changepwd_donar.as_view(), name="changepwd-donar"),

    

    # volunteer dashboard
    path("index-volunteer/", views.index_volunteer, name="index-volunteer"),
    path("collection-req/", views.collection_req, name="collection-req"),
    path(
        "donationrec-volunteer/",
        views.donationrec_volunteer,
        name="donationrec-volunteer",
    ),
    path(
        "donationnotrec-volunteer/",
        views.donationnotrec_volunteer,
        name="donationnotrec-volunteer",
    ),
    path(
        "donationdelivered-volunteer/",
        views.donationdelivered_volunteer,
        name="donationdelivered-volunteer",
    ),
    path("profile-volunteer/", views.profile_volunteer.as_view(), name="profile-volunteer"),
    path("changepwd-volunteer/", views.changepwd_volunteer.as_view(), name="changepwd-volunteer"),
    # vew details
    path(
        "donationdetail-donar/<int:pid>",
        views.donationdetail_donar,
        name="donationdetail-donar",
    ),
    path(
        "donationrec-detail/<int:pid>",
        views.donationrec_detail.as_view(),
        name="donationrec-detail",
    ),
    path(
        "donationcollection-detail/<int:pid>",
        views.donationcollection_detail.as_view(),
        name="donationcollection-detail",
    ),
    path('delete_donation/<int:pid>',views.delete_donation, name='delete_donation'),
    path('delete_volunteer/<int:pid>',views.delete_volunteer, name='delete_volunteer'),
    path('delete_area/<int:pid>',views.delete_area, name='delete_area'),
    path('delete_donar/<int:pid>',views.delete_donar, name='delete_donar'),


    path('admin-delete_payment/<int:pid>',views.delete_payment_admin, name='delete_payment_admin'),
    path('donar-delete_payment/<int:pid>',views.delete_payment, name='donar_delete_payment'),

    
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

