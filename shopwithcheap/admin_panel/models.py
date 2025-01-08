from django.db import models

# Create your models here.
class Admin(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name

class User(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    
class AddCategory(models.Model):
    category = models.CharField(max_length=255)
    subcategory=models.CharField(max_length=255)

class Project(models.Model):
    category = models.CharField(max_length=255)
    subcategory = models.CharField(max_length=255)
    product_title = models.CharField(max_length=255)
    product_image = models.ImageField(upload_to='images/')
    product_price = models.IntegerField()
