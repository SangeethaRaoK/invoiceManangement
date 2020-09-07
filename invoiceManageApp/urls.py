from django.urls import path

from .views import FileView,InvoicesList,FileList,StatusView,InvoiceDetailsView,InvoiceUpdateView
from rest_framework.documentation import include_docs_urls


urlpatterns = [

    path('upload/',FileView.as_view(),name="fileUpload"),
    path('fileStatusUpdate/<str:filename>',FileView.as_view(),name="fileStatusUpdateView"),
    path('fileList/',FileList.as_view(),name="filelist"),
    path('status/<str:filename>',StatusView.as_view(),name="statusview"),
    path('invoicesList/',InvoicesList.as_view(),name="listInvoices"),
    path('invoiceDetails/<str:filename>',InvoiceDetailsView.as_view(),name="invoiceDetails"),
    path('invoiceUpdate/<str:filename>',InvoiceDetailsView.as_view(),name="invoiceUpdate"),
    path('addInvoiceItems/<str:filename>',InvoiceUpdateView().as_view(),name="addItems"),

]