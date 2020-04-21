from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import RegistrationAccountForm, AccountAuthenticationForm, AccountUpdateForm
# Create your views here.

def registration_view(request):
    context = {}
    if request.POST:
        form = RegistrationAccountForm(request.POST)
        if form.is_valid():
            account = form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            #account = authenticate(email=email, password=raw_password)
            login(request, account, backend='django.contrib.auth.backends.ModelBackend')
            
            return redirect('home')
        else:
            context['registration_form'] = form
    else:
        form = RegistrationAccountForm()
        context['registration_form'] = form
    return render(request, 'account/register.html', context)

def login_view(request):
    context = {}
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.POST:
        form =  AccountAuthenticationForm(request.POST)
        if form.is_valid():
            #email = request.POST['email']
            phone = request.POST['phone']
            password = request.POST['password']
            #account = authenticate(email=email, password=password)
            account = authenticate(phone=phone, password=password)
            if account:
                login(request, account)
                return redirect('home')
    else:
        form = AccountAuthenticationForm()
    context['login_form'] = form
    return render(request, 'account/login.html', context )

def logout_view(request):
    logout(request)
    return redirect('login')

def account_view(request):
    context = {}
    if not request.user.is_authenticated:
        return redirect('login')
    if request.POST:
        form = AccountUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
    else:
        form = AccountUpdateForm(
            initial={
                'email': request.user.email,
                'username': request.user.username,
            }
        )
    context['account_form'] = form
    return render(request, 'account/profile.html', context)