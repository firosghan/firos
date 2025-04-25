from django.db import models
from django.db.models import IntegerField


# Create your models here.
class user_resgister(models.Model):
    name=models.CharField(max_length=20)
    phone=models.IntegerField()
    email=models.EmailField()
    username=models.CharField(max_length=20)
    password=models.CharField(max_length=10)
    status=models.CharField(max_length=20,default='user')
    Buildingname=models.CharField(max_length=30,null=True)
    housenumber=models.CharField(max_length=30,null=True)
    landmark=models.CharField(max_length=30,null=True)
    city=models.CharField(max_length=30,null=True)
    pincode=models.CharField(max_length=30,null=True)
    state=models.CharField(max_length=30,null=True)

class category(models.Model):
    name=models.CharField(max_length=20)

class product(models.Model):
    name=models.CharField(max_length=20)
    price=models.IntegerField()
    quantity=models.IntegerField()
    image=models.ImageField()
    category=models.ForeignKey(category,on_delete=models.CASCADE)

class cart(models.Model):
    product_details=models.ForeignKey(product,on_delete=models.CASCADE)
    user_details=models.ForeignKey(user_resgister,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)
    total_price=models.IntegerField()

class wishlist(models.Model):
    product_details = models.ForeignKey(product, on_delete=models.CASCADE)
    user_details = models.ForeignKey(user_resgister, on_delete=models.CASCADE)

class myorder(models.Model):
    product_details=models.ForeignKey(product, on_delete=models.CASCADE)
    user_details = models.ForeignKey(user_resgister, on_delete=models.CASCADE)
    product_status=models.CharField(max_length=20)
    payment_amount=models.IntegerField()
    order_date=models.DateTimeField()
    quantity=models.IntegerField()

class contacts(models.Model):
    name = models.CharField(max_length=20)
    phone = models.IntegerField()
    email = models.EmailField()
    messagebox = models.TextField()

class PasswordReset(models.Model):
    user_details = models.ForeignKey(user_resgister,on_delete = models.CASCADE)
    token = models.CharField(max_length=255)








