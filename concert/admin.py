from django.contrib import admin

from .models import Entertainer, City, Hall, Concert, Ticket, Application, Movement, Gallery, News

# Добавление модели на главную страницу интерфейса администратора
admin.site.register(Entertainer)
admin.site.register(City)
admin.site.register(Hall)
admin.site.register(Concert)
admin.site.register(Ticket)
admin.site.register(Application)
admin.site.register(Movement)
admin.site.register(Gallery)
admin.site.register(News)
