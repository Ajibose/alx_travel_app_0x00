import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from listings.models import Listing, Booking, Review
from listings.serializers import ListingSerializer, BookingSerializer, ReviewSerializer
from faker import Faker

User = get_user_model()
fake = Faker()

class Command(BaseCommand):
    help = 'Seed the database with sample data'

    def handle(self, *args, **kwargs): 
        self.create_users()
        
        self.create_listings()
        
        self.create_bookings_and_reviews()
        
        self.stdout.write(self.style.SUCCESS('Successfully seeded database'))

    def create_users(self):
        for _ in range(5):
            User.objects.create_user(
                username=fake.user_name(),
                email=fake.email(),
                password=fake.password(length=10),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
            )
        

    def create_listings(self):
        hosts = User.objects.all()
        hosts = hosts[:2]
        
        for host in hosts:
            for _ in range(3):
                data = {
                    'host': host.id,
                    'name': fake.company(),
                    'description': fake.text(),
                    'location': fake.address(),
                    'pricepernight': random.randint(50, 500)
                }
                serializer = ListingSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
        

    def create_bookings_and_reviews(self):
        guests = User.objects.all()
        guests = guests[2:]
        listings = Listing.objects.all()
        status_choices = ['pending', 'confirmed', 'canceled']
        
        for guest in guests:
            for _ in range(2):
                listing = random.choice(listings)
                start_date = datetime.now().date()
                end_date = start_date + timedelta(days=random.randint(1, 7))
                data = {
                    'property': listing.property_id,
		    'user': guest.id,
		    'start_date': start_date,
		    'end_date': end_date,
		    'total_price': listing.pricepernight * (end_date - start_date).days,
		    'status': random.choice(status_choices)
		}

                serializer = BookingSerializer(data=data)
                booking = ""
                if serializer.is_valid():
                    booking = serializer.save()

                if booking.status == 'confirmed':
                    data = {
                        'property': listing.property_id,
                        'user': guest.id,
                        'rating': random.randint(1, 5),
                        'comment': fake.text()
                    }
                    serializer = ReviewSerializer(data=data)
                    if serializer.is_valid():
                        serializer.save()

