from django.db import models

# Create your models here.
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name 

class Products(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    details = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.DecimalField(max_digits=10, decimal_places=2)
    is_kilo = models.BooleanField(default=False, verbose_name="Sold by weight?")
    is_promotion = models.BooleanField(default=False, verbose_name="Is Promotion?")
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return self.name 
    
class Promotions(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(verbose_name="Description / Product List") 
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name="Price")
    image = models.ImageField(upload_to='proms/') 
    active = models.BooleanField(default=True, verbose_name="Show on homepage?")

    def __str__(self):
        return self.title