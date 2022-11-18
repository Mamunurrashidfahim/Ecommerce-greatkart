from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render, reverse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from accounts.forms import RegistrationForm,UserForm,UserProfileForm
from accounts.models import Account,UserProfile
from cart.views import _cart_id
from cart.models import CartItem,Cart
from orders.models import Order,OrderProduct
import requests
#Verification Email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage



def signup(request):
    if request.method =='POST':
        form=RegistrationForm(request.POST)
        if form.is_valid():
            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
            email=form.cleaned_data['email']
            phone_number=form.cleaned_data['phone_number']
            username=email.split("@")[0]
            password=form.cleaned_data['password']
            
            user=Account.objects._create_user(first_name=first_name,last_name=last_name,email=email,username=username,password=password)
            user.phone_number=phone_number
            user.save()
            
            #USER ACTIVATION
            current_site = get_current_site(request)
            mail_subject = 'Please activate you account'
            message = render_to_string('account/account_verification_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            
            # messages.success(request,"Thank you for registering with us. We have sent you a verification email to your email address. Please verify it!!")
            return redirect('/account/login/?command=verification&email='+email)
    else:
        form=RegistrationForm()
    return render(request,'account/signup.html',context={'form':form})

def login_page(request):
    if request.user.is_authenticated:
        if request.user.is_admin:
            return HttpResponse('This is Admin page')
        elif request.user.is_seller:
            return HttpResponse('This is Seller page')
        else:
            return HttpResponse('This is Customer page')
        
    return render(request, 'account/login.html')


def doLogin(request):
    if request.method =='POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email,password=password)
        if user != None:
            try:
              cart=Cart.objects.get(cart_id=_cart_id(request))
              is_cart_item_exists=CartItem.objects.filter(cart=cart).exists()
              
              if is_cart_item_exists:
                cart_item =CartItem.objects.filter(cart=cart)
                  
                product_variation = []
                for item in cart_item:
                    variation=item.variations.all()
                    product_variation.append(list(variation))
                      
                cart_item=CartItem.objects.filter(user=user)
                ex_var_list=[]
                id=[]
                for item in cart_item:
                    existing_variation =item.variations.all()
                    ex_var_list.append(list(existing_variation))
                    id.append(item.id)  
                
                for pr in product_variation:
                    if pr in ex_var_list:
                        index=ex_var_list.index(pr)
                        item_id=id[index]
                        item = CartItem.objects.get(id=item_id)
                        item.quantity += 1
                        item_user=user
                        item.save()
                    else:
                        cart_item=CartItem.objects.filter(cart=cart)
                        for item in cart_item:
                            item.user =user
                            item.save()  
            except:
              pass
            login(request, user)
            if user.is_admin:
                return HttpResponse('This is Admin page')
            elif user.is_seller:
                return HttpResponse('This is Seller page')
            else:
                messages.success(request,"You are now logged in!!")
                url =request.META.get('HTTP_REFERER')
                try:
                  query=requests.utils.urlparse(url).query
                  params=dict(x.split('=') for x in query.split('&'))
                  if 'next' in params:
                      nextPage =params['next']
                      return redirect(nextPage)
                except:
                    return redirect('account:dashbord')
        else:
            messages.success(request,"Invalid Login Information!!")
            return redirect("account:user_login")
            
    return render(request, 'account/login.html',context={})


@login_required(login_url ='account:user_login')
def logout_user(request):
    if request.user != None:
        logout(request)
    return redirect("/")



def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulations! Your account is activated.')
        return redirect('account:user_login')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('account:signup')

def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            # Reset Password Email
            current_site = get_current_site(request)
            mail_subject = 'Forgot Password'
            message = render_to_string('account/confirm_password_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(request, 'Password reset mail has been sent to your email address. If you not fimd the email,Check the "Spam" folder in your email inbox.')
            return redirect('account:user_login')
        else:
            messages.error(request, 'Account does not exist!')
            return redirect('account:forgotPassword')
    return render(request, 'account/forgotPassword.html')

def confirm_password_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return redirect('account:resetPassword')
    else:
        messages.error(request, 'This link has been expired!')
        return redirect('account:user_login')
        
def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successfully!!')
            return redirect('account:user_login')
        else:
           messages.error(request,"Password do not Match!!") 
           return redirect('account:resetPassword')  
    else:
        return render(request,'account/resetPassword.html',context={})

@login_required(login_url ='account:user_login')
def dashbord(request):
    orders=Order.objects.order_by('-created_at').filter(user_id=request.user.id,is_ordered=True)
    orders_count=orders.count()
    userprofile = UserProfile.objects.get(user_id=request.user.id)
    return render(request,'account/dashbord.html',context={'orders_count':orders_count,'userprofile':userprofile})

@login_required(login_url ='account:user_login')    
def my_orders(request):
    order_product=OrderProduct.objects.filter(user=request.user,ordered=True)
    context={
        'order_product':order_product}
    return render(request,'account/my_orders.html',context)


@login_required(login_url ='account:user_login')    
def edit_profile(request):
    userprofile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('account:edit_profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'userprofile': userprofile,
    }
    return render(request, 'account/edit_profile.html', context)

@login_required(login_url ='account:user_login')
def change_password(request):
    if request.method =='POST':
        current_password=request.POST['current_password']
        new_password=request.POST['new_password']
        confirm_password=request.POST['confirm_password']
        
        user=Account.objects.get(username__exact=request.user.username)
        
        if new_password == confirm_password:
            success=user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                messages.success(request,'Your Password has been Updated.')
                return redirect('account:change_password')
            else:
                messages.error(request,'Please Enter valid Current Password .')
                return redirect('account:change_password')
        else:
            messages.error(request,'Password Dose not match!!')
            return redirect('account:change_password')
        
    return render(request,'account/change_password.html',context={})

@login_required(login_url ='account:user_login')
def order_details(request, order_id):
    order_details=OrderProduct.objects.filter(order__order_number=order_id)
    order=Order.objects.get(order_number=order_id)
    
    total=0
    for i in order_details:
        total += i.product_price * i.quantity
    tax=(2*total)/100
    subtotal=total+tax
    
    return render(request,'account/order_details.html',context={'order_details':order_details,'order':order,'subtotal':subtotal})