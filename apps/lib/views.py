from django.shortcuts import redirect

from lib.decorators import render_to

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm

from django.contrib.auth.decorators import login_required

@render_to('lib/auth.html')
def auth(request):
    out = {}
    
    out['login_form'] = login_form = AuthenticationForm()
    
    if request.user.is_authenticated():
        return redirect('/')
    
    if request.method == 'POST':
        out['login_form'] = login_form = AuthenticationForm(data=request.POST)
        
        if login_form.is_valid():
            user = authenticate(username=login_form.cleaned_data['username'], password=login_form.cleaned_data['password'])
            
            if user is not None:
                if user.is_active:
                    login(request, user)
            
            return redirect('/')
        else:
            return out
    
    return out

@login_required
def logout_user(request):
    logout(request)

    return redirect('/')