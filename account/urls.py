from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home,name="home"),
    path('products/', views.products,name="products"),
    path('customer/<str:customer_name>/', views.customer,name="customer"),
    path('createorder/<str:customer_name>/',views.createOrder,name="createorder"),
    path('updateorder/<str:pk>/',views.updateOrder,name="updateorder"),
    path('deleteorder/<str:pk>/',views.deleteOrder,name="deleteorder"),
    path('register/',views.register,name="register"),
    path('login/',views.Login,name="login"),
    path('logout/',views.Logout,name="logout"),
    path('user/',views.userPage,name="userpage"),
    path('profile/',views.profile,name="profile"),
    path('reset_password/',
     auth_views.PasswordResetView.as_view(template_name="account/reset.html"),
     name="reset_password"),
     
    path('reset_password_sent/', 
        auth_views.PasswordResetDoneView.as_view(template_name="account/password_reset_sent.html"), 
        name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
     auth_views.PasswordResetConfirmView.as_view(template_name="account/password_reset_form.html"), 
     name="password_reset_confirm"),

    path('reset_password_complete/', 
        auth_views.PasswordResetCompleteView.as_view(template_name="account/password_reset_done.html"), 
        name="password_reset_complete"),

]

'''
1- submit email form  #PasswordChangeView.as_view
2- email sent success message #PasswordRestDoneView.as_view()
3- link to password rest from in email #PasswordRestConfirmView.as_view()
4- password successfully change message #PasswordRestCompleteView.as_view()
'''