import firebase_admin
from firebase_admin import credentials, db
from django.conf import settings

import logging

def initialize_firebase():
    try:
        # Check if Firebase is already initialized
        firebase_admin.get_app()
        logging.info("Firebase app already initialized.")
    except ValueError:
        # Initialize Firebase
        logging.info(f"Initializing Firebase with credentials: {settings.FIREBASE_CREDENTIALS_PATH}")
        cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
        firebase_admin.initialize_app(cred, {
            'databaseURL': settings.FIREBASE_DATABASE_URL
        })
        logging.info("Firebase app successfully initialized.")



class BoothDatabase:
    def __init__(self):
        initialize_firebase()
        self.db = db.reference('Cities')

    async def fetch_cities(self):
        try:
            cities_snapshot = self.db.get()
            return list(cities_snapshot.keys()) if cities_snapshot else []
        except Exception as e:
            raise Exception(f"Error fetching cities: {str(e)}")

    async def fetch_booths(self, city):
        try:
            # print(f"Fetching booths for city: {city}")
            booths_snapshot = self.db.child(city).get()
            # print(f"Raw booths snapshot: {booths_snapshot}")

            booths = []
            if booths_snapshot:
                for booth_data in booths_snapshot.values():
                    # print(f"Processing booth data: {booth_data}")
                    if (booth_data.get('id') and
                            booth_data.get('bloName') and
                            booth_data.get('latitude') and
                            booth_data.get('longitude')):
                        booth = {
                            'id': booth_data.get('id', ''),
                            'name': booth_data.get('name', 'Unnamed Booth'),
                            # Default to "Unnamed Booth" if name is missing
                            'images': booth_data.get('imageUri', ''),
                            'blo_name': booth_data.get('bloName', ''),
                            'blo_contact': booth_data.get('bloContact', ''),
                            'district': booth_data.get('district', city),
                            'taluka': booth_data.get('taluka', ''),
                            'latitude': float(booth_data.get('latitude', 0.0)),
                            'longitude': float(booth_data.get('longitude', 0.0))
                        }

                        booths.append(booth)
            # print(f"Booths fetched: {booths}")
            return booths
        except Exception as e:
            raise Exception(f"Error fetching booths: {str(e)}")
