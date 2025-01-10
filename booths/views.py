# views.py
from django.shortcuts import render
from django.http import JsonResponse
from .firebase_utils import BoothDatabase

booth_db = BoothDatabase()

async def city_selection(request):
    try:
        cities = await booth_db.fetch_cities()
        context = {
            'cities': cities,
        }
        return render(request, 'booths/city_selection.html', context)
    except Exception as e:
        return render(request, 'booths/city_selection.html', {'error': str(e)})

async def get_talukas(request, city):
    try:
        booths = await booth_db.fetch_booths(city)
        # Extract unique talukas from booths
        talukas = list(set(booth['taluka'] for booth in booths))
        return JsonResponse({'talukas': talukas})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

async def get_booths_by_taluka(request, city, taluka):
    try:
        all_booths = await booth_db.fetch_booths(city)
        # Filter booths by taluka
        taluka_booths = [booth for booth in all_booths if booth['taluka'] == taluka]
        return JsonResponse({'booths': taluka_booths})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def map_view(request):
    # Render a map template or return a JSON response
    return render(request, 'map_view.html', {})