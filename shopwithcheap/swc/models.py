from django.db import models

# Create your models here.
class Admin(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    def __str__(self):
        return self.name
    
class Subcategory(models.Model):
    category = models.CharField(max_length=255)
    subcategory = models.CharField(max_length=255)

class Product(models.Model):
    category = models.CharField(max_length=255)
    subcategory = models.CharField(max_length=255)
    product_title = models.CharField(max_length=255)
    product_price = models.IntegerField()
    product_image = models.ImageField(upload_to="product/")

class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    def __str__(self):
        return self.name
    
class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    mobile = models.BigIntegerField()
    message = models.CharField(max_length=255)
