from django.urls import path
from store import views

app_name ='store'

urlpatterns = [
    path('',views.index,name='home'),
    path('store/',views.store,name='store'),
    path('shop/',views.shop,name='shop'),
    path('shop/<slug:category_slug>/',views.shop,name='Products_by_category'),
    path('store/<slug:store_slug>/',views.store_page,name='store_page'),
    path('store/<slug:store_slug>/<slug:product_slug>/',views.product_detail,name='single_product'),
    path('search/',views.search,name='search'),
    path('submit_review/<int:product_id>/',views.submit_review,name='submit_review'),

]