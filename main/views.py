from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.apps import apps
from .models import *
from django.db.models import Sum
from .forms import CustomUserCreationForm
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
import numpy as np
import json



def login_page(request):
    message = ''
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'account/login.html')

def logoutUser(request):
    logout(request)
    messages.error(request, "See you again!")
    return redirect('login')

def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            # print(user)
            UserProfile.objects.create(User=user)
            Thresholds.objects.create(User=user)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, 'Welcome to Our platform! Please update your Profile!!!!')
                    return redirect('/Profile-Update/')
        else:
            messages.error(request, 'Invalid your registration... Please try again')
    context = {'form': form, 'page': page}
    return render(request, 'account/register.html', context)

@login_required(login_url='login')
def UserprofileView(request):
    username = User.objects.get(username=request.user.username)
    if request.method == "POST":
        if request.POST.get("form_type") == 'formOne':
            try:
                ProfilePic = request.FILES.get('ProfilePic')
                ProfileObj = UserProfile.objects.get(User=username)
                ProfileObj.ProfilePic = ProfilePic
                ProfileObj.save()
                
                #UserProfile.objects.create(User=username,ProfilePic=ProfilePic)
                messages.success(request, 'Your Profile was Updated')

            except:
                # print(traceback.format_exc())
                messages.error(request,'Unable to update your Profile. Please try again!')
        elif request.POST.get("form_type") == 'formTwo':
            try:
                Food = request.POST['Food']
                Travel = request.POST['Travel']
                RentandUtilities = request.POST['RentandUtilities']
                Shopping = request.POST['Shopping']
                Medical = request.POST['Medical']
                OtherExpenses = request.POST['OtherExpenses']
                ThresholdsData = Thresholds.objects.get(User=username)
                ThresholdsData.FoodLimit = Food
                ThresholdsData.TravelLimit = Travel
                ThresholdsData.RentandUtilitiesLimit = RentandUtilities
                ThresholdsData.ShoppingLimit = Shopping
                ThresholdsData.MedicalLimit = Medical
                ThresholdsData.OtherExpensesLimit = OtherExpenses
                ThresholdsData.save()
                messages.success(request, 'Your Thresholds was Updated')
            except:
                # print(traceback.format_exc())
                messages.error(request,'Unable to update Thresholds. Please try again!')

    ProfileObj = UserProfile.objects.get(User=username)
    avatar = ProfileObj.ProfilePic.url
    ThresholdsData = Thresholds.objects.get(User=username)
    # print(ThresholdsData.FoodLimit)
    context = {
        'avatar':avatar,
        'ThresholdsData':ThresholdsData
    }
    return render(request, 'account/profile.html',context=context)


@login_required(login_url='login')
def DeleteItem(request,id, model):
    modeldata = apps.get_model('main', model)
    data = modeldata.objects.get(id=id)
    try:
        data.delete()
        messages.warning(request, 'Deleted Sucessfully!!!')
    except:
        messages.error(request, 'Unable to delete Please try again')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def monthwisehelper(data):
    if len(data) != 0:
        for i in data:
            month = str(datetime.strftime(i['month'], '%m-%Y'))
            i['month'] = month
    return data

def month_wise_fetch_helper(username, now,Modelname):
    modeldata = apps.get_model('main', Modelname)
    try:
        totalexpense = modeldata.objects.filter(User=username,Time__year=now.year,Time__month=now.month).aggregate(total_expense=Sum('Amount'))
        if totalexpense['total_expense'] == None:
            totalexpense['total_expense'] = 0
    except:
        totalexpense = {'total_expense': 0}
    totalexpense['ExpenseName'] = Modelname
    totalexpense['Month'] = now.strftime('%Y-%m')
    return totalexpense

def percentage_change(col1,col2):
    return ((col2.sub(col1)).div(col1)).mul(100)

