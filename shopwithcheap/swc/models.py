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

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        return self.product.product_price * self.quantity