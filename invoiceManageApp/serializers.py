from rest_framework import serializers
from .models import File,Invoice,Item
import random
import datetime

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=Item
        fields=['name','description','price']

    def create(self,validated_data):
        print(validated_data)
        print("creating items")
        if "file" not in validated_data.keys():
            print("invoice exists.add new item to invoice")
            item_data=Item.objects.create(name=validated_data['name'],description=validated_data['description'],price=validated_data['price'])
            print(item_data)
            print("items created")
            return(item_data)
        else:

            print("new invoice items")
            item_data=Item.objects.create(name="HarryPotter",description="book",price=500)
            print(item_data)
            print("items created")
            return item_data


class InvoiceSerializer(serializers.ModelSerializer):
    items=ItemSerializer(required=False,many=True)
    class Meta:
        model=Invoice
        fields=['vendor','purchaser','invoicenumber','duedate','subtotal','tax','total','items']


    def create(self, validated_data):
        print("creating invoice")
        invoice_number = random.randint(1, 100)
        print(invoice_number)
        item_data=ItemSerializer.create(ItemSerializer,validated_data)

        invoice_data = Invoice.objects.create(vendor='Infinera', purchaser='Sangeetha', invoicenumber=invoice_number,duedate=datetime.datetime.now(), subtotal=10000,
                               tax=25, total=10025)
        invoice_data.items.add(item_data)
        print(invoice_data)
        print("invoice created successfully")
        return invoice_data






class FileSerializer(serializers.ModelSerializer):
    invoice=InvoiceSerializer(required=False)
    class Meta:
        model=File
        fields=['file','filename','status','uploadedtime','invoice','custname']

    def create(self, validated_data):
        print("creating  file")
        invoice=InvoiceSerializer.create(InvoiceSerializer(),validated_data=validated_data)
        print(validated_data)
        file,created=File.objects.update_or_create(invoice=invoice,file=validated_data['file'],filename=validated_data['filename'],status='digitized',uploadedtime=datetime.datetime.now(),custname=validated_data['custname'])
        return file



