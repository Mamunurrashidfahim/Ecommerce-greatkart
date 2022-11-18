from django.db.models.query_utils import Q
from django.http.response import HttpResponse
from django.shortcuts import redirect, render,get_object_or_404
from cart.models import CartItem
from store.models import HomeSlider, ProductGallery, ReviewRating, Store,Product, StoreSlider
from accounts.models import UserProfile
from django.views.generic import DetailView
from category.models import Category
from cart.views import _cart_id
from django.core.paginator import Paginator
from django.db.models import Q
from store.forms import ReviewForm
from django.contrib import messages
from orders.models import OrderProduct


def index(request):
    product =Product.objects.all().filter(is_available=True)
    home_slider = HomeSlider.objects.filter(is_active=True)
    for prod in product:
         reviews=ReviewRating.objects.filter(product_id=prod.id,status=True)
    
    return render(request,'home.html',context={'product':product,'reviews':reviews,'home_slider':home_slider})

def shop(request,category_slug=None):
    categories =None
    product =None
    
    if category_slug != None:
        categories      = get_object_or_404(Category, slug=category_slug)
        product         = Product.objects.filter(category=categories, is_available=True)
        paginator=Paginator(product,1)
        page=request.GET.get('page')
        paged_products=paginator.get_page(page)
        product_count   =product.count()
    else:
        product =Product.objects.all().filter(is_available=True).order_by('id')
        paginator=Paginator(product,2)
        page=request.GET.get('page')
        paged_products=paginator.get_page(page)
        product_count=product.count()
    return render(request,'shop.html',context={'product':paged_products,'product_count':product_count})

def store(request):
    store=Store.objects.all().filter(is_active=True)
    store_slider =StoreSlider.objects.filter(is_active=True)
    return render(request,'store.html',context={'store':store,'store_slider':store_slider})

def store_page(request,store_slug):
    store_page =Store.objects.get(store_slug=store_slug)
    product=Product.objects.filter(store=store_page)
    return render(request,'store_page.html',context={'store_page':store_page,'product':product})

def product_detail(request,store_slug,product_slug):
    try:
        single_product =Product.objects.get(store__store_slug=store_slug,slug=product_slug)
        in_cart =CartItem.objects.filter(cart__cart_id=_cart_id(request),product=single_product).exists()
    except Exception as e:
        raise e
    if request.user.is_authenticated:
        try:
            orderproduct=OrderProduct.objects.filter(user=request.user,product_id=single_product.id).exists()
        except OrderProduct.DoesNotExist:
            orderproduct=None
    else:
        orderproduct=None
      
    reviews=ReviewRating.objects.filter(product_id=single_product.id,status=True)
    
    
    product_gallery=ProductGallery.objects.filter(product_id = single_product.id)
    
    return render(request,'product_detail.html',context={'single_product':single_product,'in_cart':in_cart,'orderproduct':orderproduct,'reviews':reviews,'product_gallery':product_gallery})

def search(request):
    if 'keyword' in request.GET:
        keyword=request.GET['keyword']
        if keyword:
            product =Product.objects.order_by('-create_at').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            product_count=product.count()
        
    return render(request,'shop.html',context={'product':product,'product_count':product_count})


def submit_review(request,product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method =='POST':
        try:
            reviews=ReviewRating.objects.get(user__id=request.user.id,product__id=product_id)
            form=ReviewForm(request.POST,instance=reviews)
            form.save()
            messages.success(request, 'Thank you! Your review has been updated.')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data=ReviewRating()
                data.subject=form.cleaned_data['subject']
                data.review=form.cleaned_data['review']
                data.rating=form.cleaned_data['rating']
                data.ip=request.META.get('REMOTE_ADDR')
                data.product_id=product_id
                data.user_id=request.user.id
                data.save()
                messages.success(request, 'Thank you! Your review has been Submitted.')
                return redirect(url)
                
      