from django.contrib import admin
from .models import *


class GroupsAdmin(admin.ModelAdmin):
    model = Loan
    list_display = ('GroupName', 'User',)

class LoanAdmin(admin.ModelAdmin):
    model = Loan
    list_display = ('User','Time','LoanTaken','Amount','EMIMonth','EMIAmount','Paid','Proof',)

class FoodAdmin(admin.ModelAdmin):
    model = Loan
    list_display = ('User','ParterName','Time','Amount','Paidby','Proof',)

class TravelAdmin(admin.ModelAdmin):
    model = Travel
    list_display = ('User','TravelledIn','Time','Amount','Proof',)

class RentandUtilitiesAdmin(admin.ModelAdmin):
    model = RentandUtilities
    list_display = ('User','Category','PaidTo','Time','Amount','Proof',)

class ShoppingAdmin(admin.ModelAdmin):
    model = Shopping
    list_display = ('User','ItemName','PurchasedFrom','Time','Amount','Proof',)

class MedicalAdmin(admin.ModelAdmin):
    model = Medical
    list_display = ('User','HospitalName','DiseaseName','Prescription','Time','Amount','Proof',)

class UserProfileAdmin(admin.ModelAdmin):
    model = UserProfile
    list_display = ('User','ProfilePic',)

class SupportAdmin(admin.ModelAdmin):
    model = Support
    list_display = ('User','IssueType','Description','Status','Comment',)

class ThresholdsAdmin(admin.ModelAdmin):
    model = Thresholds
    list_display = ('User', 'FoodLimit', 'TravelLimit', 'RentandUtilitiesLimit','ShoppingLimit', 'MedicalLimit', 'OtherExpensesLimit',)

admin.site.register(Groups, GroupsAdmin)
admin.site.register(Thresholds, ThresholdsAdmin)
admin.site.register(Loan,LoanAdmin)
admin.site.register(Food, FoodAdmin)
admin.site.register(Travel,TravelAdmin)
admin.site.register(RentandUtilities,RentandUtilitiesAdmin)
admin.site.register(Shopping,ShoppingAdmin)
admin.site.register(Medical,MedicalAdmin)
admin.site.register(UserProfile,UserProfileAdmin)
admin.site.register(Support,SupportAdmin)