#Dashboard or Index Page
@login_required(login_url='login')
def index(request):
    ThisMonthwiseData = []
    LastMonthwiseData = []
    username = User.objects.get(username=request.user.username)
    ListModels = ['Food','Travel','RentandUtilities','Shopping','Medical','OtherExpenses']
    thismonth = datetime.now()
    for Modelname in ListModels:
        ThisMonthwiseData.append(month_wise_fetch_helper(username,thismonth,Modelname))
    df = pd.DataFrame(ThisMonthwiseData)
    # df = df.fillna('No data Found')
    #df = df.explode('data', ignore_index=True)

    # now fill the NaN with an empty dict
    # df.freshness_grades = df.data.fillna({i: {} for i in df.index})

    # # then normalize the column
    # df = df.join(pd.json_normalize(df.pop('data')))
    # lastmonth = datetime.now() - relativedelta(months=1)
    # for Modelname in ListModels:
    #     LastMonthwiseData.append(month_wise_fetch_helper(lastmonth,Modelname))
    # df2 = pd.DataFrame(LastMonthwiseData)
    #df['Lastmonth_expense'] = df2['total_expense']
    ThresholdsData = list(Thresholds.objects.filter(User=username).values_list('FoodLimit', 'TravelLimit','RentandUtilitiesLimit', 'ShoppingLimit', 'MedicalLimit','OtherExpensesLimit'))
    df2 = pd.DataFrame(ThresholdsData, columns=['Food', 'Travel', 'RentandUtilities','Shopping', 'Medical', 'OtherExpenses'])
    df2 = df2.rename_axis(index=None, columns='ExpenseName').T.reset_index()
    df2 = df2.rename_axis(index=None)
    df['Thershold'] = df2[df2.columns[1]]
    df = df.fillna(0)
    df['Percentage'] = percentage_change(df['Thershold'],df['total_expense'])
    df = df.fillna(0)
    df.replace([np.inf, -np.inf], 0, inplace=True)
    # print(df)
    json_records = df.reset_index().to_json(orient ='records')
    ThisMonthwiseData = []
    ThisMonthwiseData = json.loads(json_records)
    ThismonthdataCompare = {}
    for i in range(len(ListModels)):
        ThismonthdataCompare[ListModels[i]] = ThisMonthwiseData[i]['total_expense']
    ThersholdMeetPercentage = {}
    for i in range(len(ListModels)):
        ThersholdMeetPercentage[ListModels[i]] = ThisMonthwiseData[i]['Percentage']
    # print(ThersholdMeetPercentage)
    context = {
        'Username' : username,
        'MonthwiseDataFrame':ThisMonthwiseData,
        'ThismonthdataCompare':ThismonthdataCompare,
        'ThersholdMeetPercentage':ThersholdMeetPercentage
    }
    return render(request, 'index.html', context=context)

#Loans taken and paid Page

@login_required(login_url='login')
def LoansView(request):
    model = 'Loan'
    username = User.objects.get(username=request.user.username)
    if request.method == "POST":
        try:
            Loantaken = request.POST['Loantaken']
            Amount = request.POST['Amount']
            EMIMonths = request.POST['EMIMonths']
            EMIAmount = request.POST['EMIAmount']
            EMIMonths = int(EMIMonths)
            ThisMonth = request.POST.get('thismonth', '') == 'on'
            EMIStart = request.POST['EMIStart']
            datem = datetime.strptime(EMIStart, "%Y-%m-%d")
            if ThisMonth:
                val = 0
            else:
                val = 1
            Months = []
            for i in range(val,int(EMIMonths)+1):
                Add_months = datem + relativedelta(months=i)
                Add_months = Add_months.strftime('%Y-%m')
                Months.append(Add_months)
            for i in Months:
                Loan.objects.create(User=username,LoanTaken=Loantaken,Amount=Amount, EMIMonth= i,EMIAmount=EMIAmount,Paid=False)
            messages.success(request, 'New Loan Added')
        except Exception as e:
            # print(traceback.format_exc())
            messages.error(request, "Something went wrong! Please check the logs")
    LoanData = Loan.objects.filter(User=username.id)
    context = {
        'model' : model,
        'LoanData' : LoanData
    }   
    return render(request, 'Loans.html', context=context)

