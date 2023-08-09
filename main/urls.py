from django.urls import path, include
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView, PasswordChangeView, PasswordChangeDoneView
from .views import *


urlpatterns = [
    path('', index, name='index'),
    path('login/',login_page,name='login'),
    path('logout/', logoutUser, name="logout"),
    path("register/", registerUser, name="register"),

    path('NewGroups/', NewGroupsView, name='NewGroups'),
    path('ManageGroups/', ManageGroupsView, name='ManageGroups'),

    path('Profile-Update/',UserprofileView, name="Profile-Update"),
    path('Notifications/',NotificationsView, name="Notifications"),
    path('Support/',SupportView, name='Support'),
    path('Loans/', LoansView, name='Loans'),
    path('LoanAddProof/<int:id>/', LoanAddProof, name='LoanAddProof'),
    path('Food/', FoodView, name='Food'),
    path('FoodAddProof/<int:id>/', FoodAddProof, name='FoodAddProof'),
    path('RentandUtilities/', RentandUtilitiesView, name='RentandUtilities'),
    path('RentandUtilitiesAddProof/<int:id>/', RentandUtilitiesAddProof, name='RentandUtilitiesAddProof'),
    path('Medical/', MedicalView, name='Medical'),
    path('MedicalAddProof/<int:id>/', MedicalAddProof, name='MedicalAddProof'),
    path('OtherExpenses/', OtherExpensesView, name='OtherExpenses'),
    path('OtherExpensesAddProof/<int:id>/', OtherExpensesAddProof, name='OtherExpensesAddProof'),
    path('Travel/', TravelView , name='Travel'),
    path('TravelAddProof/<int:id>/', TravelAddProof, name='TravelAddProof'),
    path('SalaryCredited/', SalaryCreditedView, name='SalaryCredited'),
    path('Savings/', SavingsView, name='Savings'),
    path('Settings/', SettingsView, name='Settings'),
    path('Shopping/', ShoppingView, name='Shopping'),
    path('ShoppingAddProof/<int:id>/', ShoppingAddProof, name='ShoppingAddProof'),
    path('SalaryCredited/', SalaryCreditedView, name='SalaryCredited'),
    path('SalaryCreditedAddProof/<int:id>/', SalaryCreditedAddProof, name='SalaryCreditedAddProof'),
    path('Investments/', InvestmentsView, name='Investments'),

    path('password-reset/', PasswordResetView.as_view(template_name="account/password_reset.html", email_template_name="account/password_reset_email.html"), name='password-reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(template_name="account/password_reset_done.html"), name='password-reset-done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name="account/password_reset_confirm.html"), name='password-reset-confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(template_name="account/password_reset_complete.html"), name='password-reset-complete'),

    path('password-change/', PasswordChangeView.as_view(template_name="account/password_change.html"), name='password-change'),
    path('password_change/done/', PasswordChangeDoneView.as_view(template_name="account/password_change_done.html"), name='password-change-done'),
    path('', include('django.contrib.auth.urls')),
    path('DeleteItem/<int:id>/<str:model>/', DeleteItem, name='DeleteItem')
]
