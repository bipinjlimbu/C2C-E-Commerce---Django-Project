from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta

class User(AbstractUser):
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='images/users/', blank=True, null=True)
    is_verified_seller = models.BooleanField(default=False)
    
    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=50, blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Product(models.Model):
    class Condition(models.TextChoices):
        LIKE_NEW = 'like_new', 'Like New'
        EXCELLENT = 'excellent', 'Excellent'
        GOOD = 'good', 'Good'
        FAIR = 'fair', 'Fair'
        FOR_PARTS = 'for_parts', 'For Parts / Not Working'

    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    
    title = models.CharField(max_length=255)
    brand = models.CharField(max_length=100)
    model_name = models.CharField(max_length=100, blank=True)
    
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_negotiable = models.BooleanField(default=True)
    
    condition = models.CharField(max_length=20, choices=Condition.choices, default=Condition.GOOD)
    battery_health = models.PositiveIntegerField(blank=True, null=True)
    has_original_box = models.BooleanField(default=False)
    has_bill_or_warranty = models.BooleanField(default=False)
    
    is_sold = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def primary_image(self):
        first_img = self.images.first()
        return first_img.image.url if first_img else None

    @property
    def is_recently_listed(self):
        return self.created_at >= timezone.now() - timedelta(days=7)

    def __str__(self):
        return f"{self.title} - NPR {self.price} ({self.seller.username})"


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='images/products/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        CONFIRMED = 'confirmed', 'Confirmed'
        SHIPPING = 'shipping', 'In Transit'
        DELIVERED = 'delivered', 'Delivered'
        COMPLETED = 'completed', 'Completed'
        CANCELLED = 'cancelled', 'Cancelled'

    class PaymentMethod(models.TextChoices):
        ESEWA = 'esewa', 'eSewa'
        KHALTI = 'khalti', 'Khalti'
        COD = 'cod', 'Cash on Delivery'

    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchases')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sales')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    
    delivery_address = models.TextField()
    payment_method = models.CharField(max_length=20, choices=PaymentMethod.choices, default=PaymentMethod.ESEWA)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} | {self.product.title}"


class SellerReview(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_reviews')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_reviews')
    order = models.OneToOneField(Order, on_delete=models.SET_NULL, null=True, blank=True)
    
    rating = models.PositiveIntegerField(default=5)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.seller.username} ({self.rating}★)"