from django.db import models
from django.urls import reverse
from django.contrib import admin
from django.dispatch import receiver
from django.db.models.signals import post_delete
from django.contrib.auth.models import User

class Directors(models.Model):
    """Заполнение полей для режиссеров"""
    first_name = models.CharField(max_length=200, help_text='Имя режиссера', null=True, blank=True)
    last_name = models.CharField(max_length=200, help_text='Фамилия режиссера', null=True, blank=True)
    data_of_birth = models.DateField(null=True, blank=True, help_text='Дата рождения')
    data_of_death = models.DateField(null=True, blank=True, help_text='Дата смерти')
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return '{} {}'.format(self.last_name, self.first_name)

class Films(models.Model):
    """Заполнение полей для фильмов."""
    name = models.CharField(max_length=200, help_text='Название')
    genre = models.CharField(choices=(('детектив', 'детектив'), ('фантастика', 'фанатастика'), ('мелодрама', 'мелодрама'), ('приключения', 'приключения'), ('боевик', 'боевик'), ('комедия', 'комедия')), null=True, blank=True, max_length=200, help_text='Жанр')
    country_production = models.CharField(null=True, blank=True, max_length=200, help_text='Страна производства')
    year_of_release = models.CharField(null=True, blank=True, max_length=200, help_text='Год создания')
    film_serial = models.CharField(choices=(('film', 'film'), ('serial', 'serial')), default='')
    text_file = models.FileField(null=True, blank=True, upload_to = 'images/')
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    directors = models.ForeignKey(Directors, on_delete=models.SET_NULL, null=True, help_text='Режиссер')
    
    def __str__(self):
        """Возвращает строковое представление модели."""
        return f"{self.name[:30]}..."
        
class EntryEstimationFilm(models.Model):
    """Оценки"""
    films = models.ForeignKey(Films, on_delete=models.CASCADE, null=True)
    estimation = models.CharField(choices=(('1', 1), ('2', 2), ('3', 3), ('4', 4), ('5', 5)), null=True, blank=True, help_text='Оценка по пятибальной шкале')
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

class EntryNameFilm(models.Model):
    """Комментарии"""
    films = models.ForeignKey(Films, on_delete=models.CASCADE, null=True)
    about_film = models.TextField(help_text = 'Добавьте комментарий к фильму')
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        """Возвращает строковое названия фильма."""
        return f"{self.about_film[:50]}..."
    
class MediaFilm(models.Model):
    """Добавляет изображения к фильмам и сериалам"""
    films = models.ForeignKey(Films, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200, help_text='Название', null=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to = 'images/')
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

class VideoFilm(models.Model):
    """Добавляет видео к фильмам и сериалам"""
    films = models.ForeignKey(Films, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200, help_text='Название', null=True, blank=True)
    videos = models.FileField(null=True, blank=True, help_text='Выберите файл для загрузки', upload_to = 'images/')
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

class MediaDirectors(models.Model):
    """Добавляет изображения на страницу с режиссером"""
    directors = models.ForeignKey(Directors, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200, help_text='Название', null=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to = 'images/')
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    

@receiver(post_delete, sender=MediaFilm)
def media_post_delete_handler(sender, **kwargs):
    media = kwargs['instance']
    storage, path = media.image.storage, media.image.path
    storage.delete(path)

@receiver(post_delete, sender=MediaDirectors)
def media_post_delete_handler(sender, **kwargs):
    media = kwargs['instance']
    storage, path = media.image.storage, media.image.path
    storage.delete(path)

@receiver(post_delete, sender=VideoFilm)
def media_post_delete_handler(sender, **kwargs):
    media = kwargs['instance']
    storage, path = media.videos.storage, media.videos.path
    storage.delete(path)
    


