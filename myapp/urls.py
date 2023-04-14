from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('findpet', views.findpet, name="findpet"),
    path('bookings', views.bookings, name="bookings"),
    path('cancellings', views.cancellings, name="cancellings"),
    path('seebookings', views.seebookings, name="seebookings"),
    path('deletebooking', views.deletebooking, name="deletebooking"),
    path('signup', views.signup, name="signup"),
    path('signin', views.signin, name="signin"),
    path('success', views.success, name="success"),
    path('signout', views.signout, name="signout"),
    path('download-pdf/<int:pk>', views.download_pdf_view,name='download-pdf'),

]