@login_required(login_url='login')
def LoanAddProof(request, id):
    UpdateColValue = Loan.objects.get(id=id)
    if request.method == "POST":
        try:
            Paid = request.POST.get('Paid')
            EMIAmount = request.POST.get('EMIAmount')
            Proof = request.FILES.get('ProofAttachment')
            
            if Paid == 'Yes':
                Paid = True
            else:
                Paid = False
            # print(EMIAmount)
            # print(Paid)
            # print(Proof)
            #Loan.objects.filter(pk=id).update(EMIAmount=EMIAmount, Paid=Paid, Proof=Proof)
            LoanObj = Loan.objects.get(id=id)
            LoanObj.EMIAmount = EMIAmount
            LoanObj.Paid = Paid
            if bool(request.FILES.get('ProofAttachment', False)) == True:
                LoanObj.Proof = Proof
            LoanObj.save()
            messages.success(request, 'Updated Successfully')
            return redirect('/Loans/')
        except Exception as e:
            # print(traceback.format_exc())
            messages.error(request, "Something went wrong! Update Failed.")
            return redirect('/Loans')
        
    context = {
        'UpdateColValue': UpdateColValue
    }
    return render(request, 'LoanAddProof.html',context = context)
    

#For food expanses
@login_required(login_url='login')
def FoodView(request):
    model = 'Food'
    username = User.objects.get(username=request.user.username)
    if request.method == "POST":
        try:
            ParterName = request.POST['ParterName']
            Time = request.POST['Time']
            Amount = request.POST['Amount']
            Paidby = request.POST['Paidby']
            Proof = request.FILES.get('Proof')
            Food.objects.create(User=username,ParterName=ParterName,Time=Time,Amount=Amount,Paidby= Paidby,Proof=Proof)
            messages.success(request, 'New Food expense Added')
        except Exception:
            # print(traceback.format_exc())
            messages.error(request, "Something went wrong! Please check the logs")
    FoodData = Food.objects.filter(User=username.id)
    context = {
        'model' : model,
        'FoodData' : FoodData
    }
    return render(request, 'Food.html', context=context)

@login_required(login_url='login')
def FoodAddProof(request, id):
    UpdateColValue = Food.objects.get(id=id)
    if request.method == "POST":
        try:
            ParterName = request.POST.get('ParterName')
            Time = request.POST.get('Time')
            Amount = request.POST.get('Amount')
            Proof = request.FILES.get('ProofAttachment')
            FoodObj = Food.objects.get(id=id)
            FoodObj.ParterName = ParterName
            FoodObj.Time = Time
            FoodObj.Amount = Amount
            if bool(request.FILES.get('ProofAttachment', False)) == True:
                FoodObj.Proof = Proof
            FoodObj.save()
            messages.success(request, 'Updated Successfully')
            return redirect('/Food/')
        except Exception as e:
            # print(traceback.format_exc())
            messages.error(request, "Something went wrong! Update Failed.")
            return redirect('/Food')
        
    context = {
        'UpdateColValue': UpdateColValue
    }
    return render(request, 'FoodAddProof.html',context = context)
    

#For Travel Expenses
@login_required(login_url='login')
def TravelView(request):
    model = 'Travel'
    username = User.objects.get(username=request.user.username)
    if request.method == "POST":
        try:
            TravelledIn = request.POST['TravelledIn']
            Time = request.POST['Time']
            Amount = request.POST['Amount']
            Proof = request.FILES.get('Proof')
            
            Travel.objects.create(User=username,TravelledIn=TravelledIn,Time=Time,Amount=Amount,Proof=Proof)
            messages.success(request, 'New Travel expense Added')
        except Exception:
            # print(traceback.format_exc())
            messages.error(request, "Something went wrong! Please check the logs")
    TravelData = Travel.objects.filter(User=username.id)
    context = {
        'model' : model,
        'TravelData' : TravelData
    }
    return render(request, 'Travel.html', context=context)

