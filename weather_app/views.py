from decimal import Decimal
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.db import IntegrityError
from django.contrib import messages
from django.http import HttpResponse
import requests

from weather_app.models import Location
from weather_app.services.weather_api_service import WeatherApiService
from weather_app.dto import LocationWeatherDTO


class StartPage( LoginRequiredMixin, ListView):
    '''Возвращает домашнюю страницу с отображением добавленных локаций.'''
    template_name = 'weather/pages/index.html'
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

    # def delete(self, request, *args, **kwargs):
    #     try:
    #         location = Location.objects.filter(user=request.user).get(
    #             longitude=float(request.POST['longitude'].replace(',', '.')),
    #             latitude=float(request.POST['latitude'].replace(',', '.'))
    #         )
    #         location.delete()
    #         messages.success(request, "Локация удалена.")
    #     except Exception as e:
    #         messages.error(request, f'Не удалось удалить локацию: {e}')
    #
    #     return redirect('weather_app:main')

    def post(self, request, *args, **kwargs):
        """Обрабатывает удаление локации."""
        longitude = Decimal(request.POST['longitude'].replace(',', '.'))
        latitude = Decimal(request.POST['latitude'].replace(',', '.'))
        locations = Location.objects.filter(user=request.user)
        try:
            location = Location.objects.filter(user=request.user).get(
                longitude=Decimal(request.POST['longitude'].replace(',', '.')),
                latitude=Decimal(request.POST['latitude'].replace(',', '.'))
            )
            # location = Location.objects.filter(
            #     user=request.user,
            #     latitude=latitude,
            #     longitude=longitude
            # ).first()
            if location:
                location.delete()
                messages.success(request, "Локация удалена.")
        except Exception as e:
            messages.error(request, f'Не удалось удалить локацию: {e}')

        return redirect('weather_app:main')


class SearchPage(LoginRequiredMixin, ListView):
    '''Возвращает список найденных населенных пунктов.'''

    template_name = 'weather/pages/search.html'
    context_object_name = 'locations'

    def get_queryset(self):
        location = self.request.GET.get('location')
        try:
            if not location:
                return []
            return WeatherApiService.get_locations_by_name(name=location)
        except Exception as e:
            messages.error(self.request, f'Ошибка поиска локаций: {e}')
        return []

    def post(self, request, *args, **kwargs):
        try:
            name = request.POST.get('name')
            country = request.POST.get('country')
            longitude = Decimal(request.POST.get('longitude').replace(',', '.'))
            latitude = Decimal(request.POST.get('latitude').replace(',', '.'))

            location = Location.objects.create(
                name=name,
                country=country,
                longitude=longitude,
                latitude=latitude,
                user=request.user,
            )
            location.save()
            messages.info(self.request, 'Локация добавлена')
            return redirect('weather_app:main')
        except IntegrityError as e:
            messages.error(self.request, f'Локация уже добавлена в вашу коллекцию')
            return redirect('weather_app:main')





