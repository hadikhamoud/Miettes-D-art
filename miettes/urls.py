
from django.contrib import admin
from django.urls import path
from MA import views
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('taymaa-and-sara-only-secret/', admin.site.urls),
    path('homepage', views.homepage),
    path('', views.homepage),
    path('aboutus', views.aboutus_view, name='aboutus'),
    path('contactus', views.contactus_view, name='contactus'),
    path('products/', views.products_view, name='products'),
    path('webmail', views.webmail_view, name='webmail'),
    path('checkcart', views.cart_view, name='checkcart'),
    path('discover', views.discover_view, name='discover'),
    path('collections/<str:Title_en>/', views.collection_view, name='collections'),
    path('viewproduct/<str:SKU>/', views.viewproduct_view, name='viewproduct'),
    path('faq/', views.faq_view, name='faq'),
    path('checkout', views.checkout_view, name='checkout'),
    path('removeitem/<str:orderItemID>',
         views.removeitem_view, name='removeitem'),
    path('search/', views.search_view,name='search'),
    path('payment/', views.payment_view,name='payment'),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = 'MA.views.page_not_found_view'
handler500 = 'MA.views.internal_server_error_view'
handler403 = 'MA.views.permission_denied_view'
handler400 = 'MA.views.bad_request_view'
