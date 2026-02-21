from django.contrib import admin
from .models import Films, EntryNameFilm, Directors, MediaFilm, MediaDirectors, VideoFilm, EntryEstimationFilm
admin.site.register(Films)
admin.site.register(EntryNameFilm)
admin.site.register(MediaFilm)
admin.site.register(Directors)
admin.site.register(MediaDirectors)
admin.site.register(VideoFilm)
admin.site.register(EntryEstimationFilm)