@login_required(login_url='login')
def TravelAddProof(request, id):
    UpdateColValue = Travel.objects.get(id=id)
    if request.method == "POST":
        try:
            TravelledIn = request.POST.get('TravelledIn')
            Time = request.POST.get('Time')
            Amount = request.POST.get('Amount')
            Proof = request.FILES.get('ProofAttachment')
            TravelObj = Travel.objects.get(id=id)
            TravelObj.TravelledIn = TravelledIn
            TravelObj.Time = Time
            TravelObj.Amount = Amount
            if bool(request.FILES.get('ProofAttachment', False)) == True:
                TravelObj.Proof = Proof
            TravelObj.save()
            messages.success(request, 'Updated Successfully')
            return redirect('/Travel/')
        except Exception as e:
            # print(traceback.format_exc())
            messages.error(request, "Something went wrong! Update Failed.")
            return redirect('/Travel')
        
    context = {
        'UpdateColValue': UpdateColValue
    }
    return render(request, 'TravelAddProof.html',context = context)


#For HomeExpanses expanses
@login_required(login_url='login')
def RentandUtilitiesView(request):
    model = 'RentandUtilities'
    username = User.objects.get(username=request.user.username)
    if request.method == "POST":
        try:
            Category = request.POST['Category']
            PaidTo = request.POST['PaidTo']
            Time = request.POST['Time']
            Amount = request.POST['Amount']
            Proof = request.FILES.get('Proof')
            RentandUtilities.objects.create(User=username,Category=Category,PaidTo=PaidTo, Time=Time,Amount=Amount,Proof=Proof)
            messages.success(request, 'New Home expense Added')
        except Exception:
            # print(traceback.format_exc())
            messages.error(request, "Something went wrong! Please check the logs")
    RentandUtilitiesData = RentandUtilities.objects.filter(User=username.id)
    context = {
        'model' : model,
        'RentandUtilitiesData' : RentandUtilitiesData
    }
    return render(request, 'RentandUtilities.html', context=context)

@login_required(login_url='login')
def RentandUtilitiesAddProof(request, id):
    UpdateColValue = RentandUtilities.objects.get(id=id)
    if request.method == "POST":
        try:
            Category = request.POST.get('Category')
            PaidTo = request.POST.get('PaidTo')
            Time = request.POST.get('Time')
            Amount = request.POST.get('Amount')
            Proof = request.FILES.get('ProofAttachment')
            RentandUtilitiesObj = RentandUtilities.objects.get(id=id)
            RentandUtilitiesObj.Category = Category
            RentandUtilitiesObj.PaidTo = PaidTo
            RentandUtilitiesObj.Time = Time
            RentandUtilitiesObj.Amount = Amount
            if bool(request.FILES.get('ProofAttachment', False)) == True:
                RentandUtilitiesObj.Proof = Proof
            RentandUtilitiesObj.save()
            messages.success(request, 'Updated Successfully')
            return redirect('/RentandUtilities/')
        except Exception as e:
            # print(traceback.format_exc())
            messages.error(request, "Something went wrong! Update Failed.")
            return redirect('/RentandUtilities/')
        
    context = {
        'UpdateColValue': UpdateColValue
    }
    return render(request, 'RentandUtilitiesAddProof.html',context = context)


#Shopping
@login_required(login_url='login')
def ShoppingView(request):
    model = 'Shopping'
    username = User.objects.get(username=request.user.username)
    if request.method == "POST":
        try:
            ItemName = request.POST['ItemName']
            PurchasedFrom = request.POST['PurchasedFrom']
            Time = request.POST['Time']
            Amount = request.POST['Amount']
            Proof = request.FILES.get('Proof')
            Shopping.objects.create(User=username,ItemName=ItemName,PurchasedFrom=PurchasedFrom, Time=Time,Amount=Amount,Proof=Proof)
            messages.success(request, 'New Shopping expense Added')
        except Exception:
            # print(traceback.format_exc())
            messages.error(request, "Something went wrong! Please check the logs")
    ShoppingData = Shopping.objects.filter(User=username.id)
    context = {
        'model' : model,
        'ShoppingData' : ShoppingData
    }
    return render(request, 'Shopping.html', context=context)

