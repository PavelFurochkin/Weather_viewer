import decimal
from unittest.mock import patch
from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.contrib.messages.storage.fallback import FallbackStorage

from weather_app.dto import LocationWeatherDTO
from weather_app.models import Location
from weather_app.views import StartPage, SearchPage

User = get_user_model()


class StartPageTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass333333')
        self.factory = RequestFactory()
        self.view = StartPage()
        self.request = self.factory.get('/')
        self.request.user = self.user
        self.view.request = self.request

        self.location1 = Location.objects.create(
            user=self.user,
            country='RU',
            name='Куево Тутуево',
            latitude=decimal.Decimal('36.2243'),
            longitude=decimal.Decimal('117.8301')
        )

        self.dto_instance = LocationWeatherDTO(
            temperature=-2,
            temperature_feels_like=-7,
            weather_desc='overcast clouds',
            humidity=91,
            wind_speed=4.3,
            icon_id='04n',
            name='Куево Тутуево',
            country='RU',
            latitude=self.location1.latitude,
            longitude=self.location1.longitude
        )

    @patch('weather_app.views.WeatherApiService.get_location_by_coord')
    def test_get_queryset_success(self, mock_get_location):
        """
        Проверяем, что GET-запрос к стартовой странице:
         - вызывает WeatherApiService.get_location_by_coord с корректными параметрами,
         - возвращает в контекст список погоды (сформированный на основе результата сервиса).
        """
        mock_get_location.return_value = self.dto_instance

        # Вызываем тестируемый метод get_queryset
        qs = self.view.get_queryset()

        # Проверяем, что возвращается список из одной записи
        self.assertEqual(len(qs), 1)
        # Сравниваем полученный DTO с ожидаемым
        self.assertEqual(qs[0], self.dto_instance)

        # Проверяем, что метод WeatherApiService.get_location_by_coord вызвался ровно один раз
        # с корректными координатами (значения из self.location1)
        mock_get_location.assert_called_once_with(
            self.location1.latitude,
            self.location1.longitude
        )

    def test_post_deletes_location(self):
        data = {
            "latitude": str(self.location1.longitude).replace('.', ','),
            "longitude": str(self.location1.latitude).replace('.', ',')
        }

        request = self.factory.post('/', data=data)
        request.POST = data
        request.user = self.user
        request.session = {}
        # Устанавливаем фейковое хранилище сообщений, чтобы избежать ошибки MessageFailure
        setattr(request, '_messages', FallbackStorage(request))
        response = self.view.post(request)

        # Проверяем, что объект локации был удален из базы
        self.assertFalse(Location.objects.filter(pk=self.location1.pk).exists())

        self.assertEqual(response.status_code, 302)


class SearchPageTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass333333')
        self.factory = RequestFactory()
        self.view = SearchPage()

        self.location1 = Location.objects.create(
            user=self.user,
            country='RU',
            name='Куево Тутуево',
            latitude=decimal.Decimal('36.2243'),
            longitude=decimal.Decimal('117.8301')
        )

        request = self.factory.get('search/', data={'location': self.location1.name})
        request.user = self.user
        self.view.request = request

    @patch('weather_app.views.WeatherApiService.get_locations_by_name')
    def test_search_queryset_success(self, mock_get_location):
        """
        Проверяем, что GET-запрос к поисковой странице:
         - вызывает WeatherApiService.get_locations_by_name с корректными параметрами,
         - возвращает в контекст список погоды (сформированный на основе результата сервиса).
        """
        mock_get_location.return_value = [self.location1.name]

        # Вызываем тестируемый метод get_queryset
        qs = self.view.get_queryset()

        # Проверяем, что возвращается список из одной записи
        self.assertEqual(len(qs), 1)
        # Сравниваем полученное имя локации с ожидаемым
        self.assertEqual(qs[0], self.location1.name)

        # Проверяем, что метод WeatherApiService.get_locations_by_name вызвался ровно один раз
        mock_get_location.assert_called_once_with(
            name=self.location1.name
        )

    def test_post_save_location(self):
        data = {
            'user': 'testuser',
            'country': 'RU',
            'name': 'Село Зеленое',
            'latitude': '36,2245',
            'longitude': '117,8305'
        }

        request = self.factory.post('search/', data=data)
        request.POST = data
        request.user = self.user
        request.session = {}
        # Устанавливаем фейковое хранилище сообщений, чтобы избежать ошибки MessageFailure
        setattr(request, '_messages', FallbackStorage(request))
        setattr(self.view, "request", request)
        response = self.view.post(request)

        # Проверяем, что объект локации был добавлен
        self.assertTrue(Location.objects.filter(name="Село Зеленое", user=self.user).exists())

        self.assertEqual(response.status_code, 302)
