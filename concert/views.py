from django.shortcuts import render, redirect

# Класс HttpResponse из пакета django.http, который позволяет отправить текстовое содержимое.
from django.http import HttpResponse, HttpResponseNotFound
# Конструктор принимает один обязательный аргумент – путь для перенаправления. Это может быть полный URL (например, 'https://www.yahoo.com/search/') или абсолютный путь без домена (например, '/search/').
from django.http import HttpResponseRedirect

from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages

from django.db.models import Max
from django.db.models import Q

from datetime import datetime, timedelta

# Отправка почты
from django.core.mail import send_mail

# Подключение моделей
from .models import Entertainer, City, Hall, Concert, Ticket, Application, Movement, Gallery, News
# Подключение форм
from .forms import CityForm, HallForm, EntertainerForm, ConcertForm, TicketForm, ApplicationForm, MovementForm, GalleryForm, NewsForm, SignUpForm

from django.db.models import Sum

from django.db import models

import sys

import math

#from django.utils.translation import ugettext as _
from django.utils.translation import gettext_lazy as _

from django.utils.decorators import method_decorator
from django.views.generic import UpdateView
from django.contrib.auth.models import User
from django.urls import reverse_lazy

from django.contrib.auth import login as auth_login

from django.db.models.query import QuerySet

# Подключаем модкль генерации случайных чисел
import random

# Create your views here.
# Групповые ограничения
def group_required(*group_names):
    """Requires user membership in at least one of the groups passed in."""
    def in_groups(u):
        if u.is_authenticated:
            if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
                return True
        return False
    return user_passes_test(in_groups, login_url='403')

###################################################################################################

# Стартовая страница 
def index(request):
    try:
        entertainer = Entertainer.objects.all().order_by('?')[0:4]
        concert = Concert.objects.all().order_by('-datec')[0:4]
        news1 = News.objects.all().order_by('-daten')[0:1]
        news23 = News.objects.all().order_by('-daten')[1:3]
        return render(request, "index.html", {"entertainer": entertainer, "concert": concert, "news1": news1, "news23": news23})            
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)    

# Контакты
def contact(request):
    try:
        return render(request, "contact.html")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

###################################################################################################

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def city_index(request):
    try:
        city = City.objects.all().order_by('title')
        return render(request, "city/index.html", {"city": city,})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
@group_required("Managers")
def city_create(request):
    try:
        if request.method == "POST":
            city = City()
            city.title = request.POST.get("title")
            cityform = CityForm(request.POST)
            if cityform.is_valid():
                city.save()
                return HttpResponseRedirect(reverse('city_index'))
            else:
                return render(request, "city/create.html", {"form": cityform})
        else:        
            cityform = CityForm()
            return render(request, "city/create.html", {"form": cityform})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Функция edit выполняет редактирование объекта.