@login_required(login_url='login')
def ShoppingAddProof(request, id):
    UpdateColValue = Shopping.objects.get(id=id)
    if request.method == "POST":
        try:
            ItemName = request.POST.get('ItemName')
            PurchasedFrom = request.POST.get('PurchasedFrom')
            Time = request.POST.get('Time')
            Amount = request.POST.get('Amount')
            Proof = request.FILES.get('ProofAttachment')
            ShoppingObj = Shopping.objects.get(id=id)
            ShoppingObj.ItemName = ItemName
            ShoppingObj.PurchasedFrom = PurchasedFrom
            ShoppingObj.Time = Time
            ShoppingObj.Amount = Amount
            if bool(request.FILES.get('ProofAttachment', False)) == True:
                ShoppingObj.Proof = Proof
            ShoppingObj.save()
            messages.success(request, 'Updated Successfully')
            return redirect('/Shopping/')
        except Exception as e:
            # print(traceback.format_exc())
            messages.error(request, "Something went wrong! Update Failed.")
            return redirect('/Shopping/')
        
    context = {
        'UpdateColValue': UpdateColValue
    }
    return render(request, 'ShoppingAddProof.html',context = context)

#For Hospitalized and Medical Expanses
@login_required(login_url='login')
def MedicalView(request):
    model = 'Medical'
    username = User.objects.get(username=request.user.username)
    if request.method == "POST":
        try:
            HospitalName = request.POST['HospitalName']
            DiseaseName = request.POST['DiseaseName']
            Prescription = request.FILES.get('Prescription')
            Time = request.POST['Time']
            Amount = request.POST['Amount']
            Proof = request.FILES.get('Proof')
            Medical.objects.create(User=username,HospitalName=HospitalName,DiseaseName=DiseaseName,Prescription=Prescription, Time=Time,Amount=Amount,Proof=Proof)
            messages.success(request, 'New Medical expense Added')
        except Exception:
            # print(traceback.format_exc())
            messages.error(request, "Something went wrong! Please check the logs")
    MedicalData = Medical.objects.filter(User=username.id)
    context = {
        'model' : model,
        'MedicalData' : MedicalData
    }
    return render(request, 'Medical.html', context=context)

@login_required(login_url='login')
def MedicalAddProof(request, id):
    UpdateColValue = Medical.objects.get(id=id)
    if request.method == "POST":
        try:
            HospitalName = request.POST.get('HospitalName')
            DiseaseName = request.POST.get('DiseaseName')
            Time = request.POST.get('Time')
            Amount = request.POST.get('Amount')
            Prescription = request.FILES.get('Prescription')
            Proof = request.FILES.get('ProofAttachment')
            MedicalObj = Medical.objects.get(id=id)
            MedicalObj.HospitalName = HospitalName
            MedicalObj.DiseaseName = DiseaseName
            MedicalObj.Time = Time
            MedicalObj.Amount = Amount
            if bool(request.FILES.get('Prescription', False)) == True:
                MedicalObj.Prescription = Prescription
            if bool(request.FILES.get('ProofAttachment', False)) == True:
                MedicalObj.Proof = Proof
            MedicalObj.save()
            messages.success(request, 'Updated Successfully')
            return redirect('/Medical/')
        except Exception as e:
            # print(traceback.format_exc())
            messages.error(request, "Something went wrong! Update Failed.")
            return redirect('/Medical/')
        
    context = {
        'UpdateColValue': UpdateColValue
    }
    return render(request, 'MedicalAddProof.html',context = context)


#For Electronics purshases Page
@login_required(login_url='login')
def OtherExpensesView(request):
    model = 'OtherExpenses'
    username = User.objects.get(username=request.user.username)
    if request.method == "POST":
        try:
            Name = request.POST['Name']
            Time = request.POST['Time']
            Amount = request.POST['Amount']
            Proof = request.FILES.get('Proof')
            OtherExpenses.objects.create(User=username,Name=Name, Time=Time,Amount=Amount,Proof=Proof)
            messages.success(request, 'New OtherExpenses Added')
        except Exception:
            # print(traceback.format_exc())
            messages.error(request, "Something went wrong! Please check the logs")
    OtherExpensesData = OtherExpenses.objects.filter(User=username.id)
    context = {
        'model' : model,
        'OtherExpensesData' : OtherExpensesData
    }
    return render(request, 'OtherExpenses.html', context=context)


