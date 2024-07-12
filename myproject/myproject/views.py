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

# import requests
# from django.http import JsonResponse, HttpResponseForbidden
# from django.views import View
# from django.conf import settings

# # ALLOWED_IPS = ['127.0.0.1']  # Start with a default allowed IP
# ALLOWED_IPS = ['127.0.0.1', "http://havilah.pythonanywhere.com/",]  # restrict it to allow the domain name  after  deployment

# class HelloView(View):
#     def get(self, request):
#         # Get the real client IP
#         client_ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR'))
#         if client_ip:
#             client_ip = client_ip.split(',')[0]
#         else:
#             client_ip = request.META.get('REMOTE_ADDR', '127.0.0.1')  #Default to '127.0.0.1' if not found

#         # Check if the client IP is in the allowed list
#         if client_ip not in ALLOWED_IPS:
#             return HttpResponseForbidden('Your IP is not allowed to access this resource.')

#         visitor_name = request.GET.get('visitor_name', 'Visitor')
#         city = request.GET.get('city')

#         if not city:
#             try:
#                 geo_response = requests.get(f'https://ipapi.co/{client_ip}/json/')
#                 geo_response.raise_for_status()  # Raise an error for bad status codes
#                 geo_data = geo_response.json()
#                 city = geo_data.get('city', 'ogbomoso')
#             except requests.RequestException as e:
#                 return JsonResponse({'error': 'Error fetching location data', 'details': str(e)})

#         try:
#             weather_response = requests.get(
#                 weather_url = f"http://api.weatherapi.com/v1/current.json?key={settings.WEATHER_API_KEY}&q={location}"
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
#                 'error': 'Error fetching weather data',
#                 'details': str(e)
#             }

#         return JsonResponse(response_data)


import requests
from django.http import JsonResponse
from django.conf import settings

def hello(request):
    visitor_name = request.GET.get('visitor_name', 'visitor')

    client_ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR'))
    

    ip_address_url = f"http://api.weatherapi.com/v1/ip.json?key={settings.URL}&q={client_ip}"

    ip_response = requests.get(ip_address_url)
    ip_result = ip_response.json()

    if ip_response.status_code == 200:
        location = ip_result.get('city', 'Unknown')
    else:
        location = 'Unknown'
        print('Location not valid! Enter your city.')

    weather_url = f"http://api.weatherapi.com/v1/current.json?key={settings.URL}&q={location}"

    weather_response = requests.get(weather_url)
    
    weather_data = weather_response.json()

    if weather_response.status_code == 200:
        temp_c = weather_data['current']['temp_c']
        greeting = f"Hello, {visitor_name}!, the temperature is {temp_c} degrees Celsius in {location}"
    else:
        temp_c = 'N/A'
        greeting = f"Hello, {visitor_name}! Temperature unavailable for {location}. Please try again later."
    
    hello = {
        'client_ip': client_ip,
        'location': location,
        'greeting': greeting
    }

    return JsonResponse(hello)


