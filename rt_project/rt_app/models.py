from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta

class User(AbstractUser):
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='images/users/', blank=True, null=True)

    def __str__(self):
        return self.username


class Product(models.Model):
    class Condition(models.TextChoices):
        LIKE_NEW = 'like_new', 'Like New'
        EXCELLENT = 'excellent', 'Excellent'
        GOOD = 'good', 'Good'
        FAIR = 'fair', 'Fair'
        FOR_PARTS = 'for_parts', 'For Parts / Not Working'

    class Category(models.TextChoices):
        SMARTPHONES = 'smartphones', 'Smartphones & Mobile'
        LAPTOPS = 'laptops', 'Laptops & Computers'
        AUDIO = 'audio', 'Headphones & Audio'
        GAMING = 'gaming', 'Consoles & Gaming'
        COMPONENTS = 'components', 'PC Parts & Accessories'
        WEARABLES = 'wearables', 'Smartwatches & Tech'

    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    category = models.CharField(max_length=30, choices=Category.choices, default=Category.SMARTPHONES)
    title = models.CharField(max_length=255)
    brand = models.CharField(max_length=100)
    model_name = models.CharField(max_length=100, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    condition = models.CharField(max_length=20, choices=Condition.choices, default=Condition.GOOD)
    battery_health = models.PositiveIntegerField(blank=True, null=True)
    has_original_box = models.BooleanField(default=False)
    has_bill_or_warranty = models.BooleanField(default=False)
    product_image = models.ImageField(upload_to='images/products/')
    is_sold = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def is_new_arrival(self):
        return self.created_at >= timezone.now() - timedelta(days=7)

    @property
    def average_rating(self):
        avg_rating = self.reviews.aggregate(avg_rating=models.Avg('rating'))['avg_rating']
        return round(avg_rating, 1) if avg_rating else 0.0

    def __str__(self):
        return f"[{self.get_category_display()}] {self.title} - NPR {self.price} ({self.seller.username})"


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')


class Order(models.Model):
    class Status(models.TextChoices):
        CONFIRMED = 'confirmed', 'Order Confirmed'
        SHIPPING = 'shipping', 'In Transit'
        DELIVERED = 'delivered', 'Delivered'
        COMPLETED = 'completed', 'Completed'
        CANCELLED = 'cancelled', 'Cancelled'

    class PaymentMethod(models.TextChoices):
        ESEWA = 'esewa', 'eSewa'
        COD = 'cod', 'Cash on Delivery'

    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchases')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sales')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orders')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.CONFIRMED)
    transaction_id = models.CharField(max_length=100, blank=True, null=True, help_text="Payment provider tracking reference ID")
    shipping_address = models.TextField()
    payment_method = models.CharField(max_length=20, choices=PaymentMethod.choices, default=PaymentMethod.ESEWA)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} | {self.product.title} (Buyer: {self.buyer.username})"


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_reviews')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_reviews')
    rating = models.PositiveIntegerField(default=5)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review ({self.rating}★) by {self.reviewer.username} for {self.seller.username} on {self.product.title}"