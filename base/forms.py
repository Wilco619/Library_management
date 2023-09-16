from django import forms
from django.shortcuts import render, redirect
from . models import Member, Book
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

class MemberRegForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['name','regNo','contact']
        widgets={
            'name':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Name'}),
            'regNo':forms.TextInput(attrs={'class':'form-control','placeholder':'Reg Number'}),
            'contact':forms.NumberInput(attrs={'class':'form-control','placeholder':'Contact'}),
        }

class BookRegForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['category','title','s_number','description']
        widgets={
            'category':forms.TextInput(attrs={'class':'form-control','placeholder':'Category'}),
            'title':forms.TextInput(attrs={'class':'form-control','placeholder':'Book title'}),
            's_number':forms.NumberInput(attrs={'class':'form-control','placeholder':'serial Number'}),
            'description':forms.TextInput(attrs={'class':'form-control','placeholder':'Description'}),
        }

def loginForm(request):
     
     page = 'login'
     #when the user is already logged in they cant access login page via the url
     if request.user.is_authenticated:
         return redirect('home')
     

     if request.method == 'POST':
         username = request.POST.get('username')
         password = request.POST.get('password')

        #try and check if the user exists in the database
         try:
             user = User.objects.get(username=username)
         except:
             messages.error(request, 'User Does Not Exist')

        #while the user is found to exist, authenticate the user, make sure password and username match   
         user = authenticate(request, username=username, password=password)

        #while the fields are not empty and user is found then create a session for the user and redirect them to their homepage
         if user is not None:
             login(request, user)
             return redirect('home')
         else:
             messages.error(request, 'UserName Or Password Does Not Exist!')
     return render(request, 'login.html', locals()) 

#cancel session from database and redirect to homepage
def logoutForm(request):
    logout(request)
    return redirect('login')