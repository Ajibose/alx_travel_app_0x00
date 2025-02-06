from .models import Listing, Booking, Review
from rest_framework import serializers


class ListingSerializer(serializers.ModelSerializer):
    """
        Serializer and deserializer for Listing model
    """
    bookings = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = Listing
        fields = [
                'property_id', 'host', 'name', 'description', 'location', 
                'pricepernight', 'created_at', 'updated_at', 'bookings'
        ]
        read_only_fields = ['property_id', 'created_at', 'updated_at']


class BookingSerializer(serializers.ModelSerializer):
    """
        Serializer and deserializer for Booking model
    """
    property = serializers.PrimaryKeyRelatedField(queryset=Listing.objects.all())
    class Meta:
        model = Booking
        fields = [
                'booking_id', 'property', 'user', 'start_date',
                'end_date', 'total_price', 'status', 'created_at'
        ]
        read_only_fields = ['booking_id', 'created_at']


    def vlaidate(self, data):
        """
            Check that the start date is less than the end date
        """
        start = data['start_date']
        end = data['end_date']
        if start >= end:
            raise serializer.ValidationError(
                    "The start date must be before the end date"
            )
        return data


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer and deserializer for Review model"""
    class Meta:
        model = Review
        fields = [
                'review_id', 'property', 'user',
                'rating', 'comment', 'created_at'
        ]
        read_only_fields = ['review_id', 'created_at']
