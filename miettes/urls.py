"""miettes URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from MA import views
from django.conf.urls import include

urlpatterns = [
    path('taymaa-and-sara-only-secret/', admin.site.urls),
    path('homepage', views.homepage),
    path('', views.homepage),
    path('aboutus', views.aboutus_view, name='aboutus'),
    path('contactus', views.contactus_view, name='contactus'),
    path('products/', views.products_view, name='products'),
    #path('productcard', views.productcard_view,name='productcard'),
    path('discover', views.discover_view, name='discover'),
    path('collections/<str:Title_en>/', views.collection_view, name='collections'),
    # path('addproduct', views.addproduct_view, name='addproduct'),
    path('viewproduct/<str:SKU>/', views.viewproduct_view, name='viewproduct'),
    path('faq/', views.faq_view, name='faq'),
    path('checkout', views.checkout_view, name='checkout'),
    path('orderemail', views.orderemail_view, name='orderemail'),
    path('removeitem/<str:orderItemID>',
         views.removeitem_view, name='removeitem'),
    path('search/', views.search_view,name='search'),
    path('payment/', views.payment_view,name='payment'),


]


handler404 = 'MA.views.page_not_found_view'
# handler500 = 'MA.views.page_not_found_view'
