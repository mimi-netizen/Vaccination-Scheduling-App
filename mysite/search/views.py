from django.shortcuts import render
from django.db.models import Q
from django.http import JsonResponse
from .models import CenterLocation, VaccineAvailability
from center.models import Center
from vaccine.models import Vaccine
from math import radians, cos, sin, asin, sqrt

def haversine_distance(lat1, lon1, lat2, lon2):
    """Calculate the distance between two points on earth"""
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    km = 6371 * c  # Earth's radius in kilometers
    return km

def search_view(request):
    query = request.GET.get('q', '')
    lat = request.GET.get('lat')
    lng = request.GET.get('lng')
    distance = float(request.GET.get('distance', 10))
    
    # Base querysets
    centers = Center.objects.all()
    vaccines = Vaccine.objects.all()
    
    # Filter by search query
    if query:
        centers = centers.filter(
            Q(name__icontains=query) |
            Q(address__icontains=query)
        )
        vaccines = vaccines.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )
    
    # Filter by location if coordinates provided
    if lat and lng:
        try:
            lat = float(lat)
            lng = float(lng)
            # Get all center locations
            center_locations = CenterLocation.objects.all()
            nearby_center_ids = []
            
            # Calculate distances and filter
            for loc in center_locations:
                dist = haversine_distance(lat, lng, loc.latitude, loc.longitude)
                if dist <= distance:
                    nearby_center_ids.append(loc.center_id)
            
            centers = centers.filter(id__in=nearby_center_ids)
        except:
            pass
    
    context = {
        'centers': centers,
        'vaccines': vaccines,
        'query': query,
    }
    
    return render(request, 'search/search_results.html', context)

def nearby_centers_api(request):
    lat = request.GET.get('lat')
    lng = request.GET.get('lng')
    distance = float(request.GET.get('distance', 10))
    
    if not (lat and lng):
        return JsonResponse({'error': 'Latitude and longitude are required'}, status=400)
    
    try:
        lat = float(lat)
        lng = float(lng)
        centers_data = []
        
        for loc in CenterLocation.objects.all():
            dist = haversine_distance(lat, lng, loc.latitude, loc.longitude)
            if dist <= distance:
                centers_data.append({
                    'id': loc.center.id,
                    'name': loc.center.name,
                    'distance': round(dist, 2),
                    'lat': loc.latitude,
                    'lng': loc.longitude,
                })
        
        return JsonResponse({'centers': centers_data})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

def vaccine_availability_api(request):
    center_id = request.GET.get('center_id')
    
    if not center_id:
        return JsonResponse({'error': 'Center ID is required'}, status=400)
    
    try:
        availabilities = VaccineAvailability.objects.filter(
            center_id=center_id,
            available_quantity__gt=0
        ).select_related('vaccine')
        
        data = [{
            'vaccine_id': av.vaccine.id,
            'vaccine_name': av.vaccine.name,
            'quantity': av.available_quantity,
            'price': str(av.price),
            'last_updated': av.last_updated.isoformat()
        } for av in availabilities]
        
        return JsonResponse({'availabilities': data})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
