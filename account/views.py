from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from .forms import *
from django.forms import inlineformset_factory
from .filter import OrderFilter
from django.contrib.auth.forms import UserCreationForm 
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import *
from django.contrib.auth.models import Group
from django.contrib.auth.models import User

# Create your views here.

@login_required #Or @login_required(login_url='login)
@admin_only
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {'orders' : orders, 'customers' : customers, 'total_customers' : total_customers,
                'total_orders' : total_orders, 'delivered' : delivered, 'pending' : pending}
    return render(request, 'account/dashboard.html',context)

@unauthenticated_user
def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            
            messages.success(request, 'Account was created for ' + username)
            return redirect('register')
    context = {'form':form}
    return render(request,'account/register.html',context)

@unauthenticated_user
def Login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request,"username or password doesn't match!")
    context = {}
    return render(request,'account/login.html',context)

@login_required
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    orders = request.user.customer.order_set.all()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    context = {'orders':orders, 'total_orders':total_orders, 'delivered':delivered, 'pending':pending}
    return render(request,'account/user.html',context)

def error_404(request, exception):
    return render(request,'account/error404.html')

@login_required
def Logout(request):
    logout(request)
    return redirect('login')

@login_required
@allowed_users(allowed_roles=['customer'])
def profile(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)
    if request.method == "POST":
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
    context={'form':form, 'customer':customer}
    return render(request,'account/profile.html',context)


@login_required
@allowed_users(allowed_roles=['admin'])
def products(request):
    products =Product.objects.all()
    context={'products':products}
    return render(request, 'account/products.html',context)

@login_required
@allowed_users(allowed_roles=['admin'])
def customer(request,customer_name):
    customers = Customer.objects.get(name=customer_name)
    
    orders = customers.order_set.all()
    order_count = orders.count()
    
    orderFilter = OrderFilter(request.GET,queryset=orders)
    orders = orderFilter.qs

    context={'customers': customers,'orders': orders,'order_count': order_count,'orderFilter':orderFilter}
    return render(request, 'account/customer.html',context)

@login_required
@allowed_users(allowed_roles=['admin'])
def createOrder(request,customer_name):
    # inlineformset_factory for create multiple forms
    OrderFormSet =inlineformset_factory(Customer,Order,fields=('product','status'),extra=3)
    customers = Customer.objects.get(name=customer_name)
    
    # form = OrderForm(initial={'customer':customers})
    formset = OrderFormSet(queryset=Order.objects.none(),instance=customers)
    
    if request.method == "POST":
        # form  = OrderForm(request.POST)
        formset = OrderFormSet(request.POST,instance=customers)
        if formset.is_valid():
            formset.save()
            return redirect('/')
    
    context= {'formset':formset}
    return render(request,'account/order_form.html',context)

@login_required
@allowed_users(allowed_roles=['admin'])
def updateOrder(request,pk):
    order = Order.objects.get(id=pk) 
    form = OrderForm(instance=order)
    if request.method == "POST":
        form  = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    context= {'form':form}
    return render(request,'account/updateorder.html',context)

@login_required
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request,pk):
    order = Order.objects.get(id=pk) 
    if request.method == "POST":
        order.delete()
        return redirect('/')
    context= {'item':order}
    return render(request,'account/delete.html',context)

