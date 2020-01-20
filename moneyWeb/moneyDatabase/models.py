from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class StockBuying(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    broker = models.CharField(max_length=30)
    date = models.DateTimeField(default=timezone.now)
    asset_name = models.CharField(max_length=50)
    quantity = models.FloatField()
    value = models.FloatField()
    total_value = models.FloatField()
    total_value_paid = models.FloatField()
    comment = models.TextField(default="")

    def __str__(self):
        return self.asset_name

class StockSelling(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    broker = models.CharField(max_length=30)
    date = models.DateTimeField(default=timezone.now)
    asset_name = models.CharField(max_length=50)
    quantity = models.FloatField()
    value = models.FloatField()
    total_value = models.FloatField()
    total_value_received = models.FloatField()
    comment = models.TextField(default="")

    def __str__(self):
        return self.asset_name

class FixedBuying(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    broker = models.CharField(max_length=30)
    date = models.DateTimeField(default=timezone.now)
    asset_name = models.CharField(max_length=50)
    quantity = models.FloatField()
    value = models.FloatField()
    total_value = models.FloatField()
    total_value_paid = models.FloatField()
    comment = models.TextField(default="")

    def __str__(self):
        return self.asset_name

class FixedSelling(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    broker = models.CharField(max_length=30)
    date = models.DateTimeField(default=timezone.now)
    asset_name = models.CharField(max_length=50)
    quantity = models.FloatField()
    value = models.FloatField()
    total_value = models.FloatField()
    total_value_received = models.FloatField()
    comment = models.TextField(default="")

    def __str__(self):
        return self.asset_name

class REIFBuying(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    broker = models.CharField(max_length=30)
    date = models.DateTimeField(default=timezone.now)
    asset_name = models.CharField(max_length=50)
    quantity = models.FloatField()
    value = models.FloatField()
    total_value = models.FloatField()
    total_value_paid = models.FloatField()
    comment = models.TextField(default="")

    def __str__(self):
        return self.asset_name

class REIFSelling(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    broker = models.CharField(max_length=30)
    date = models.DateTimeField(default=timezone.now)
    asset_name = models.CharField(max_length=50)
    quantity = models.FloatField()
    value = models.FloatField()
    total_value = models.FloatField()
    total_value_received = models.FloatField()
    comment = models.TextField(default="")
    profit = models.FloatField(default=0.00)
    darf = models.FloatField(default=0.00)
    darf_paid = models.CharField(max_length=5, default="")

    def __str__(self):
        return self.asset_name

class Current(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    asset_name = models.CharField(max_length=50)
    quantity = models.FloatField()
    mean_value = models.FloatField()
    total = models.FloatField()

    def __str__(self):
        return self.asset_name

class Taxes(models.Model):
    date_updated = models.DateTimeField(default=timezone.now)
    tax_name = models.CharField(max_length=50)
    value = models.FloatField()

    def __str__(self):
        return self.tax_name
