from django.urls import reverse, resolve

from myapp import views


class TestUrls:
    def test_register_url_resolves(self):
        path = reverse('findpet')
        assert resolve(path).func == views.findpet

class TestUrls1:
    def test_register_url_resolves(self):
        path = reverse('bookings')
        assert resolve(path).func == views.bookings

class TestUrls2:
    def test_register_url_resolves(self):
        path = reverse('cancellings')
        assert resolve(path).func == views.cancellings

class TestUrls3:
    def test_register_url_resolves(self):
        path = reverse('seebookings')
        assert resolve(path).func == views.seebookings

class TestUrls4:
    def test_register_url_resolves(self):
        path = reverse('deletebooking')
        assert resolve(path).func == views.deletebooking

class TestUrls5:
    def test_register_url_resolves(self):
        path = reverse('signup')
        assert resolve(path).func == views.signup

class TestUrls6:
    def test_register_url_resolves(self):
        path = reverse('signin')
        assert resolve(path).func == views.signin

class TestUrls7:
    def test_register_url_resolves(self):
        path = reverse('success')
        assert resolve(path).func == views.success

class TestUrls8:
    def test_register_url_resolves(self):
        path = reverse('signout')
        assert resolve(path).func == views.signout
