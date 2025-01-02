from django.db import models
from AdminApp . models import *

# Create your models here.
class Register(models.Model):
    name = models.CharField(max_length=100,default='null')
    email = models.EmailField(max_length=100,default='null')
    password = models.CharField(max_length=100,default='null')
    phone = models.CharField(max_length=100,default=0)
    place = models.TextField(default='null')
    status = models.IntegerField(default=0)

class Contact(models.Model):
    name = models.CharField(max_length=100,default='null')
    email = models.EmailField(max_length=100,default='null')
    phone = models.CharField(max_length=100,default=0)
    subject = models.CharField(max_length=20,default='null')
    message = models.TextField(default='null')

class Cart(models.Model):
    usercart = models.ForeignKey(Register,on_delete=models.CASCADE)
    userpro  = models.ForeignKey(Products,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total = models.IntegerField()
    status = models.IntegerField(default=0)

class Checkout(models.Model):
    usercheckout = models.ForeignKey(Register,on_delete=models.CASCADE)
    usercart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    adress = models.TextField()
    city = models.CharField(max_length=20)
    pincode = models.IntegerField()
    country = models.CharField(max_length=20)

class Payment(models.Model):
    user = models.ForeignKey(Register, on_delete=models.CASCADE, null=True, blank=True)  # Link payment to a user
    payment_id = models.CharField(max_length=100)  # PayPal payment ID
    payer_id = models.CharField(max_length=100, null=True, blank=True)  # PayPal payer ID
    amount = models.IntegerField()  # Payment amount
    currency = models.CharField(max_length=10, default='USD')  # Currency used
    status = models.CharField(max_length=20)  # Payment status (e.g., "Completed", "Failed")
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the payment was created
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp for the last update
