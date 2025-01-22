from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView
from django.contrib import messages
import requests

from weather_app.models import Location
from weather_app.services.weather_api_service import WeatherApiService
from weather_app.dto import LocationWeatherDTO


class StartPage(LoginRequiredMixin, ListView):
    template_name = 'weather_app/index.html'
    context_object_name = 'locations'
    paginate_by = 4

    def get_queryset(self):
        locations = Location.objects.filter(user=self.request.user).order_by('-id')

        weather_data = []

        for loc in locations:
            weather = LocationWeatherDTO()
            try:
                weather = WeatherApiService.get_location_by_coord(loc.latitude, loc.longitude)
            except requests.exceptions.RequestException as e:
                messages.error(self.request, str(f'Ошибка запроса к API: {e}'))

            weather_data.append(weather)

        return weather_data

    def post(self, request, *args, **kwargs):
        try:
            location = Location.objects.filter(user=self.request.user).get(
                longitude=float(request.POST['longitude'].replace(',', '.')),
                latitude=float(request.POST['latitude'].replace(',', '.'))
            )

            location.delete()
        except Exception as e:
            messages.error(request, str(f'Не удалось удалить локацию: {e}'))

        return redirect('main')




# class SearchPage(LoginRequiredMixin, TemplateView):
#     def get(self, request):
#         pass
#
#     def post(self):
#         pass

# def index(request):
#     return render(request, 'weather/pages/index.html')
