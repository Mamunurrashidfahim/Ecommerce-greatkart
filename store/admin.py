from django.contrib import admin
import admin_thumbnails
from store.models import HomeSlider, Product, ProductGallery, ReviewRating,Store, Variation,StoreSlider


@admin_thumbnails.thumbnail('image')
class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug': ('product_name',)}
    list_display =('product_name','slug','category','price','stock','is_available')
    inlines =[ProductGalleryInline]
admin.site.register(Product ,ProductAdmin)

class StoreAdmin(admin.ModelAdmin):
    prepopulated_fields={'store_slug': ('store_name',)}
    list_display =('store_name','store_owner','store_slug','created_at','is_active')

admin.site.register(Store ,StoreAdmin)

class VariationAdmin(admin.ModelAdmin):
    list_display =('product','variation_category','variation_value','is_active')
    list_editable =('is_active',)
    list_filter =('product','variation_category','variation_value')
    
admin.site.register(Variation,VariationAdmin)

admin.site.register(ReviewRating)
admin.site.register(ProductGallery)
admin.site.register(HomeSlider)
admin.site.register(StoreSlider)