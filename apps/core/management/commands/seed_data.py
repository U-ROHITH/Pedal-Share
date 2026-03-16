from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.cycles.models import Cycle
from apps.users.models import UserProfile
from decimal import Decimal

class Command(BaseCommand):
    help = 'Seeds the database with the exact initial data seen in the original project'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding exact data from screenshot...')

        # 1. Create superuser
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            self.stdout.write(self.style.SUCCESS('Created superuser: admin'))
        else:
            admin = User.objects.get(username='admin')

        # 2. Create exact users
        user_list = [
            ('Priya Sharma', 'priya'),
            ('Amit Singh', 'amit'),
            ('Rohan Gupta', 'rohan'),
            ('Sahil Kumar', 'sahil'),
            ('Neha Raj', 'neha'),
            ('Vikram Singh', 'vikram')
        ]
        
        users = {}
        for full_name, username in user_list:
            user, created = User.objects.get_or_create(
                username=username, 
                defaults={'email': f'{username}@example.com'}
            )
            if created:
                user.set_password('pass123')
                user.save()
            
            profile, _ = UserProfile.objects.get_or_create(user=user)
            profile.full_name = full_name
            profile.wallet_balance = Decimal('500.00')
            profile.save()
            users[username] = user
            self.stdout.write(f'Created/Updated user: {full_name}')

        # 3. Create exact cycles from screenshot
        # Title, Type, Color, Price, Location, Owner_Username, Rating, Rides
        cycle_data = [
            ('P-Color', 'regular', 'Purple', '10.00', 'Hostel B, Gate 2', 'priya', '4.5', 12),
            ('City Cruiser', 'regular', 'Teal', '20.00', 'Main Campus, Block A', 'amit', '4.7', 18),
            ('Trek Master', 'mountain', 'Orange', '30.00', 'Sports Complex, Block D', 'rohan', '4.5', 15),
            ('Blue Bolt', 'hybrid', 'Blue', '25.00', 'Library Gate, Block C', 'sahil', '4.8', 22),
            ('Red Rover', 'hybrid', 'Red', '22.00', 'Admin Block, Parking Lot', 'neha', '4.6', 11),
            ('Green Racer', 'mountain', 'Green', '15.00', 'Cafeteria Entrance, Block G', 'vikram', '4.4', 9),
        ]

        Cycle.objects.all().delete() # Clear existing to avoid duplicates during seeding

        for title, ctype, color, price, loc, owner_uname, rate, rides in cycle_data:
            Cycle.objects.create(
                title=title,
                owner=users[owner_uname],
                cycle_type=ctype,
                color=color,
                price_per_hour=Decimal(price),
                location=loc,
                available_from='08:00',
                available_until='20:00',
                is_available=True,
                rating=Decimal(rate),
                total_bookings=rides
            )
            self.stdout.write(f'Created cycle: {title}')

        self.stdout.write(self.style.SUCCESS('Successfully seeded exact data!'))
