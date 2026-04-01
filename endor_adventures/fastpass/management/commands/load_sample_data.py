from django.core.management.base import BaseCommand
from fastpass.models import ThemeZone, Attraction, TimeSlot, Guest
from datetime import time

class Command(BaseCommand):
    help = 'Load sample data for Endor Adventures'

    def handle(self, *args, **options):
        # Add Theme Zones
        zones = [
            ThemeZone(name='Forest of Endor', description='Towering redwoods and ancient trees. Home to treehouse attractions.', is_open=True),
            ThemeZone(name='Ewok Village', description='The heart of Ewok civilization! Family-friendly rides.', is_open=True),
            ThemeZone(name='Imperial Ruins', description='Remnants of the fallen Empire. Thrill rides ahead!', is_open=True),
            ThemeZone(name='Speeder Bike Canyon', description='High-speed adventures through narrow forest paths.', is_open=True),
            ThemeZone(name='Bright Tree Grove', description='Entertainment and dining district. Live shows!', is_open=True),
        ]
        for zone in zones:
            zone.save()
        self.stdout.write(self.style.SUCCESS('Added 5 Theme Zones'))

        # Add Attractions
        forest = ThemeZone.objects.get(name='Forest of Endor')
        ewok = ThemeZone.objects.get(name='Ewok Village')
        imperial = ThemeZone.objects.get(name='Imperial Ruins')
        speeder = ThemeZone.objects.get(name='Speeder Bike Canyon')
        bright = ThemeZone.objects.get(name='Bright Tree Grove')

        attractions = [
            Attraction(name="Wicket's Wild Treehouse Drop", zone=forest, description='', attraction_type='ride', thrill_level=3, current_wait_minutes=25, is_operational=True),
            Attraction(name='Canopy Rope Bridge Walk', zone=forest, description='', attraction_type='experience', thrill_level=1, current_wait_minutes=10, is_operational=True),
            Attraction(name='Gorax Cave Expedition', zone=forest, description='', attraction_type='ride', thrill_level=3, current_wait_minutes=35, is_operational=True),
            Attraction(name='Log Drum Spinner', zone=ewok, description='', attraction_type='ride', thrill_level=2, current_wait_minutes=15, is_operational=True),
            Attraction(name="Chief Chirpa's Storytelling", zone=ewok, description='', attraction_type='show', thrill_level=1, current_wait_minutes=5, is_operational=True),
            Attraction(name='Ewok Cooking Class', zone=ewok, description='', attraction_type='experience', thrill_level=1, current_wait_minutes=20, is_operational=True),
            Attraction(name='AT-ST Rampage Coaster', zone=imperial, description='', attraction_type='ride', thrill_level=4, min_height_cm=140, current_wait_minutes=60, is_operational=True),
            Attraction(name='Bunker Escape Room', zone=imperial, description='', attraction_type='experience', thrill_level=2, current_wait_minutes=30, is_operational=True),
            Attraction(name='Speeder Bike Chase', zone=speeder, description='', attraction_type='ride', thrill_level=4, min_height_cm=140, current_wait_minutes=45, is_operational=True),
            Attraction(name='Scout Trooper Training', zone=speeder, description='', attraction_type='experience', thrill_level=3, current_wait_minutes=25, is_operational=True),
            Attraction(name='Yub Nub Celebration Show', zone=bright, description='', attraction_type='show', thrill_level=1, current_wait_minutes=0, is_operational=True),
            Attraction(name='Endor Cantina', zone=bright, description='', attraction_type='dining', thrill_level=1, current_wait_minutes=10, is_operational=True),
        ]
        for attraction in attractions:
            attraction.save()
        self.stdout.write(self.style.SUCCESS('Added 12 Attractions'))

        # Add Guests
        guests = [
            Guest(first_name='Luke', last_name='Skywalker', email='luke@rebellion.org', membership_tier='gold', height_cm=172),
            Guest(first_name='Leia', last_name='Organa', email='leia@rebellion.org', membership_tier='platinum', height_cm=150),
            Guest(first_name='Han', last_name='Solo', email='han@falcon.com', membership_tier='silver', height_cm=180),
            Guest(first_name='Wicket', last_name='Warrick', email='wicket@endor.net', membership_tier='platinum', height_cm=80),
            Guest(first_name='Chewie', last_name='Wookiee', email='chewie@kashyyyk.com', membership_tier='standard', height_cm=228),
        ]
        for guest in guests:
            guest.save()
        self.stdout.write(self.style.SUCCESS('Added 5 Guests'))

        # Add Time Slots for Speeder Bike Chase
        speeder_bike = Attraction.objects.get(name='Speeder Bike Chase')
        time_slots_data = [
            (time(9, 0), time(9, 30), 25),
            (time(10, 0), time(10, 30), 25),
            (time(11, 0), time(11, 30), 25),
            (time(13, 0), time(13, 30), 25),
            (time(14, 0), time(14, 30), 25),
            (time(15, 0), time(15, 30), 25),
        ]
        for start, end, max_fp in time_slots_data:
            TimeSlot.objects.create(attraction=speeder_bike, start_time=start, end_time=end, max_fastpasses=max_fp, is_active=True)
        self.stdout.write(self.style.SUCCESS('Added 6 time slots for Speeder Bike Chase'))

        # Add Time Slots for AT-ST Rampage Coaster
        atst = Attraction.objects.get(name='AT-ST Rampage Coaster')
        for start, end, max_fp in time_slots_data:
            TimeSlot.objects.create(attraction=atst, start_time=start, end_time=end, max_fastpasses=max_fp, is_active=True)
        self.stdout.write(self.style.SUCCESS('Added 6 time slots for AT-ST Rampage Coaster'))

        # Add Time Slots for Wicket's Wild Treehouse Drop
        wicket = Attraction.objects.get(name="Wicket's Wild Treehouse Drop")
        for start, end, max_fp in time_slots_data:
            TimeSlot.objects.create(attraction=wicket, start_time=start, end_time=end, max_fastpasses=max_fp, is_active=True)
        self.stdout.write(self.style.SUCCESS('Added 6 time slots for Wicket\'s Wild Treehouse Drop'))

        self.stdout.write(self.style.SUCCESS('Period 2 sample data complete!'))
