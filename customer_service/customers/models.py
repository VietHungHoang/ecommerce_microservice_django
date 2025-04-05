import uuid
from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class Customer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, max_length=255)
    password = models.CharField(max_length=128)  # Sẽ lưu trữ hash
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return f"{self.full_name} ({self.email})"

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Customer"
        verbose_name_plural = "Customers"


class Address(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, related_name='addresses', on_delete=models.CASCADE)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    sub_district = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    is_default_shipping = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.street}, {self.sub_district}, {self.district} {self.city}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Address"
        verbose_name_plural = "Addresses"
        # Make sure there is only one default shipping address for each customer
        constraints = [
            models.UniqueConstraint(fields=['customer', 'is_default_shipping'], condition=models.Q(is_default_shipping=True), name='unique_default_shipping'),
        ]