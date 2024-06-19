# models.py
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    rating = models.IntegerField(default=0)# Нове поле для рейтингу
    specifications = models.TextField(blank=True)  # Нове поле для специфікацій

    def __str__(self):
        return self.name

class Cart(models.Model):
    cart_id = models.CharField(max_length=100,blank = True)
    date_added = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.cart_id
    
class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default = True)
    
    def sub_total(self):
        return self.product.price * self.quantity
    def __str__(self):
        return str(self.product)