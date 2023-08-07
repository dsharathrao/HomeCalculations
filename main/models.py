from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.


class UserProfile(models.Model):
    User = models.ForeignKey(get_user_model(), null=True, on_delete=models.CASCADE)
    ProfilePic = models.ImageField(upload_to='UserProfilePics/', default='default.png')
    def __str__(self):
        return str(self.id)
    class Meta:
        verbose_name_plural="User Profiles"

Support_CHOICES = (
    ('new','NEW'),
    ('resolved', 'RESOLVED'),
    ('inprogress','INPROGRESS'),
    ('cancelled','CANCELLED'),
    ('closed','CLOSED'),
)


class Groups(models.Model):
    User = models.ForeignKey(get_user_model(), null=True, on_delete=models.CASCADE, related_name='+')
    GroupName = models.CharField(max_length=100,blank=False,null=False)
    OtherUsers = models.ManyToManyField(get_user_model(), related_name="+")

    def __str__(self):
        return str(self.id)
    class Meta:
        verbose_name_plural="Groups"


class Support(models.Model):
    User = models.ForeignKey(get_user_model(), null=True, on_delete=models.CASCADE)
    Time = models.DateTimeField(auto_now=True)
    IssueType = models.CharField(max_length=100,blank=False,null=False)
    Description = models.CharField(max_length=100,blank=False,null=False)
    Status = models.CharField(max_length=100, choices=Support_CHOICES, default='new')
    Comment = models.CharField(max_length=1000,blank=False,null=False)
    def __str__(self):
        return str(self.id)
    class Meta:
        verbose_name_plural="Support Section"

class Loan(models.Model):
    User = models.ForeignKey(get_user_model(), null=True, on_delete=models.CASCADE)
    Time = models.DateField(auto_now_add=True, blank=True)
    LoanTaken = models.CharField(max_length=100,blank=False,null=False)
    Amount = models.IntegerField()
    EMIMonth = models.CharField(max_length=100,blank=True,null=True)
    EMIAmount = models.IntegerField()
    Paid = models.BooleanField()
    Proof = models.FileField(upload_to='Loans/%Y/%m/%d', blank=True, null=True)

    def __str__(self):
        return str(self.id)
    class Meta:
        verbose_name_plural="Loans"

class Food(models.Model):
    User = models.ForeignKey(get_user_model(), null=True, on_delete=models.CASCADE)
    ParterName = models.CharField(max_length=100, blank=False, null=False)
    Time = models.DateField(blank=True, null=True)
    Amount = models.IntegerField()
    Paidby = models.CharField(max_length=100, blank=True, null=True)
    Proof = models.FileField(upload_to='FoodData/%Y/%m/%d', blank=True, null=True)

    def __str__(self) -> str:
        return str(self.id)
    class Meta:
        verbose_name_plural = "Food"

class Travel(models.Model):
    User = models.ForeignKey(get_user_model(), null=True, on_delete=models.CASCADE)
    TravelledIn = models.CharField(max_length=100, blank=False, null=False)
    Time = models.DateField(blank=True, null=True)
    Amount = models.IntegerField()
    Proof = models.FileField(upload_to='Travels/%Y/%m/%d', blank=True, null=True)

    def __str__(self) -> str:
        return str(self.id)
    class Meta:
        verbose_name_plural = "Travels"

class RentandUtilities(models.Model):
    User = models.ForeignKey(get_user_model(), null=True, on_delete=models.CASCADE)
    Category = models.CharField(max_length=100, blank=False, null=False)
    PaidTo = models.CharField(max_length=100, blank=True, null=True)
    Time = models.DateField(blank=True, null=True)
    Amount = models.IntegerField()
    Proof = models.FileField(upload_to='RentUtilities/%Y/%m/%d', blank=True, null=True)

    def __str__(self) -> str:
        return str(self.id)
    class Meta:
        verbose_name_plural = "Rent & Utilities"

class Shopping(models.Model):
    User = models.ForeignKey(get_user_model(), null=True, on_delete=models.CASCADE)
    ItemName = models.CharField(max_length=100, blank=False, null=False)
    PurchasedFrom = models.CharField(max_length=100, blank=True, null=True)
    Time = models.DateField(blank=True, null=True)
    Amount = models.IntegerField()
    Proof = models.FileField(upload_to='Shopping/%Y/%m/%d', blank=True, null=True)

    def __str__(self) -> str:
        return str(self.id)
    class Meta:
        verbose_name_plural = "Shopping"

class Medical(models.Model):
    User = models.ForeignKey(get_user_model(), null=True, on_delete=models.CASCADE)
    HospitalName = models.CharField(max_length=100, blank=False, null=False)
    DiseaseName = models.CharField(max_length=100, blank=True, null=True)
    Prescription = models.FileField(upload_to='Medical/Prescription/%Y/%m/%d', blank=True, null=True)
    Time = models.DateField(blank=True, null=True)
    Amount = models.IntegerField()
    Proof = models.FileField(upload_to='Medical/Bills/%Y/%m/%d', blank=True, null=True)

    def __str__(self) -> str:
        return str(self.id)
    class Meta:
        verbose_name_plural = "Medical"

class OtherExpenses(models.Model):
    User = models.ForeignKey(get_user_model(), null=True, on_delete=models.CASCADE)
    Name = models.CharField(max_length=100, blank=False, null=False)
    Time = models.DateField(blank=True, null=True)
    Amount = models.IntegerField()
    Proof = models.FileField(upload_to='OtherExpenses/%Y/%m/%d', blank=True, null=True)

    def __str__(self) -> str:
        return str(self.id)
    class Meta:
        verbose_name_plural = "OtherExpenses"

class SalaryCredited(models.Model):
    User = models.ForeignKey(get_user_model(), null=True, on_delete=models.CASCADE)
    Time = models.DateField(blank=True, null=True)
    Amount = models.IntegerField()
    Proof = models.FileField(upload_to='SalaryCredited/%Y/%m/%d', blank=True, null=True)

    def __str__(self) -> str:
        return str(self.id)
    class Meta:
        verbose_name_plural = "Salary Credited"

class Thresholds(models.Model):
    User = models.ForeignKey(get_user_model(), null=True, on_delete=models.CASCADE)
    FoodLimit = models.IntegerField(default=0)
    TravelLimit = models.IntegerField(default=0)
    RentandUtilitiesLimit = models.IntegerField(default=0)
    ShoppingLimit = models.IntegerField(default=0)
    MedicalLimit = models.IntegerField(default=0)
    OtherExpensesLimit = models.IntegerField(default=0)
    def __str__(self) -> str:
        return str(self.id)
    class Meta:
        verbose_name_plural = "User Thresholds"
