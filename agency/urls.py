"""
URL configuration for agency project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include

from django.conf import settings 
from django.conf.urls.static import static 
from django.conf.urls import include

from concert import views
from django.contrib.auth import views as auth_views

urlpatterns = [

    path('', views.index),
    path('index/', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    #path('report/index/', views.report_index, name='report_index'),
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),

    path('city/index/', views.city_index, name='city_index'),
    path('city/create/', views.city_create, name='city_create'),
    path('city/edit/<int:id>/', views.city_edit, name='city_edit'),
    path('city/delete/<int:id>/', views.city_delete, name='city_delete'),
    path('city/read/<int:id>/', views.city_read, name='city_read'),
        
    path('hall/index/', views.hall_index, name='hall_index'),
    #path('hall/list/', views.hall_list, name='hall_list'),
    path('hall/create/', views.hall_create, name='hall_create'),
    path('hall/edit/<int:id>/', views.hall_edit, name='hall_edit'),
    path('hall/delete/<int:id>/', views.hall_delete, name='hall_delete'),
    path('hall/read/<int:id>/', views.hall_read, name='hall_read'),

    path('entertainer/index/', views.entertainer_index, name='entertainer_index'),
    path('entertainer/list/', views.entertainer_list, name='entertainer_list'),
    path('entertainer/create/', views.entertainer_create, name='entertainer_create'),
    path('entertainer/edit/<int:id>/', views.entertainer_edit, name='entertainer_edit'),
    path('entertainer/delete/<int:id>/', views.entertainer_delete, name='entertainer_delete'),
    path('entertainer/read/<int:id>/', views.entertainer_read, name='entertainer_read'),
        
    path('concert/index/', views.concert_index, name='concert_index'),
    path('concert/list/', views.concert_list, name='concert_list'),
    path('concert/create/', views.concert_create, name='concert_create'),
    path('concert/edit/<int:id>/', views.concert_edit, name='concert_edit'),
    path('concert/delete/<int:id>/', views.concert_delete, name='concert_delete'),
    path('concert/read/<int:id>/', views.concert_read, name='concert_read'),
            
    path('ticket/index/', views.ticket_index, name='ticket_index'),
    path('ticket/list/', views.ticket_list, name='ticket_list'),
    path('ticket/create/<int:concert_id>/', views.ticket_create, name='ticket_create'),
    path('ticket/edit/<int:id>/', views.ticket_edit, name='ticket_edit'),
    path('ticket/delete/<int:id>/', views.ticket_delete, name='ticket_delete'),
    path('ticket/read/<int:id>/', views.ticket_read, name='ticket_read'),

    path('application/index/', views.application_index, name='application_index'),
    path('application/list/', views.application_list, name='application_list'),
    path('application/create/', views.application_create, name='application_create'),
    path('application/edit/<int:id>/', views.application_edit, name='application_edit'),
    path('application/delete/<int:id>/', views.application_delete, name='application_delete'),
    path('application/read/<int:id>/', views.application_read, name='application_read'),

    path('movement/index/<int:application_id>/', views.movement_index, name='movement_index'),
    path('movement/create/<int:application_id>/', views.movement_create, name='movement_create'),
    path('movement/edit/<int:id>/<int:application_id>/', views.movement_edit, name='movement_edit'),
    path('movement/delete/<int:id>/<int:application_id>/', views.movement_delete, name='movement_delete'),
    path('movement/read/<int:id>/<int:application_id>/', views.movement_read, name='movement_read'),

    path('gallery/index/', views.gallery_index, name='gallery_index'),
    path('gallery/list/', views.gallery_list, name='gallery_list'),
    path('gallery/create/', views.gallery_create, name='gallery_create'),
    path('gallery/edit/<int:id>/', views.gallery_edit, name='gallery_edit'),
    path('gallery/delete/<int:id>/', views.gallery_delete, name='gallery_delete'),
    path('gallery/read/<int:id>/', views.gallery_read, name='gallery_read'),

    path('news/index/', views.news_index, name='news_index'),
    path('news/list/', views.news_list, name='news_list'),
    path('news/create/', views.news_create, name='news_create'),
    path('news/edit/<int:id>/', views.news_edit, name='news_edit'),
    path('news/delete/<int:id>/', views.news_delete, name='news_delete'),
    path('news/read/<int:id>/', views.news_read, name='news_read'),

    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('settings/account/', views.UserUpdateView.as_view(), name='my_account'),
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('password-change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

