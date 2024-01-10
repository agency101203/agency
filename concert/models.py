from django.db import models
#from django.utils.translation import ugettext as _
from django.utils.translation import gettext_lazy as _
from PIL import Image
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

from django.contrib.auth.models import User

# Модели отображают информацию о данных, с которыми вы работаете.
# Они содержат поля и поведение ваших данных.
# Обычно одна модель представляет одну таблицу в базе данных.
# Каждая модель это класс унаследованный от django.db.models.Model.
# Атрибут модели представляет поле в базе данных.
# Django предоставляет автоматически созданное API для доступа к данным

# choices (список выбора). Итератор (например, список или кортеж) 2-х элементных кортежей,
# определяющих варианты значений для поля.
# При определении, виджет формы использует select вместо стандартного текстового поля
# и ограничит значение поля указанными значениями.

# Читабельное имя поля (метка, label). Каждое поле, кроме ForeignKey, ManyToManyField и OneToOneField,
# первым аргументом принимает необязательное читабельное название.
# Если оно не указано, Django самостоятельно создаст его, используя название поля, заменяя подчеркивание на пробел.
# null - Если True, Django сохранит пустое значение как NULL в базе данных. По умолчанию - False.
# blank - Если True, поле не обязательно и может быть пустым. По умолчанию - False.
# Это не то же что и null. null относится к базе данных, blank - к проверке данных.
# Если поле содержит blank=True, форма позволит передать пустое значение.
# При blank=False - поле обязательно.

# Эстрадный исполнитель
class Entertainer(models.Model):
    name = models.CharField(_('entertainer_name'), max_length=128)
    details = models.TextField(_('entertainer_details'))
    photo = models.ImageField(_('entertainer_photo'), upload_to='images/', blank=True, null=True)    
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'entertainer'
        # indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['name']),
        ]
        # Сортировка по умолчанию
        ordering = ['name']
    def __str__(self):
        # Вывод в тег Select 
        return "{}".format(self.name)

# Населенный пункт 
class City(models.Model):
    title = models.CharField(_('city_title'), max_length=128, unique=True)
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'city'
        # indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['title']),
        ]
        # Сортировка по умолчанию
        ordering = ['title']
    def __str__(self):
        # Вывод в тег Select 
        return "{}".format(self.title)

# Концертная площадка
class Hall(models.Model):
    city = models.ForeignKey(City, related_name='hall_city', on_delete=models.CASCADE)
    title = models.CharField(_('hall_title'), max_length=128)
    capacity = models.IntegerField(_('capacity'))  
    photo = models.ImageField(_('hall_photo'), upload_to='images/', blank=True, null=True)    
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'hall'
		# indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['city']),
            models.Index(fields=['title']),
        ]
        # Сортировка по умолчанию
        ordering = ['title']
    def __str__(self):
        # Вывод в тег Select
        return "{}, {}".format(self.city, self.title)

# Концерт
class Concert(models.Model):
    datec = models.DateTimeField(_('datec'))
    entertainer = models.ForeignKey(Entertainer, related_name='concert_entertainer', on_delete=models.CASCADE)
    hall = models.ForeignKey(Hall, related_name='concert_hall', on_delete=models.CASCADE)
    price_min = models.DecimalField(_('price_min'), max_digits=9, decimal_places=2)
    price_max = models.DecimalField(_('price_max'), max_digits=9, decimal_places=2)
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'concert'
		# indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['datec']),
            models.Index(fields=['entertainer']),
            models.Index(fields=['hall']),
        ]
        # Сортировка по умолчанию
        ordering = ['datec']
    def __str__(self):
        # Вывод в тег Select
        return "{}, {} {}".format(self.entertainer, self.datec.strftime('%d.%m.%Y %H:%M'), self.hall)

# Продажа билетов на концерт
class Ticket(models.Model):
    concert = models.ForeignKey(Concert, related_name='ticket_concert', on_delete=models.CASCADE)
    place = models.CharField(_('place'), max_length=64)
    price = models.DecimalField(_('price'), max_digits=9, decimal_places=2)
    user = models.ForeignKey(User, related_name='ticket_user', on_delete=models.CASCADE)
    datet = models.DateTimeField(_('datet'), auto_now_add=True)
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'ticket'
		# indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['concert']),
            models.Index(fields=['user']),
            models.Index(fields=['datet']),
        ]
        # Сортировка по умолчанию
        ordering = ['datet']
    def __str__(self):
        # Вывод в тег Select
        return "{}: {}, {}".format(self.date, self.entertainer, self.hall)

# Заявка клиента
class Application(models.Model):
    datea = models.DateTimeField(_('datea'), auto_now_add=True)
    user = models.ForeignKey(User, related_name='application_user', on_delete=models.CASCADE)
    title = models.CharField(_('application_title'), max_length=255)
    details = models.TextField(_('application_details'))
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'application'
        # indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['datea']),
            models.Index(fields=['user']),
        ]
        # Сортировка по умолчанию
        ordering = ['datea']
    def __str__(self):
        # Вывод в тег Select
        return "{} ({}): {}".format(self.datea.strftime('%d.%m.%Y'), self.user, self.title)

# Рассмотрение заявки клиента
class Movement(models.Model):
    application = models.ForeignKey(Application, related_name='movement_application', on_delete=models.CASCADE)
    datem = models.DateTimeField(_('datem'))
    status = models.CharField(_('movement_status'), max_length=128)
    details = models.TextField(_('movement_details'), blank=True, null=True)
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'movement'
        # indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['application']),
            models.Index(fields=['datem']),
        ]
        # Сортировка по умолчанию
        ordering = ['datem']        
    def __str__(self):
        # Вывод в тег Select
        return "{} ({}): {}".format(self.datem.strftime('%d.%m.%Y'), self.application, self.status)

# Фотогалерея 
class Gallery(models.Model):
    dateg = models.DateTimeField(_('dateg'))
    title = models.CharField(_('gallery_title'), max_length=256)
    details = models.TextField(_('gallery_details'))
    photo1 = models.ImageField(_('gallery_photo'), upload_to='images/', blank=True, null=True)    
    photo2 = models.ImageField(_('gallery_photo'), upload_to='images/', blank=True, null=True)    
    photo3 = models.ImageField(_('gallery_photo'), upload_to='images/', blank=True, null=True)    
    photo4 = models.ImageField(_('gallery_photo'), upload_to='images/', blank=True, null=True)    
    photo5 = models.ImageField(_('gallery_photo'), upload_to='images/', blank=True, null=True)    
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'gallery'
        # indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['dateg']),
        ]
        # Сортировка по умолчанию
        ordering = ['dateg']
		
# Новости 
class News(models.Model):
    daten = models.DateTimeField(_('daten'))
    title = models.CharField(_('news_title'), max_length=256)
    details = models.TextField(_('news_details'))
    photo = models.ImageField(_('news_photo'), upload_to='images/', blank=True, null=True)    
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'news'
        # indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['daten']),
        ]
        # Сортировка по умолчанию
        ordering = ['daten']
