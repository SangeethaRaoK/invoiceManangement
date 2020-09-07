from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
class Item(models.Model):
    name=models.CharField(max_length=20)
    description=models.CharField(max_length=30)
    price=models.FloatField()

class Invoice(models.Model):
    vendor=models.CharField(max_length=20)
    purchaser=models.CharField(max_length=20)
    invoicenumber=models.IntegerField(primary_key=True)
    duedate=models.DateTimeField(auto_now_add=True)
    subtotal=models.FloatField()
    tax=models.FloatField()
    total=models.FloatField()
    items=models.ManyToManyField(Item,related_name='inlcudes')

class File(models.Model):
    file=models.FileField(blank=False,null=False)
    custname=models.CharField(max_length=10,default="admin")
    filename=models.CharField(max_length=50,primary_key=True)
    status=models.CharField(max_length=20)
    uploadedtime=models.DateTimeField(auto_now_add=True)
    invoice=models.ForeignKey(Invoice,on_delete=models.CASCADE)

