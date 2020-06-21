from django.http import HttpResponse
from django.shortcuts import render,redirect

def unauthenticated_user(view_func):
    def wrapper_function(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)
    
    return wrapper_function
    
def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_function(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roles:   
                return view_func(request, *args, **kwargs)
            else:
                return render(request,'account/error403.html')
        return wrapper_function
    return decorator

def admin_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        if group == "customer":   
            return redirect('userpage')
        if group == "admin":   
            return view_func(request, *args, **kwargs)
    return wrapper_function
    


