from django.db import models
from django.urls import reverse
from category.models import Category
from django.conf import settings
from accounts.models import Account
from django.db.models import Avg,Count

class Store(models.Model):
    store_owner = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    store_name  = models.CharField(max_length=264,blank=True)
    store_slug  = models.SlugField(max_length=255,unique=True)
    store_image = models.ImageField(upload_to='store_profile_pic')
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)
    is_active   = models.BooleanField(default=True)
    
    def get_url(self):
        return reverse('store:store_page',args=[self.store_slug])
    
    def __str__(self):
        return self.store_name


class Product(models.Model):
    product_name   =models.CharField(max_length=255,unique=True)
    store          =models.ForeignKey(Store,on_delete=models.CASCADE)
    category       =models.ForeignKey(Category,on_delete=models.CASCADE)
    slug           =models.SlugField(max_length=255,unique=True)
    description    =models.TextField(max_length=500,blank=True)
    price          =models.IntegerField()
    old_price      =models.IntegerField()
    images         =models.ImageField( upload_to='products')
    stock          =models.IntegerField()
    is_available   =models.BooleanField(default=True)
    create_at      =models.DateTimeField( auto_now_add=True)
    update_at      =models.DateTimeField( auto_now=True)
    
    def get_url(self):
        return reverse('store:single_product',args=[self.store.store_slug, self.slug])
    
    def __str__(self):
        return self.product_name
    
    def averageReview(self):
        reviews=ReviewRating.objects.filter(product=self,status=True).aggregate(average=Avg('rating'))
        avg=0
        if reviews['average'] is not None:
            avg=float(reviews['average'])
        return avg
    
    def countReview(self):
        reviews=ReviewRating.objects.filter(product=self,status=True).aggregate(count=Count('rating'))
        count=0
        if reviews['count'] is not None:
            count=int(reviews['count'])
        return count
            
 
class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager,self).filter(variation_category='color',is_active=True)
    
    def sizes(self):
        return super(VariationManager,self).filter(variation_category='size',is_active=True)
    
 
variation_category_choices=(
    ('color','color'),
    ('size','size'),  
)

class Variation(models.Model):
    product             = models.ForeignKey(Product,on_delete=models.CASCADE)
    variation_category  = models.CharField(max_length=100,choices=variation_category_choices)
    variation_value     =models.CharField(max_length=50)
    is_active           =models.BooleanField(default=True)
    create_at           =models.DateTimeField(auto_now_add=True)
    
    objects=VariationManager()
    
    def __str__(self):
        return self.variation_value
    
class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject
    
class ProductGallery(models.Model):
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    image=models.ImageField( upload_to='store/products', max_length=255)
    
    def __str__(self):
        return self.product.product_name
    
    class Meta:
        verbose_name = 'Product Gallery'
        verbose_name_plural = 'Product Gallery'
        
class HomeSlider(models.Model):
    images = models.ImageField(upload_to='homeslider')
    title = models.CharField(max_length=100)
    is_active=models.BooleanField(default=True)
    
    def __str__(self):
        return self.title
    
class StoreSlider(models.Model):
    images = models.ImageField(upload_to='storeslider')
    title = models.CharField(max_length=100)
    is_active=models.BooleanField(default=True)
    
    def __str__(self):
        return self.title