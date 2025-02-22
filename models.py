from django.db import models

class Table(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Column(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.table.name}.{self.name}"

class Sales(models.Model):
    sale_id = models.IntegerField(primary_key=True)
    region = models.CharField(max_length=100)
    amount = models.FloatField()
    date = models.DateField()
    customer_id = models.IntegerField()
    product_id = models.IntegerField()

class Employees(models.Model):
    emp_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    salary = models.FloatField()
    hire_date = models.DateField()

class Customers(models.Model):
    customer_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    join_date = models.DateField()

class Products(models.Model):
    product_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    price = models.FloatField()
    stock = models.IntegerField()

class Orders(models.Model):
    order_id = models.IntegerField(primary_key=True)
    customer_id = models.IntegerField()
    product_id = models.IntegerField()
    quantity = models.IntegerField()
    order_date = models.DateField()