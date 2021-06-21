from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Company(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images')
    description = models.TextField(max_length=10000, blank=True, null=True)
    category = models.ManyToManyField(Category, related_name='category')
    company = models.ForeignKey(Company, related_name='company', on_delete=models.CASCADE)
    price = models.IntegerField()
    discount = models.IntegerField(default=0)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.name

class Cart(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    session_key = models.CharField(max_length=200, blank=True)
    product = models.ManyToManyField(Product, related_name='product_items', blank=True)

class Quantity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product')
    quantity = models.IntegerField(default=1)
