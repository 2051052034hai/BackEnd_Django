from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField

class BaseModel(models.Model):
    createdDate = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class UserRoleEnum(models.IntegerChoices):
    CUSTOMER = 1
    EMPLOYEE = 2
    ADMIN = 3


class User(AbstractUser):
    address = models.CharField(max_length=50, null=True)
    phone = models.CharField(max_length=10, null= True)
    role = models.IntegerField(choices=UserRoleEnum.choices, default=UserRoleEnum.CUSTOMER)
    avatar = models.ImageField(upload_to="sales/%Y/%m", null=True)
    accumulatePoint = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = RichTextField(null=True)
    unitPrice = models.DecimalField(max_digits=10, decimal_places=2)
    unitsInStock = models.IntegerField()
    image = models.ImageField(upload_to="sales/%Y/%m", null=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    bills = models.ManyToManyField('Bill', through='BillDetail', related_name='products')

    def __str__(self):
        return self.name


class Bill(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subTotal = models.DecimalField(max_digits=10, decimal_places=2)


class BillDetail(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()

    def total_price(self):
        return self.price * self.quantity


class Supplier(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


class ImportBill(BaseModel):
    createdDate = models.DateTimeField(auto_now_add=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True)
    products = models.ManyToManyField('Product', through='ImportDetail', related_name='imports')


class ImportDetail(models.Model):
    importBill = models.ForeignKey(ImportBill, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.ImageField()
    price = models.DecimalField(max_digits=10, decimal_places=2)


class Event(BaseModel):
    endDate = models.DateTimeField(auto_now_add=True)
    product = models.ManyToManyField('Product', through='EvenDetail', related_name='events')


class EvenDetail(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    discountPrice = models.DecimalField(max_digits=10, decimal_places=2)
