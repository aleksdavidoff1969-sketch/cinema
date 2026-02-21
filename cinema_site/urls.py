"""Определяет схемы URL для cinema_site."""
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'cinema_site'
urlpatterns = [
 # Главная страница
 path('', views.index, name='index'),
 # Страница со списком всех фильмов.
 path('films/', views.films, name='films'),
 # Страница со списком всех сериалов
 path('serials/', views.serials, name='serials'),
 # Страница со списком всех режиссеров.
 path('directors/', views.directors, name='directors'),
 # Страница с подробной информацией по отдельному режиссеру.
 path('director/<int:director_id>/', views.director, name='director'),
 # Страница с подробной информацией по отдельному фильму.
 path('films/<int:film_id>/', views.film, name='film'),
 # Страница с подробной информацией по отдельному сериалу.
 path('serials/<int:serial_id>/', views.serial, name='serial'),
 # Страница для добавления нового фильма.
 path('new_film/', views.new_film, name='new_film'),
 # Страница для добавления нового сериала.
 path('new_serial/', views.new_serial, name='new_serial'),
 # Страница для добавления нового режиссера.
 path('new_director/', views.new_director, name='new_director'),
 # Страница для добавления новой оценки фильма.
 path('new_estimation_film/<int:film_id>/', views.new_estimation_film, name='new_estimation_film'),
 # Страница для добавления новой записи к фильму.
 path('new_entry_film/<int:film_id>/', views.new_entry_film, name='new_entry_film'),
 # Страница для добавления новой оценки сериала.
 path('new_estimation_serial/<int:serial_id>/', views.new_estimation_serial, name='new_estimation_serial'),
 # Страница для добавления новой записи к сериалу.
 path('new_entry_serial/<int:serial_id>/', views.new_entry_serial, name='new_entry_serial'),
 # Страница для редактирования полей сериала.
 path('edit_entry_serial/<int:serial_id>/', views.edit_entry_serial, name='edit_entry_serial'),
 # Страница для редактирования полей фильма.
 path('edit_entry_film/<int:film_id>/', views.edit_entry_film, name='edit_entry_film'),
 # Страница для редактирования полей режиссера.
 path('edit_entry_director/<int:director_id>/', views.edit_entry_director, name='edit_entry_director'),
# Страница для добавления нового изображения к фильму
 path('new_image_film/<int:film_id>/', views.new_image_film, name='new_image_film'), 
 # Страница для добавления нового изображения к сериалу
 path('new_image_serial/<int:serial_id>/', views.new_image_serial, name='new_image_serial'),
 # Страница для добавления нового видео к фильму
 path('new_video_film/<int:film_id>/', views.new_video_film, name='new_video_film'),
 # Страница для добавления нового видео к сериалу
 path('new_video_serial/<int:serial_id>/', views.new_video_serial, name='new_video_serial'),
 # Страница с фото режиссера
 path('delete_director/<int:director_id>/', views.delete_director, name='delete_director'),
 # Страница для удаления изображений к фильму 
 path('delete_film_id/<int:image_id>/<int:film_id>/', views.delete_film_id, name='delete_film_id'),
 # Страница для удаления видео к фильму 
 path('delete_film_video_id/<int:video_id>/<int:film_id>/', views.delete_film_video_id, name='delete_film_video_id'),
 # Страница для удаления видео к сериалу 
 path('delete_serial_video_id/<int:video_id>/<int:serial_id>/', views.delete_serial_video_id, name='delete_serial_video_id'),
 # Страница для удаления изображений к сериалу 
 path('delete_film_id/<int:image_id>/<int:serial_id>/', views.delete_serial_id, name='delete_serial_id'),
 # Страница для удаления фото режиссера 
 path('delete_director_id/<int:image_id>/<int:director_id>/', views.delete_director_id, name='delete_director_id'),
 # Страница для добавления нового изображения к станице с режиссером
 path('new_image_director/<int:director_id>/', views.new_image_director, name='new_image_director'),
 # Страница для поиска режиссера
 path('directors/search/', views.search_director, name='search_director'),
 # Страница для поиска фильмов режиссера
 path('director/search/', views.search_director_film, name='search_director_film'),
 # Страница для добавления режиссера на страницу с фильмом 
 path('add_film_director/<int:film_id>/', views.add_film_director, name='add_film_director'),
 # Страница для добавления режиссера на страницу с сериалом 
 path('add_serial_director/<int:serial_id>/', views.add_serial_director, name='add_serial_director'),
 # Страница для удаления страницы с режиссером 
 path('delete_director_page/<int:director_id>/', views.delete_director_page, name='delete_director_page'),
 # Страница для удаления страницы с фильмом 
 path('delete_film_page/<int:film_id>/', views.delete_film_page, name='delete_film_page'),
 # Страница для удаления страницы с сериалом 
 path('delete_serial_page/<int:serial_id>/', views.delete_serial_page, name='delete_serial_page'),
 ]