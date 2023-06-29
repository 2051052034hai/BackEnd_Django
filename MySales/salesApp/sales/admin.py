from django.contrib import admin
from .models import Product, Category
from  django import  forms
from  ckeditor_uploader.widgets import CKEditorUploadingWidget


class ProductForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget)
    class Meta:
        model = Product
        fields = '__all__'


class ProductAdmin(admin.ModelAdmin):
    form = ProductForm
    list_display = ['id', 'name', 'description', 'unitPrice', 'unitsInStock']
    search_fields = ['name']
    list_filter = ['id', 'name', 'unitPrice', 'unitsInStock']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
