from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from .apps import PagesConfig
import random
import pandas as pd
from .models import Bank, Details
import pickle
import numpy as np
import os

def predict(request):
    
    if request.method == 'POST':
        
            # get sound from request
        Gender = request.POST.get('gender')
        Married = request.POST.get('married')
        Dependents = request.POST.get('dependents')
        Education = request.POST.get('education')
        Self_Employed = request.POST.get('self_employed')
        Applicant_Income = request.POST.get('applicantIncome')
        Coapplicant_Income = request.POST.get('coapplicantIncome')
        Loan_Amount = request.POST.get('loanamount')
        Loan_Amount_Term = request.POST.get('loan_amount_term')
        Credit_History = request.POST.get('credit_history')
        Property_Area = request.POST.get('propertyarea')
            # np.array([income,age,rooms,bedrooms,population])
            
            
        
        price = {'Gender': [int(Gender)],
            'Married': [int(Married)],
            'Dependents': [int(Dependents)],
            'Education': [int(Education)],
            'Self_Employed': [int(Self_Employed)],        
            'Applicant_Income': [int(Applicant_Income)],        
            'Coapplicant_Income': [int(Coapplicant_Income)],        
            'Loan_Amount': [int(Loan_Amount)],        
            'Loan_Amount_Term': [int(Loan_Amount_Term)],        
            'Credit_History': [int(Credit_History)],        
            'Property_Area': [int(Property_Area)],    
                        
            }
        df = pd.DataFrame(price,columns=['Gender','Married','Dependents','Education','Self_Employed','Applicant_Income','Coapplicant_Income','Loan_Amount','Loan_Amount_Term','Credit_History','Property_Area']) 
            # vectorize sound
            # vector = PricepredictorConfig.vectorizer.transform([income,age,rooms,bedrooms,population])
        new_row = {'Gender':1, 'Married':1, 'Dependents':2, 'Education':1, 'Self_Employed':0, 'Applicant_Income':10000, 'Coapplicant_Income':2000, 'Loan_Amount':208, 'Loan_Amount_Term':200, 'Credit_History':1, 'Property_Area':2}

        df = df.append(new_row, ignore_index=True)

        from sklearn.decomposition import PCA
        pca = PCA(n_components = 2)
        testab = pca.fit_transform(df)
        explained_variance = pca.explained_variance_ratio_
            # predict based on vector
        prediction = PagesConfig.classifier.predict(testab)[0]
         
        bank = False
        if(int(prediction) == 1):
            # random.randint(2,30) for rec in range(3)
            bank = Bank.objects.filter(id__in=[2,3])
            eligible = "1"
        else:
            eligible = "0"    
            # build response
        response = {
            'eligibility': eligible,
            'status':int(prediction)
            }
        if bank:
            response.update({
                'bank1': bank[0],'bank2': bank[1],
            })
            # return response
            # return JsonResponse(response)
    return render(request, 'pages/services.html',response)

def index(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:

            if User.objects.filter(username=username).exists():
                messages.error(request, 'That username is taken')
                return redirect('index')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'That email is being used')
                    return redirect('index')
                else:
                    user = User.objects.create_user(username=username, email=email, password=password)
                    user.save()
                    auth.login(request, user)
                    return redirect('login')
        else:
            messages.error(request,'Passwords do not match')
            return redirect('index')
    else:
        return render(request,'pages/index.html')
    return render(request,'pages/index.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password'] 

        user = auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request,'You are now logged in')
            return redirect('index')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')
    else:
        return render(request, 'pages/login.html')

def logout(request):
    auth.logout(request)
    messages.success(request,'You are now logged out')
    return redirect('index')

def dashboard(request):
    return render(request,'pages/dashboard.html')

def services(request):
    return render(request,'pages/services.html')

def contact(request):
    return render(request,'pages/contact.html')

def details(request):
    banks = Details.objects.all()
    response = {
        'banks': banks
    }
    
    return render(request,'pages/details.html', response)

def risk(request):

    if request.method == 'POST':
        Bank = request.POST.get('bank')
        Area = request.POST.get('area')
        module_dir = os.path.dirname(__file__)  # get current directory
        file_path = os.path.join(module_dir, 'chetanModel.sav')
        print(file_path)
        with open(module_dir + '/chetanModel.sav', 'rb') as model:

	        clf, bank, state, city, area, defaulter = pickle.load(model)
        if Bank and Area:
            b = bank.fit_transform([Bank])
            a = area.fit_transform([Area])

            risk_factor = clf.predict_proba(np.array([b, a]).reshape(1, -1))


            rounded_risk =  [round(risk, 1) * 100 for risk in risk_factor[0].tolist()]
            bank_risk , area_risk = rounded_risk[0], rounded_risk[1]               

            response = {
            'bank_risk': bank_risk,
            'area_risk': area_risk
            }       
            print("xrdctfvygbhnjmcfvgbhjnm",response)  
            return render(request,'pages/services.html', response)

    return render(request,'pages/services.html')