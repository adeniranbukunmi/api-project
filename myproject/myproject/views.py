# import requests
# from django.http import JsonResponse
# from django.views import View
# from django.conf import settings

# class HelloView(View):
#     def get(self, request):
#         visitor_name = request.GET.get('visitor_name', 'Visitor')
#         client_ip = request.META.get('REMOTE_ADDR', '127.0.0.1')
        
#         geo_response = requests.get(f'https://ipapi.co/{client_ip}/json/')
#         geo_data = geo_response.json()
#         city = geo_data.get('city', 'New York')

#         weather_response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={settings.WEATHER_API_KEY}')
#         weather_data = weather_response.json()
#         temperature = weather_data['main']['temp']
        
#         greeting = f'Hello, {visitor_name}!, the temperature is {temperature} degrees Celcius in {city}'
        
#         response_data = {
#             'client_ip': client_ip,
#             'location': city,
#             'greeting': greeting
#         }
        
#         return JsonResponse(response_data)


# import requests
# from django.http import JsonResponse
# from django.views import View
# from django.conf import settings

# class HelloView(View):
#     def get(self, request):
#         try:
#             visitor_name = request.GET.get('visitor_name', 'Visitor')
#             client_ip = request.META.get('REMOTE_ADDR', '127.0.0.1')

#             geo_response = requests.get(f'https://ipapi.co/{client_ip}/json/')
#             geo_response.raise_for_status()  # Raise an error for bad status codes
#             geo_data = geo_response.json()
#             city = geo_data.get('city', 'New York')

#             weather_response = requests.get(
#                 f'https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={settings.WEATHER_API_KEY}'
#             )
#             weather_response.raise_for_status()  # Raise an error for bad status codes
#             weather_data = weather_response.json()
#             temperature = weather_data['main']['temp']

#             greeting = f'Hello, {visitor_name}!, the temperature is {temperature} degrees Celsius in {city}'

#             response_data = {
#                 'client_ip': client_ip,
#                 'location': city,
#                 'greeting': greeting
#             }
#         except requests.RequestException as e:
#             response_data = {
#                 'error': 'Error fetching data',
#                 'details': str(e)
#             }

#         return JsonResponse(response_data)
    





# views that manage ip address of user dynamically 

import requests
from django.http import JsonResponse, HttpResponseForbidden
from django.views import View
from django.conf import settings

ALLOWED_IPS = ['127.0.0.1']  # Start with a default allowed IP

class HelloView(View):
    def get(self, request):
        # Get the real client IP
        client_ip = request.META.get('HTTP_X_FORWARDED_FOR')
        if client_ip:
            client_ip = client_ip.split(',')[0]
        else:
            client_ip = request.META.get('REMOTE_ADDR', '127.0.0.1')

        # Check if the client IP is in the allowed list
        if client_ip not in ALLOWED_IPS:
            return HttpResponseForbidden('Your IP is not allowed to access this resource.')

        visitor_name = request.GET.get('visitor_name', 'David')
        city = request.GET.get('city')

        if not city:
            try:
                geo_response = requests.get(f'https://ipapi.co/{client_ip}/json/')
                geo_response.raise_for_status()  # Raise an error for bad status codes
                geo_data = geo_response.json()
                city = geo_data.get('city', 'ogbomoso')
            except requests.RequestException as e:
                return JsonResponse({'error': 'Error fetching location data', 'details': str(e)})

        try:
            weather_response = requests.get(
                f'https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={settings.WEATHER_API_KEY}'
            )
            weather_response.raise_for_status()  # Raise an error for bad status codes
            weather_data = weather_response.json()
            temperature = weather_data['main']['temp']

            greeting = f'Hello, {visitor_name}!, the temperature is {temperature} degrees Celsius in {city}'

            response_data = {
                'client_ip': client_ip,
                'location': city,
                'greeting': greeting
            }
        except requests.RequestException as e:
            response_data = {
                'error': 'Error fetching weather data',
                'details': str(e)
            }

        return JsonResponse(response_data)



