from django.shortcuts import render

# Create your views here.
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status, generics
from .serializers import FileSerializer,InvoiceSerializer,ItemSerializer
from rest_framework.mixins import UpdateModelMixin
import pandas as pd
import tabula
from django.conf import settings
import os
from .models import File,Invoice
from django.http import Http404,JsonResponse
import PyPDF2
import random
from datetime import date
from drf_yasg.utils import swagger_auto_schema

class FileView(APIView):
    parser_classes = (MultiPartParser,FormParser)

    @swagger_auto_schema(operation_summary="API for Uploading a file and generating an invoice marking status of the file as digitized")
    def post(self, request, *args, **kwargs):
        file_serializer=FileSerializer(data=request.data)
        if file_serializer.is_valid(raise_exception=ValueError):
            print("valid")
            file_serializer.save()

            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        return Response(file_serializer.error_messages,
                        status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_summary="API to mark the status as digitized ")
    def patch(self, request, *args, **kwargs):
        file = get_object_or_404(File, pk=kwargs['filename'])
        print(type(file))
        print(file)
        serializer = FileSerializer(file, data=request.data, partial=True)
        if serializer.is_valid():
            file = serializer.save()
            return Response(FileSerializer(file).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class FileList(APIView):
    @swagger_auto_schema(operation_summary="API View  all the uploaded files")
    def get(self, request, format=None):
        files = File.objects.all()
        serializer = FileSerializer(files, many=True)
        return Response(serializer.data)


class InvoicesList(APIView):
    @swagger_auto_schema(operation_summary="API to view all the invoices")
    def get(self, request, format=None):
        invoices = Invoice.objects.all()
        serializer = InvoiceSerializer(invoices, many=True)
        return Response(serializer.data)



class StatusView(APIView):

    def get_object(self, filename):
        print(filename)
        print(type(filename))
        try:
            file=File.objects.get(filename=filename)
            print(file)
            return file
        except File.DoesNotExist:
            print("doen not exist")
            raise Http404

    @swagger_auto_schema(operation_summary="API to view status of the file")
    def get(self, request, filename, format=None):

        file= self.get_object(filename)
        serializer = FileSerializer(file)
        data={'filename':serializer.data['filename'],'status':serializer.data['status']}
        return JsonResponse(data)

class InvoiceDetailsView(APIView):

    def get_object(self, filename):
        print(filename)
        print(type(filename))
        try:
            file=File.objects.get(filename=filename)
            print(file)
            return file
        except File.DoesNotExist:
            print("doen not exist")
            raise Http404

    @swagger_auto_schema(operation_summary="API to view invoice details of a file")
    def get(self, request, filename, format=None):

        file= self.get_object(filename)
        if file.status=='digitized':
            invoice=file.invoice
            serializer = InvoiceSerializer(invoice)
            return Response(serializer.data)
        else:
            return JsonResponse({'message':'file is not digitized'})

    @swagger_auto_schema(operation_summary="API to partially update the invoice details of a file")
    def patch(self, request, *args, **kwargs):
        file = get_object_or_404(File, pk=kwargs['filename'])

        serializer = InvoiceSerializer(file.invoice, data=request.data, partial=True)
        if serializer.is_valid():
            print("(valid)")
            invoice=serializer.save()
            file.invoice=invoice
            file.save(update_fields=['invoice'])
            print(file)
            return Response(FileSerializer(file).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class InvoiceUpdateView(APIView):
    def get_object(self, filename):
        print(filename)
        print(type(filename))
        try:
            file=File.objects.get(filename=filename)
            print(file)
            return file
        except File.DoesNotExist:
            print("doen not exist")
            raise Http404

    @swagger_auto_schema(operation_summary="API to add items to the invoice of a file")
    def patch(self, request, *args, **kwargs):
        file = get_object_or_404(File, pk=kwargs['filename'])
        print(request.data)
        item_serializer=ItemSerializer(data=request.data)
        if item_serializer.is_valid():
            print("items are valid")
            item=item_serializer.save()
            file.invoice.items.add(item)
            file.save(update_fields=['invoice'])
            print(file)
            return Response(FileSerializer(file).data)
        else:
            return Response(item_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
























