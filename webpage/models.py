from distutils.command.upload import upload
from django.db import models

# Create your models here.
class product(models.Model):
    product_id=models.AutoField
    product_name=models.CharField(max_length=30)
    product_description=models.CharField(max_length=250)
    price=models.IntegerField()
    category=models.CharField(max_length=100)
    product_date=models.DateField()
    image=models.ImageField(upload_to='webpage/images')
    def __str__(self):
        return self.product_name

class Contact(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=30)
    email=models.CharField(max_length=30)
    phone=models.CharField(max_length=30)
    desc=models.CharField(max_length=30)
    def __str__(self):
        return self.name
class Order(models.Model):
    order_id=models.AutoField(primary_key=True)
    item_json=models.CharField(max_length=5000)
    amount=models.IntegerField(default=0)
    name=models.CharField(max_length=100)
    email=models.CharField(max_length=50)
    address=models.CharField(max_length=5000)
    city=models.CharField(max_length=50)
    state=models.CharField(max_length=50)
    zip_code=models.IntegerField()
    phone=models.CharField(max_length=10)
class Orderupdate(models.Model):
    update_id=models.AutoField(primary_key=True)
    order_id=models.IntegerField(default="")
    update_desc=models.CharField(max_length=500)
    timestamp=models.DateField(auto_now_add=True)
    def __str__(self):
        return self.update_desc[0:8]+"..."
