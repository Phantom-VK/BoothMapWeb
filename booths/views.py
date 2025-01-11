from django.shortcuts import render
from django.http import JsonResponse
from .firebase_utils import BoothDatabase

booth_db = BoothDatabase()

# Fetch and display cities
async def city_selection(request):
    try:
        cities = await booth_db.fetch_cities()
        context = {'cities': cities}
        return render(request, 'booths/city_selection.html', context)
    except Exception as e:
        return render(request, 'booths/city_selection.html', {'error': str(e)})

# Fetch talukas for a city
async def get_talukas(request, city):
    try:
        # Fetch booths for the city
        booths = await booth_db.fetch_booths(city)

        # Extract unique talukas (normalized)
        talukas = list({booth.get('taluka', '').strip() for booth in booths})
        return JsonResponse({'talukas': talukas})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# Fetch booths for a specific city and taluka
async def get_booths_by_taluka(request, city, taluka):
    try:
        # Normalize the input taluka
        taluka_normalized = taluka.strip().lower()

        # Fetch booths for the city
        all_booths = await booth_db.fetch_booths(city)
        # Filter booths for the specific taluka
        taluka_booths = [
            booth for booth in all_booths
            if booth.get('taluka', '').strip().lower() == taluka_normalized
        ]

        # Log filtered results for debugging
        print(f"Filtered booths for taluka '{taluka}': {taluka_booths}")
        return JsonResponse({'booths': all_booths})
    except Exception as e:
        # Log the error for debugging
        print(f"Error in get_booths_by_taluka: {e}")
        return JsonResponse({'error': str(e)}, status=500)

# Render map view
def map_view(request):
    return render(request, 'map_view.html', {})
