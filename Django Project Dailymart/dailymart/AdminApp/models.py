from django.db import models

# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=20)
    category_desc = models.TextField()
    category_image = models.ImageField(upload_to='images')
class Products(models.Model):
    product_name = models.CharField(max_length=20,default='null')
    product_price = models.IntegerField(default=0)
    product_desc = models.TextField(default='null')
    product_image = models.ImageField(default='null',upload_to='pics')
    product_category = models.CharField(max_length=20,default='null')

