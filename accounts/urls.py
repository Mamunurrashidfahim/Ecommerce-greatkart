from django.urls import path
from accounts import views

app_name='account'

urlpatterns = [ 
    path("login/", views.doLogin, name='user_login'),
    path("signup/", views.signup, name='signup'),
    path("logout/", views.logout_user, name='logout'),
    path("dashbord/", views.dashbord, name='dashbord'),
    path("my_orders/", views.my_orders, name='my_orders'),
    path("edit_profile/", views.edit_profile, name='edit_profile'),
    path("change_password/", views.change_password, name='change_password'),
    path("order_details/<int:order_id>/", views.order_details, name='order_details'),
    path("", views.dashbord, name='dashbord'),
    
    
    path("activate/<uidb64>/<token>/", views.activate, name='activate'),
    path('forgotPassword/',views.forgotPassword,name='forgotPassword'),
    path("confirm_password_validate/<uidb64>/<token>/", views.confirm_password_validate, name='confirm_password_validate'),
    path('resetPassword/',views.resetPassword,name='resetPassword'),
]