@login_required(login_url='login')
def OtherExpensesAddProof(request, id):
    UpdateColValue = OtherExpenses.objects.get(id=id)
    if request.method == "POST":
        try:
            Name = request.POST.get('Name')
            Time = request.POST.get('Time')
            Amount = request.POST.get('Amount')
            Proof = request.FILES.get('ProofAttachment')
            OtherExpensesObj = OtherExpenses.objects.get(id=id)
            OtherExpensesObj.Name = Name
            OtherExpensesObj.Time = Time
            OtherExpensesObj.Amount = Amount
            if bool(request.FILES.get('ProofAttachment', False)) == True:
                OtherExpensesObj.Proof = Proof
            OtherExpensesObj.save()
            messages.success(request, 'Updated Successfully')
            return redirect('/OtherExpenses/')
        except Exception as e:
            # print(traceback.format_exc())
            messages.error(request, "Something went wrong! Update Failed.")
            return redirect('/OtherExpenses/')
        
    context = {
        'UpdateColValue': UpdateColValue
    }
    return render(request, 'OtherExpensesAddProof.html',context = context)



#How much got monthly
@login_required(login_url='login')
def SalaryCreditedView(request):
    model = 'SalaryCredited'
    username = User.objects.get(username=request.user.username)
    if request.method == "POST":
        try:
            Time = request.POST['Time']
            Amount = request.POST['Amount']
            Proof = request.FILES.get('Proof')
            SalaryCredited.objects.create(User=username, Time=Time,Amount=Amount,Proof=Proof)
            messages.success(request, 'Salary Added')
        except Exception:
            # print(traceback.format_exc())
            messages.error(request, "Something went wrong! Please check the logs")
    SalaryCreditedData = SalaryCredited.objects.filter(User=username.id)
    context = {
        'model' : model,
        'SalaryCreditedData' : SalaryCreditedData
    }
    return render(request, 'SalaryCredited.html', context=context)

@login_required(login_url='login')
def SalaryCreditedAddProof(request, id):
    UpdateColValue = SalaryCredited.objects.get(id=id)
    if request.method == "POST":
        try:
            Time = request.POST.get('Time')
            Amount = request.POST.get('Amount')
            Proof = request.FILES.get('ProofAttachment')
            OtherExpensesObj = SalaryCredited.objects.get(id=id)
            OtherExpensesObj.Time = Time
            OtherExpensesObj.Amount = Amount
            if bool(request.FILES.get('ProofAttachment', False)) == True:
                OtherExpensesObj.Proof = Proof
            OtherExpensesObj.save()
            messages.success(request, 'Updated Successfully')
            return redirect('/SalaryCredited/')
        except Exception as e:
            # print(traceback.format_exc())
            messages.error(request, "Something went wrong! Update Failed.")
            return redirect('/SalaryCredited/')
        
    context = {
        'UpdateColValue': UpdateColValue
    }
    return render(request, 'SalaryCreditedAddProof.html',context = context)



@login_required(login_url='login')
def SupportView(request):
    username = User.objects.get(username=request.user.username)
    if request.method == "POST":
        try:
            IssueType = request.POST['IssueType']
            Description = request.POST['Description']
            Support.objects.create(User=username, IssueType=IssueType, Description=Description)
            messages.warning(request, 'We will Check and update to you!')
        except Exception:
            # print(traceback.format_exc())
            messages.error(request, "Something went wrong! Please check the logs")
    SupportData = Support.objects.filter(User=username.id)
    context = {
        'SupportData' : SupportData
    }
    return render(request, 'Support.html',context = context)



@login_required(login_url='login')
def NotificationsView(request):
    return render(request, 'Notifications.html')




@login_required(login_url='login')
def InvestmentsView(request):
    return render(request, 'Investments.html')

#Savings
@login_required(login_url='login')
def SavingsView(request):
    return render(request, 'Savings.html')

#Settings page
@login_required(login_url='login')
def SettingsView(request):
    return render(request, 'Settings.html')
