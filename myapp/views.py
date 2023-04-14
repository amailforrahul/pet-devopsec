from django.shortcuts import render
from decimal import Decimal

# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import User, pet, Book
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import UserLoginForm, UserRegisterForm
from django.contrib.auth.decorators import login_required
from decimal import Decimal

import io
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context


def home(request):
    if request.user.is_authenticated:
        return render(request, 'myapp/home.html')
    else:
        return render(request, 'myapp/signin.html')


@login_required(login_url='signin')
def findpet(request):
    context = {}
    if request.method == 'POST':
        pet_type_r = request.POST.get('pet_type')
        pet_breed_r = request.POST.get('pet_breed')
        pet_location_r = request.POST.get('pet_location')

        pet_list = pet.objects.filter(pet_type=pet_type_r, pet_breed=pet_breed_r, pet_location=pet_location_r)
        if pet_list:
            return render(request, 'myapp/list.html', locals())
        else:
            context["error"] = "Sorry no pets available this time"
            return render(request, 'myapp/findpet.html', context)
    else:
        return render(request, 'myapp/findpet.html')


@login_required(login_url='signin')
def bookings(request):
    context = {}
    if request.method == 'POST':
        pet_id_r = request.POST.get('pet_id')
        no_pets_r = int(request.POST.get('no_pets'))
        obj_pet = pet.objects.get(id=pet_id_r)
        if obj_pet:
            if obj_pet.pet_rem > int(no_pets_r):

                pet_type_r = obj_pet.pet_type
                cost = int(no_pets_r) * obj_pet.pet_price

                pet_breed_r = obj_pet.pet_breed
                pet_location_r = obj_pet.pet_location
                pet_bloodline_r = obj_pet.pet_bloodline

                pet_nos_r = Decimal(obj_pet.pet_nos)
                pet_price_r = obj_pet.pet_price
                date_r = obj_pet.date
                time_r = obj_pet.time

                username_r = request.user.username
                email_r = request.user.email
                userid_r = request.user.id

                pet_rem_r = obj_pet.pet_rem - no_pets_r

                pet.objects.filter(id=pet_id_r).update(pet_rem=pet_rem_r)

                book = Book.objects.create(name=username_r, email=email_r, userid=userid_r, pet_type=pet_type_r,
                                           pet_breed=pet_breed_r, pet_location=pet_location_r,
                                           pet_bloodline=pet_bloodline_r, pet_id=pet_id_r, pet_price=pet_price_r,
                                           pet_nos=no_pets_r,
                                           date=date_r, time=time_r, status='BOOKED')

                print('------------book id-----------', book.pet_id)
                # book.save()
                return render(request, 'myapp/bookings.html', locals())
            else:
                context["error"] = "Sorry select fewer number of seats"
                return render(request, 'myapp/findpet.html', context)

    else:
        return render(request, 'myapp/findpet.html')


@login_required(login_url='signin')
def cancellings(request):
    context = {}
    if request.method == 'POST':
        id_r = request.POST.get('pet_id')
        # seats_r = int(request.POST.get('no_seats'))

        try:
            book_obj = Book.objects.get(id=id_r)
            pet_obj = pet.objects.get(id=book_obj.pet_id)

            rem_r = pet_obj.pet_rem + book_obj.pet_nos
            pet.objects.filter(id=book_obj.pet_id).update(pet_rem=rem_r)
            # nos_r = book.nos - seats_r

            Book.objects.filter(id=id_r).update(status='CANCELLED')
            Book.objects.filter(id=id_r).update(pet_nos=0)
            return redirect(seebookings)
        except Book.DoesNotExist:
            context["error"] = "Sorry You have not booked that Pet"
            return render(request, 'myapp/error.html', context)
    else:
        return render(request, 'myapp/findpet.html')

@login_required(login_url='signin')
def deletebooking(request):
    context = {}
    if request.method == 'POST':
        id_r = request.POST.get('pet_idd')
        # seats_r = int(request.POST.get('no_seats'))

        try:
            book_obj = Book.objects.get(id=id_r)

            pet_obj = pet.objects.get(id=book_obj.pet_id)
            rem_r = pet_obj.pet_rem + book_obj.pet_nos
            pet.objects.filter(id=book_obj.pet_id).update(pet_rem=rem_r)
            # nos_r = book.nos - seats_r

            Book.objects.filter(id=id_r).delete()
            Book.objects.filter(id=id_r).update(pet_nos=0)
            return redirect(seebookings)

        except Book.DoesNotExist:
            context["error"] = "Sorry You have not booked that Pet"
            return render(request, 'myapp/error.html', context)
    else:
        return render(request, 'myapp/findpet.html')

@login_required(login_url='signin')
def seebookings(request, new={}):
    context = {}
    id_r = request.user.id
    book_list = Book.objects.filter(userid=id_r)
    if book_list:
        return render(request, 'myapp/booklist.html', locals())
    else:
        context["error"] = "Sorry no Pet booked"
        return render(request, 'myapp/findpet.html', context)


def signup(request):
    context = {}
    if request.method == 'POST':
        name_r = request.POST.get('name')
        email_r = request.POST.get('email')
        password_r = request.POST.get('password')
        user = User.objects.create_user(name_r, email_r, password_r, )
        if user:
            login(request, user)
            return render(request, 'myapp/thank.html')
        else:
            context["error"] = "Provide valid credentials"
            return render(request, 'myapp/signup.html', context)
    else:
        return render(request, 'myapp/signup.html', context)


def signin(request):
    context = {}
    if request.method == 'POST':
        name_r = request.POST.get('name')
        password_r = request.POST.get('password')
        user = authenticate(request, username=name_r, password=password_r)
        if user:
            login(request, user)
            # username = request.session['username']
            context["user"] = name_r
            context["id"] = request.user.id
            return render(request, 'myapp/success.html', context)
            # return HttpResponseRedirect('success')
        else:
            context["error"] = "Provide valid credentials"
            return render(request, 'myapp/signin.html', context)
    else:
        context["error"] = "You are not logged in"
        return render(request, 'myapp/signin.html', context)


def signout(request):
    context = {}
    logout(request)
    context['error'] = "You have been logged out"
    return render(request, 'myapp/signin.html', context)


def success(request):
    context = {}
    context['user'] = request.user
    return render(request, 'myapp/success.html', context)


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return


def download_pdf_view(request, pk):
    book = Book.objects.filter(id=pk)
    print(book)
    # dischargeDetails=models.PatientDischargeDetails.objects.all().filter(patientId=pk).order_by('-id')[:1]
    dict = {

        'id': book[0].pet_id,

        'pet_type': book[0].pet_type,

        'pet_breed': book[0].pet_breed,

        'pet_location': book[0].pet_location,

        'pet_bloodline': book[0].pet_bloodline,

        'pet_nos': book[0].pet_nos,

        'pet_price': book[0].pet_price,

        'date': book[0].date,

        'id': book[0].id,

        'comments': book[0].id,
    }
    return render_to_pdf('myapp/download_bill.html', dict)
