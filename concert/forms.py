from django import forms
from django.forms import ModelForm, TextInput, Textarea, DateInput, NumberInput, DateTimeInput
from .models import Entertainer, City, Hall, Concert, Ticket, Application, Movement, Gallery, News
#from django.utils.translation import ugettext as _
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
import re
import datetime
from django.utils import timezone
import pytz

# При разработке приложения, использующего базу данных, чаще всего необходимо работать с формами, которые аналогичны моделям.
# В этом случае явное определение полей формы будет дублировать код, так как все поля уже описаны в модели.
# По этой причине Django предоставляет вспомогательный класс, который позволит вам создать класс Form по имеющейся модели
# атрибут fields - указание списка используемых полей, при fields = '__all__' - все поля
# атрибут widgets для указания собственный виджет для поля. Его значением должен быть словарь, ключами которого являются имена полей, а значениями — классы или экземпляры виджетов.
# Населенный пункт
class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ['title',]
        widgets = {
            'title': TextInput(attrs={"size":"100"}),            
        }
        labels = {
            'title': _('city_title'),            
        }
    # Метод-валидатор для поля title
    def clean_title(self):
        data = self.cleaned_data['title']
        # Ошибка если начинается не с большой буквы
        if data.istitle() == False:
            raise forms.ValidationError(_('Value must start with a capital letter'))
        # Метод-валидатор обязательно должен вернуть очищенные данные, даже если не изменил их
        return data

# Концертная площадка
class HallForm(forms.ModelForm):
    class Meta:
        model = Hall
        fields = ('city', 'title', 'capacity', 'photo')
        widgets = {
            'city': forms.Select(attrs={'class': 'chosen'}),
            'title': TextInput(attrs={"size":"100"}),
            'capacity': NumberInput(attrs={"size":"10", "min": "1", "step": "1"}),                    
        }
        labels = {
            'city': _('city'),
        }

        
# Артисты
class EntertainerForm(forms.ModelForm):
    class Meta:
        model = Entertainer
        fields = ('name', 'details', 'photo')
        widgets = {
            'name': TextInput(attrs={"size":"100"}),
            'details': Textarea(attrs={'cols': 100, 'rows': 10}),                        
        }

# Концерт
class ConcertForm(forms.ModelForm):
    class Meta:
        model = Concert
        fields = ('datec', 'entertainer', 'hall', 'price_min', 'price_max')
        widgets = {
            'datec': DateTimeInput(format='%d/%m/%Y %H:%M:%S'),
            'entertainer': forms.Select(attrs={'class': 'chosen'}),
            'hall': forms.Select(attrs={'class': 'chosen'}),
            'price_min': NumberInput(attrs={"size":"10", "min": "1", "step": "1"}),                    
            'price_max': NumberInput(attrs={"size":"10", "min": "1", "step": "1"}),                    
        }
        labels = {
            'entertainer': _('entertainer'),
            'hall': _('hall'),
        }
    # Метод-валидатор для поля datec
    def clean_datec(self):        
        if isinstance(self.cleaned_data['datec'], datetime.date) == True:
            data = self.cleaned_data['datec']
            #print(data)        
        else:
            raise forms.ValidationError(_('Wrong date and time format'))
        # Метод-валидатор обязательно должен вернуть очищенные данные, даже если не изменил их
        return data   

# Билеты
class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        #fields = ('concert', 'place', 'price', 'user')
        fields = ('place', 'price')
        widgets = {
            #'concert': forms.Select(attrs={'class': 'chosen'}),
            'place': TextInput(attrs={"size":"20"}),                  
            'Ticket': NumberInput(attrs={"size":"10", "min": "1", "step": "1"}),  
            #'user': forms.Select(attrs={'class': 'chosen'}),                              
        }
        #labels = {
        #    'concert': _('concert'),
        #    'user': _('user'),
        #}

# Заявки
class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ('title', 'details')
        widgets = {
            'title': TextInput(attrs={"size":"100"}),
            'details': Textarea(attrs={'cols': 100, 'rows': 10}),            
        }        

# Движение заявки
class MovementForm(forms.ModelForm):
    class Meta:
        model = Movement
        fields = ('datem', 'status', 'details')
        widgets = {
            'datem': DateInput(attrs={"type":"date", "readonly":"readonly"}),
            'status': TextInput(attrs={"size":"100"}),
            'details': Textarea(attrs={'cols': 100, 'rows': 10}),
        }

# Фотогалерея
class GalleryForm(forms.ModelForm):
    class Meta:
        model = Gallery
        fields = ('dateg', 'title', 'details', 'photo1', 'photo2', 'photo3', 'photo4', 'photo5')
        widgets = {
            'dateg': DateTimeInput(format='%d/%m/%Y %H:%M:%S'),
            'title': TextInput(attrs={"size":"100"}),
            'details': Textarea(attrs={'cols': 100, 'rows': 10}),                        
        }
    # Метод-валидатор для поля dateg
    def clean_dateg(self):        
        if isinstance(self.cleaned_data['dateg'], datetime.date) == True:
            data = self.cleaned_data['dateg']
            #print(data)        
        else:
            raise forms.ValidationError(_('Wrong date and time format'))
        # Метод-валидатор обязательно должен вернуть очищенные данные, даже если не изменил их
        return data   

# Новости
class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ('daten', 'title', 'details', 'photo')
        widgets = {
            'daten': DateTimeInput(format='%d/%m/%Y %H:%M:%S'),
            'title': TextInput(attrs={"size":"100"}),
            'details': Textarea(attrs={'cols': 100, 'rows': 10}),                        
        }
    # Метод-валидатор для поля daten
    def clean_daten(self):        
        if isinstance(self.cleaned_data['daten'], datetime.date) == True:
            data = self.cleaned_data['daten']
            #print(data)        
        else:
            raise forms.ValidationError(_('Wrong date and time format'))
        # Метод-валидатор обязательно должен вернуть очищенные данные, даже если не изменил их
        return data   

# Форма регистрации
class SignUpForm(UserCreationForm):
    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')