@login_required
@group_required("Managers")
def city_edit(request, id):
    try:
        city = City.objects.get(id=id)
        if request.method == "POST":
            city.title = request.POST.get("title")
            cityform = CityForm(request.POST)
            if cityform.is_valid():
                city.save()
                return HttpResponseRedirect(reverse('city_index'))
            else:
                return render(request, "city/edit.html", {"form": cityform})
        else:
            # Загрузка начальных данных
            cityform = CityForm(initial={'title': city.title, })
            return render(request, "city/edit.html", {"form": cityform})
    except City.DoesNotExist:
        return HttpResponseNotFound("<h2>City not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def city_delete(request, id):
    try:
        city = City.objects.get(id=id)
        city.delete()
        return HttpResponseRedirect(reverse('city_index'))
    except City.DoesNotExist:
        return HttpResponseNotFound("<h2>City not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы read.html для просмотра объекта.
@login_required
@group_required("Managers")
def city_read(request, id):
    try:
        city = City.objects.get(id=id) 
        return render(request, "city/read.html", {"city": city})
    except City.DoesNotExist:
        return HttpResponseNotFound("<h2>City not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

###################################################################################################

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def hall_index(request):
    try:
        hall = Hall.objects.all().order_by('title')
        return render(request, "hall/index.html", {"hall": hall})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
@group_required("Managers")
def hall_create(request):
    try:
        if request.method == "POST":
            hall = Hall()        
            hall.city = City.objects.filter(id=request.POST.get("city")).first()
            hall.title = request.POST.get("title")
            hall.capacity = request.POST.get("capacity")
            if 'photo' in request.FILES:                
                hall.photo = request.FILES['photo']   
            hallform = HallForm(request.POST)
            if hallform.is_valid():
                hall.save()
                return HttpResponseRedirect(reverse('hall_index'))
            else:
                return render(request, "hall/create.html", {"form": hallform})
        else:        
            hallform = HallForm(initial={ 'capacity': 1000})
            return render(request, "hall/create.html", {"form": hallform})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Функция edit выполняет редактирование объекта.
# Функция в качестве параметра принимает идентификатор объекта в базе данных.
@login_required
@group_required("Managers")
def hall_edit(request, id):
    try:
        hall = Hall.objects.get(id=id) 
        if request.method == "POST":
            hall.city = City.objects.filter(id=request.POST.get("city")).first()
            hall.title = request.POST.get("title")
            hall.capacity = request.POST.get("capacity")
            if "photo" in request.FILES:                
                hall.photo = request.FILES["photo"]
            hallform = HallForm(request.POST)
            if hallform.is_valid():
                hall.save()
                return HttpResponseRedirect(reverse('hall_index'))
            else:
                return render(request, "hall/edit.html", {"form": hallform})
        else:
            # Загрузка начальных данных
            hallform = HallForm(initial={'city': hall.city, 'title': hall.title, 'capacity': hall.capacity, 'photo': hall.photo })
            return render(request, "hall/edit.html", {"form": hallform})
    except Hall.DoesNotExist:
        return HttpResponseNotFound("<h2>Hall not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def hall_delete(request, id):
    try:
        hall = Hall.objects.get(id=id)
        hall.delete()
        return HttpResponseRedirect(reverse('hall_index'))
    except Hall.DoesNotExist:
        return HttpResponseNotFound("<h2>Hall not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы read.html для просмотра объекта.
#@login_required
def hall_read(request, id):
    try:
        hall = Hall.objects.get(id=id) 
        return render(request, "hall/read.html", {"hall": hall})
    except Hall.DoesNotExist:
        return HttpResponseNotFound("<h2>Hall not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

###################################################################################################

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def entertainer_index(request):
    try:
        entertainer = Entertainer.objects.all().order_by('name')
        return render(request, "entertainer/index.html", {"entertainer": entertainer})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Список для просмотра
def entertainer_list(request):
    try:
        entertainer = Entertainer.objects.all().order_by('name')
        return render(request, "entertainer/list.html", {"entertainer": entertainer})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
@group_required("Managers")
def entertainer_create(request):
    try:
        if request.method == "POST":
            entertainer = Entertainer()        
            entertainer.name = request.POST.get("name")
            entertainer.details = request.POST.get("details")
            if 'photo' in request.FILES:                
                entertainer.photo = request.FILES['photo']   
            entertainerform = EntertainerForm(request.POST)
            if entertainerform.is_valid():
                entertainer.save()
                return HttpResponseRedirect(reverse('entertainer_index'))
            else:
                return render(request, "entertainer/create.html", {"form": entertainerform})
        else:        
            entertainerform = EntertainerForm()
            return render(request, "entertainer/create.html", {"form": entertainerform})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Функция edit выполняет редактирование объекта.
# Функция в качестве параметра принимает идентификатор объекта в базе данных.
@login_required
@group_required("Managers")
def entertainer_edit(request, id):
    try:
        entertainer = Entertainer.objects.get(id=id) 
        if request.method == "POST":
            entertainer.name = request.POST.get("name")
            entertainer.details = request.POST.get("details")
            if "photo" in request.FILES:                
                entertainer.photo = request.FILES["photo"]
            entertainerform = EntertainerForm(request.POST)
            if entertainerform.is_valid():
                entertainer.save()
                return HttpResponseRedirect(reverse('entertainer_index'))
            else:
                return render(request, "entertainer/edit.html", {"form": entertainerform})
        else:
            # Загрузка начальных данных
            entertainerform = EntertainerForm(initial={'name': entertainer.name, 'details': entertainer.details, 'photo': entertainer.photo })
            return render(request, "entertainer/edit.html", {"form": entertainerform})
    except Entertainer.DoesNotExist:
        return HttpResponseNotFound("<h2>Entertainer not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def entertainer_delete(request, id):
    try:
        entertainer = Entertainer.objects.get(id=id)
        entertainer.delete()
        return HttpResponseRedirect(reverse('entertainer_index'))
    except Entertainer.DoesNotExist:
        return HttpResponseNotFound("<h2>Entertainer not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы read.html для просмотра объекта.
#@login_required
def entertainer_read(request, id):
    try:
        entertainer = Entertainer.objects.get(id=id) 
        return render(request, "entertainer/read.html", {"entertainer": entertainer})
    except Entertainer.DoesNotExist:
        return HttpResponseNotFound("<h2>Entertainer not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

###################################################################################################

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def concert_index(request):
    try:
        concert = Concert.objects.all().order_by('datec')
        return render(request, "concert/index.html", {"concert": concert})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Список для просмотра
def concert_list(request):
    try:
        # Категории и подкатегория товара (для поиска)
        entertainer = Entertainer.objects.all().order_by('name')
        city = City.objects.all().order_by('title')
        concert = Concert.objects.all().order_by('datec')
        if request.method == "POST":
            # Определить какая кнопка нажата
            if 'searchBtn' in request.POST:
                # Поиск по артисту
                selected_item_entertainer = request.POST.get('item_entertainer')
                #print(selected_item_entertainer)
                if selected_item_entertainer != '-----':
                    entertainer_query = Entertainer.objects.filter(name = selected_item_entertainer).only('id').all()
                    concert = concert.filter(entertainer_id__in = entertainer_query).all()
                # Поиск по городу
                selected_item_city = request.POST.get('item_city')
                print(selected_item_city)
                if selected_item_city != '-----':
                    city_query = City.objects.filter(title = selected_item_city).only('id').all()
                    hall_query = Hall.objects.filter(city_id__in = city_query).only('id').all()
                    concert = concert.filter(hall_id__in = hall_query).all()
                
                return render(request, "concert/list.html", {"concert": concert, "entertainer": entertainer, "selected_item_entertainer": selected_item_entertainer,  "city": city, "selected_item_city": selected_item_city, })    
            else:          
                return render(request, "concert/list.html", {"concert": concert, "entertainer": entertainer, "city": city, })
        else:
            return render(request, "concert/list.html", {"concert": concert, "entertainer": entertainer, "city": city, })           
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
@group_required("Managers")
def concert_create(request):
    try:
        if request.method == "POST":
            concert = Concert()      
            concert.datec = request.POST.get("datec")
            concert.entertainer = Entertainer.objects.filter(id=request.POST.get("entertainer")).first()
            concert.hall = Hall.objects.filter(id=request.POST.get("hall")).first()
            concert.price_min = request.POST.get("price_min")
            concert.price_max = request.POST.get("price_max")
            concertform = ConcertForm(request.POST)
            if concertform.is_valid():
                concert.save()
                return HttpResponseRedirect(reverse('concert_index'))
            else:
                return render(request, "concert/create.html", {"form": concertform})
        else:        
            concertform = ConcertForm(initial={'datec': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'price_min': 1000, 'price_max': 2000, })
            return render(request, "concert/create.html", {"form": concertform})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Функция edit выполняет редактирование объекта.
# Функция в качестве параметра принимает идентификатор объекта в базе данных.
@login_required
@group_required("Managers")
def concert_edit(request, id):
    try:
        concert = Concert.objects.get(id=id) 
        if request.method == "POST":
            concert.datec = request.POST.get("datec")
            concert.entertainer = Entertainer.objects.filter(id=request.POST.get("entertainer")).first()
            concert.hall = Hall.objects.filter(id=request.POST.get("hall")).first()
            concert.price_min = request.POST.get("price_min")
            concert.price_max = request.POST.get("price_max")
            concertform = ConcertForm(request.POST)
            if concertform.is_valid():
                concert.save()
                return HttpResponseRedirect(reverse('concert_index'))
            else:
                return render(request, "concert/edit.html", {"form": concertform})
        else:
            # Загрузка начальных данных
            concertform = ConcertForm(initial={'datec': concert.datec.strftime('%Y-%m-%d %H:%M:%S'), 'entertainer': concert.entertainer, 'hall': concert.hall, 'price_min': concert.price_min, 'price_max': concert.price_max })
            return render(request, "concert/edit.html", {"form": concertform})
    except Concert.DoesNotExist:
        return HttpResponseNotFound("<h2>Concert not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def concert_delete(request, id):
    try:
        concert = Concert.objects.get(id=id)
        concert.delete()
        return HttpResponseRedirect(reverse('concert_index'))
    except Concert.DoesNotExist:
        return HttpResponseNotFound("<h2>Concert not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы read.html для просмотра объекта.
#@login_required
def concert_read(request, id):
    try:
        concert = Concert.objects.get(id=id) 
        return render(request, "concert/read.html", {"concert": concert})
    except Concert.DoesNotExist:
        return HttpResponseNotFound("<h2>Concert not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

###################################################################################################

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def ticket_index(request):
    try:
        ticket = Ticket.objects.all().order_by('-datet')
        return render(request, "ticket/index.html", {"ticket": ticket})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Список для просмотра
@login_required
def ticket_list(request):
    try:        
        print(request.user.id)
        first_name = request.user.first_name
        last_name = request.user.last_name
        email = request.user.email
        ticket = Ticket.objects.filter(user_id=request.user.id).order_by('-datet')
        return render(request, "ticket/list.html", {"ticket": ticket, 'first_name': first_name, 'last_name': last_name, 'email': email})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
#@group_required("Managers")
def ticket_create(request, concert_id):
    try:
        concert = Concert.objects.get(id=concert_id) 
        price_min = concert.price_min;
        price_max = concert.price_max;
        if request.method == "POST":
            ticket = Ticket()      
            ticket.concert_id = concert_id
            ticket.place = request.POST.get("place")
            ticket.price = request.POST.get("price")
            ticket.user_id = request.user.id
            ticketform = TicketForm(request.POST)
            if ticketform.is_valid():
                ticket.save()
                return HttpResponseRedirect(reverse('ticket_list'))
            else:
                return render(request, "ticket/create.html", {"form": ticketform, "concert": concert})
        else:        
            ticketform = TicketForm(initial={'place': str(random.randint(1, 15)) + "-" + str(random.randint(1, 15)), 'price': price_min, })
            return render(request, "ticket/create.html", {"form": ticketform, "concert": concert})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Функция edit выполняет редактирование объекта.
# Функция в качестве параметра принимает идентификатор объекта в базе данных.
@login_required
@group_required("Managers")
def ticket_edit(request, id):
    try:
        ticket = Ticket.objects.get(id=id) 
        if request.method == "POST":
            ticket.concert = Concert.objects.filter(id=request.POST.get("concert")).first()
            ticket.place = request.POST.get("place")
            ticket.price = request.POST.get("price")
            ticket.user_id = request.user.id
            ticketform = TicketForm(request.POST)
            if ticketform.is_valid():
                ticket.save()
                return HttpResponseRedirect(reverse('ticket_index'))
            else:
                return render(request, "ticket/edit.html", {"form": ticketform})
        else:
            # Загрузка начальных данных
            ticketform = TicketForm(initial={'concert': ticket.concert, 'place': ticket.place, 'price': ticket.price , 'user': ticket.user })
            return render(request, "ticket/edit.html", {"form": ticketform})
    except Ticket.DoesNotExist:
        return HttpResponseNotFound("<h2>Ticket not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def ticket_delete(request, id):
    try:
        ticket = Ticket.objects.get(id=id)
        ticket.delete()
        return HttpResponseRedirect(reverse('ticket_index'))
    except Ticket.DoesNotExist:
        return HttpResponseNotFound("<h2>Ticket not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы read.html для просмотра объекта.
#@login_required
def ticket_read(request, id):
    try:
        ticket = Ticket.objects.get(id=id) 
        return render(request, "ticket/read.html", {"ticket": ticket})
    except Ticket.DoesNotExist:
        return HttpResponseNotFound("<h2>Ticket not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

###################################################################################################

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def application_index(request):
    try:
        application = Application.objects.all().order_by('datea')
        return render(request, "application/index.html", {"application": application})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Список 
@login_required
def application_list(request):
    try:
        #print(request.user.id)
        first_name = request.user.first_name
        last_name = request.user.last_name
        email = request.user.email
        application = Application.objects.filter(user_id=request.user.id).order_by('-datea')
        return render(request, "application/list.html", {"application": application, 'first_name': first_name, 'last_name': last_name, 'email': email})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)
    
# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
#@group_required("Managers")
def application_create(request):
    try:
        if request.method == "POST":
            application = Application()
            application.title = request.POST.get("title")
            application.details = request.POST.get("details")
            application.user_id = request.user.id
            applicationform = ApplicationForm(request.POST)
            if applicationform.is_valid():
                application.save()
                return HttpResponseRedirect(reverse('application_list'))
            else:
                return render(request, "application/create.html", {"form": applicationform})
        else:        
            applicationform = ApplicationForm()
            return render(request, "application/create.html", {"form": applicationform})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Функция edit выполняет редактирование объекта.
@login_required
@group_required("Managers")
def application_edit(request, id):
    try:
        application = Application.objects.get(id=id) 
        if request.method == "POST":
            application.title = request.POST.get("title")
            application.details = request.POST.get("details")
            applicationform = ApplicationForm(request.POST)
            if applicationform.is_valid():
                application.save()
                return HttpResponseRedirect(reverse('application_index'))
            else:
                return render(request, "application/edit.html", {"form": applicationform})
        else:
            # Загрузка начальных данных
            applicationform = ApplicationForm(initial={'title': application.title, 'details': application.details, })
            return render(request, "application/edit.html", {"form": applicationform})
    except Application.DoesNotExist:
        return HttpResponseNotFound("<h2>Application not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def application_delete(request, id):
    try:
        application = Application.objects.get(id=id)
        application.delete()
        return HttpResponseRedirect(reverse('application_index'))
    except Application.DoesNotExist:
        return HttpResponseNotFound("<h2>Application not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы read.html для просмотра объекта.
@login_required
def application_read(request, id):
    try:
        application = Application.objects.get(id=id)
        movement = Movement.objects.filter(application_id=id).order_by('-datem')
        return render(request, "application/read.html", {"application": application, "movement": movement})
    except Application.DoesNotExist:
        return HttpResponseNotFound("<h2>Application not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

###################################################################################################

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def movement_index(request, application_id):
    try:
        movement = Movement.objects.filter(application_id=application_id).order_by('-datem')
        app = Application.objects.get(id=application_id)
        #movement = Movement.objects.all().order_by('-orders', '-datem')
        return render(request, "movement/index.html", {"movement": movement, "application_id": application_id, "app": app})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
@group_required("Managers")
def movement_create(request, application_id):
    try:
        app = Application.objects.get(id=application_id)
        if request.method == "POST":
            movement = Movement()
            movement.application_id = application_id
            movement.datem = datetime.now()
            movement.status = request.POST.get("status")
            movement.details = request.POST.get("details")
            movementform = MovementForm(request.POST)
            if movementform.is_valid():
                movement.save()
                return HttpResponseRedirect(reverse('movement_index', args=(application_id,)))
            else:
                return render(request, "application/create.html", {"form": movementform})
        else:
            movementform = MovementForm(initial={ 'datem': datetime.now().strftime('%Y-%m-%d')})
            return render(request, "movement/create.html", {"form": movementform, "application_id": application_id, "app": app})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Функция edit выполняет редактирование объекта.
@login_required
@group_required("Managers")
def movement_edit(request, id, application_id):
    app = Application.objects.get(id=application_id)
    try:
        movement = Movement.objects.get(id=id) 
        if request.method == "POST":
            #movement.datem = datetime.now()
            movement.status = request.POST.get("status")
            movement.details = request.POST.get("details")
            movementform = MovementForm(request.POST)
            if movementform.is_valid():
                movement.save()
                return HttpResponseRedirect(reverse('movement_index', args=(application_id,)))
            else:
                return render(request, "application/edit.html", {"form": movementform})
        else:
            # Загрузка начальных данных
            movementform = MovementForm(initial={'application': movement.application, 'datem': movement.datem.strftime('%Y-%m-%d'), 'status': movement.status, 'details': movement.details,  })
            return render(request, "movement/edit.html", {"form": movementform, "application_id": application_id, "app": app})
    except Movement.DoesNotExist:
        return HttpResponseNotFound("<h2>Movement not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def movement_delete(request, id, application_id):
    try:
        movement = Movement.objects.get(id=id)
        movement.delete()
        return HttpResponseRedirect(reverse('movement_index', args=(application_id,)))
    except Movement.DoesNotExist:
        return HttpResponseNotFound("<h2>Movement not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы read.html для просмотра объекта.
@login_required
def movement_read(request, id, application_id):
    try:
        movement = Movement.objects.get(id=id) 
        return render(request, "movement/read.html", {"movement": movement, "application_id": application_id})
    except Movement.DoesNotExist:
        return HttpResponseNotFound("<h2>Movement not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

###################################################################################################

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def gallery_index(request):
    try:
        gallery = Gallery.objects.all().order_by('-dateg')
        return render(request, "gallery/index.html", {"gallery": gallery})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Список для просмотра
def gallery_list(request):
    try:
        gallery = Gallery.objects.all().order_by('-dateg')
        if request.method == "POST":
            # Определить какая кнопка нажата
            if 'searchBtn' in request.POST:
                # Поиск по названию 
                gallery_search = request.POST.get("gallery_search")
                #print(gallery_search)                
                if gallery_search != '':
                    gallery = gallery.filter(title__contains = gallery_search).all()                
                return render(request, "gallery/list.html", {"gallery": gallery, "gallery_search": gallery_search, })    
            else:          
                return render(request, "gallery/list.html", {"gallery": gallery})                 
        else:
            return render(request, "gallery/list.html", {"gallery": gallery})                 
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
@group_required("Managers")
def gallery_create(request):
    try:
        if request.method == "POST":
            gallery = Gallery()        
            gallery.dateg = request.POST.get("dateg")
            gallery.title = request.POST.get("title")
            gallery.details = request.POST.get("details")
            if 'photo1' in request.FILES:                
                gallery.photo1 = request.FILES['photo1']   
            if 'photo2' in request.FILES:                
                gallery.photo2 = request.FILES['photo2']   
            if 'photo3' in request.FILES:                
                gallery.photo3 = request.FILES['photo3']   
            if 'photo4' in request.FILES:                
                gallery.photo4 = request.FILES['photo4']   
            if 'photo5' in request.FILES:                
                gallery.photo5 = request.FILES['photo5']   
            galleryform = GalleryForm(request.POST)
            if galleryform.is_valid():
                gallery.save()
                return HttpResponseRedirect(reverse('gallery_index'))
            else:
                return render(request, "gallery/create.html", {"form": galleryform})
        else:        
            galleryform = GalleryForm(initial={'dateg': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), })
            return render(request, "gallery/create.html", {"form": galleryform})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Функция edit выполняет редактирование объекта.
# Функция в качестве параметра принимает идентификатор объекта в базе данных.
@login_required
@group_required("Managers")
def gallery_edit(request, id):
    try:
        gallery = Gallery.objects.get(id=id) 
        if request.method == "POST":
            gallery.dateg = request.POST.get("dateg")
            gallery.title = request.POST.get("title")
            gallery.details = request.POST.get("details")
            if "photo1" in request.FILES:                
                gallery.photo1 = request.FILES["photo1"]
            if 'photo2' in request.FILES:                
                gallery.photo2 = request.FILES['photo2'] 
            if 'photo3' in request.FILES:                
                gallery.photo3 = request.FILES['photo3']   
            if 'photo4' in request.FILES:                
                gallery.photo4 = request.FILES['photo4']   
            if 'photo5' in request.FILES:                
                gallery.photo5 = request.FILES['photo5']   
            galleryform = GalleryForm(request.POST)
            if galleryform.is_valid():
                gallery.save()
                return HttpResponseRedirect(reverse('gallery_index'))
            else:
                return render(request, "gallery/edit.html", {"form": galleryform})
        else:
            # Загрузка начальных данных
            galleryform = GalleryForm(initial={'dateg': gallery.dateg.strftime('%Y-%m-%d %H:%M:%S'), 'title': gallery.title, 'details': gallery.details, 'photo1': gallery.photo1 , 'photo2': gallery.photo2 , 'photo3': gallery.photo3 , 'photo4': gallery.photo4 , 'photo5': gallery.photo5 })
            return render(request, "gallery/edit.html", {"form": galleryform})
    except Gallery.DoesNotExist:
        return HttpResponseNotFound("<h2>Gallery not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def gallery_delete(request, id):
    try:
        gallery = Gallery.objects.get(id=id)
        gallery.delete()
        return HttpResponseRedirect(reverse('gallery_index'))
    except Gallery.DoesNotExist:
        return HttpResponseNotFound("<h2>Gallery not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы read.html для просмотра объекта.
#@login_required
def gallery_read(request, id):
    try:
        gallery = Gallery.objects.get(id=id) 
        return render(request, "gallery/read.html", {"gallery": gallery})
    except Gallery.DoesNotExist:
        return HttpResponseNotFound("<h2>Gallery not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

###################################################################################################

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def news_index(request):
    try:
        news = News.objects.all().order_by('-daten')
        return render(request, "news/index.html", {"news": news})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Список для просмотра
def news_list(request):
    try:
        news = News.objects.all().order_by('-daten')
        if request.method == "POST":
            # Определить какая кнопка нажата
            if 'searchBtn' in request.POST:
                # Поиск по названию 
                news_search = request.POST.get("news_search")
                #print(news_search)                
                if news_search != '':
                    news = news.filter(Q(title__contains = news_search) | Q(details__contains = news_search)).all()                
                return render(request, "news/list.html", {"news": news, "news_search": news_search, })    
            else:          
                return render(request, "news/list.html", {"news": news})                 
        else:
            return render(request, "news/list.html", {"news": news}) 
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
@group_required("Managers")
def news_create(request):
    try:
        if request.method == "POST":
            news = News()        
            news.daten = request.POST.get("daten")
            news.title = request.POST.get("title")
            news.details = request.POST.get("details")
            if 'photo' in request.FILES:                
                news.photo = request.FILES['photo']   
            newsform = NewsForm(request.POST)
            if newsform.is_valid():
                news.save()
                return HttpResponseRedirect(reverse('news_index'))
            else:
                return render(request, "news/create.html", {"form": newsform})
        else:        
            newsform = NewsForm(initial={'daten': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), })
            return render(request, "news/create.html", {"form": newsform})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Функция edit выполняет редактирование объекта.
# Функция в качестве параметра принимает идентификатор объекта в базе данных.
@login_required
@group_required("Managers")
def news_edit(request, id):
    try:
        news = News.objects.get(id=id) 
        if request.method == "POST":
            news.daten = request.POST.get("daten")
            news.title = request.POST.get("title")
            news.details = request.POST.get("details")
            if "photo" in request.FILES:                
                news.photo = request.FILES["photo"]
            newsform = NewsForm(request.POST)
            if newsform.is_valid():
                news.save()
                return HttpResponseRedirect(reverse('news_index'))
            else:
                return render(request, "news/edit.html", {"form": newsform})
        else:
            # Загрузка начальных данных
            newsform = NewsForm(initial={'daten': news.daten.strftime('%Y-%m-%d %H:%M:%S'), 'title': news.title, 'details': news.details, 'photo': news.photo })
            return render(request, "news/edit.html", {"form": newsform})
    except News.DoesNotExist:
        return HttpResponseNotFound("<h2>News not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def news_delete(request, id):
    try:
        news = News.objects.get(id=id)
        news.delete()
        return HttpResponseRedirect(reverse('news_index'))
    except News.DoesNotExist:
        return HttpResponseNotFound("<h2>News not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы read.html для просмотра объекта.
#@login_required
def news_read(request, id):
    try:
        news = News.objects.get(id=id) 
        return render(request, "news/read.html", {"news": news})
    except News.DoesNotExist:
        return HttpResponseNotFound("<h2>News not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

###################################################################################################    

# Регистрационная форма 
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('index')
            #return render(request, 'registration/register_done.html', {'new_user': user})
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

# Изменение данных пользователя
@method_decorator(login_required, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = ('first_name', 'last_name', 'email',)
    template_name = 'registration/my_account.html'
    success_url = reverse_lazy('index')
    #success_url = reverse_lazy('my_account')
    def get_object(self):
        return self.request.user

# Выход
from django.contrib.auth import logout
def logoutUser(request):
    logout(request)
    return render(request, "index.html")