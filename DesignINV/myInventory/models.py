from django.db import models
from django.contrib.auth.models import User

# Model to store Site data
class Site(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


# Model to store Inventory data for each site
class Inventory(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    material_code = models.CharField(max_length=100)
    material_desc = models.CharField(max_length=255)
    owner = models.CharField(max_length=255)
    type = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    opening_stock = models.IntegerField()
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Add this field

    def __str__(self):
        return f"{self.material_code} - {self.material_desc}"


class Notification(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    material_code = models.CharField(max_length=100)
    opening_stock = models.IntegerField(default=0)
    consumption = models.IntegerField(null=True, blank=True)
    closing_stock = models.IntegerField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.material_code} at {self.timestamp}"

