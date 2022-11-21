from django.contrib.sitemaps import Sitemap
from .models import Product, Collection, Category
from django.urls import reverse

class ProductSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Product.objects.all()
    

class CollectionSitemap(Sitemap):
    changefreq = "weekly"
    priority = 1.0 

    def items(self):
        return Collection.objects.all()

class CategorySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Category.objects.all()

class StaticViewSitemap(Sitemap):
    priority = 0.7
    changefreq = 'daily'

    def items(self):
        return ['aboutus', 'contactus', 'faq','homepage','products']

    def location(self, item):
        return reverse(item)