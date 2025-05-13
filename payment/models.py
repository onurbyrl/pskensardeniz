from django.db import models
from users.models import CustomUser

# Create your models here.

class Payment(models.Model):
    client = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="payments")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)