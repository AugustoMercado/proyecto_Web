from django.db import models
from django.contrib.auth.models import User
from myarticles.models import Products

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profile')
    day_buy = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Cart of {self.user.username}"

    def get_total(self):
        """
        Calculates the total price of the cart by summing the subtotals of all items.
        """
        total = 0
        for item in self.cartbuy.all():
            total += item.subtotal()
        return total

class CartsItems(models.Model):
    cart_id = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cartbuy')
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    def subtotal(self):
        """
        Calculates the subtotal for this specific item line.
        Handles both unit-based and weight-based (kilo) products.
        """
        if self.product.is_kilo:
            return (self.product.price / 100) * self.quantity
        else:
            return self.product.price * self.quantity