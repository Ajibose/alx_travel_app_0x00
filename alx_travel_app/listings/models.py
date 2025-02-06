from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid


User = get_user_model()


class Listing(models.Model):
    """Represents Property listing

    Relationships:
        host_id (User): The user that owns the property
    """
    property_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name='properties')
    name = models.CharField(max_length=150)
    description = models.TextField()
    location = models.CharField(max_length=255)
    pricepernight = models.DecimalField(max_digits=12, decimal_places=2, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'listing'

    def __str__(self):
        """String representation of the model"""
        return f"{self.name} - {self.location}, {self.pricepernight}"


class Booking(models.Model):
    """Represent the booking of properties

    Relationships
        property_id (Property):
        user_id (User):
    """
    class StatusChoice(models.TextChoices):
        """Class for status choices"""
        PENDING = 'pending', 'pending'
        CONFIRMED = 'confirmed', 'confirmed'
        CANCELED = 'canceled', 'confirmed'

    booking_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    property = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bookings")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    start_date = models.DateField()
    end_date = models.DateField()
    total_price = models.DecimalField(max_digits=12, decimal_places=2, null=False)
    status = models.CharField(max_length=9, choices=StatusChoice.choices, default=StatusChoice.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'booking'

    def ___str__(self):
        """String representation of the model"""
        return f"{self.property}: {self.start_date} - {self.end_date}, {self.status}"


class Review(models.Model):
    """Represents review by users

    Relationships:
        property (Property):
        user (User):
    """
    review_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    property = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='reviews', null=True)
    rating = models.IntegerField(
            null=False,
            validators=[
                MinValueValidator(1), MaxValueValidator(5)
            ]
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        constraints = [
                models.UniqueConstraint(
                    fields=['property', 'user'],
                    name='unique_property_user'
                )
        ]
        get_latest_by = 'created_at'
        db_table = 'review'

    def ___str__(self):
        """String representation of the model"""
        return f"{self.property}: {self.user} - {self.rating} stars"
