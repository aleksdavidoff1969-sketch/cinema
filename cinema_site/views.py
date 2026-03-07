from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from .models import Films, EntryNameFilm, Directors, MediaFilm, MediaDirectors, VideoFilm
from .forms import FilmsForm, DirectorsForm, EntryFilmForm, ImageForm, ImageDirectorForm, SearchForm, AddDirectorForm, EntryEstimationForm, VideoFilmForm
from django.contrib.auth.decorators import login_required
from django.http import Http404 

def index(request):
    """Главная страница приложения "cinema_site"."""
    return render(request, 'cinema_site/index.html')

@login_required
def films(request):
    """Выводит список фильмов."""
    form = SearchForm() 
    query = None 
    results = [] 
    if 'query' in request.GET: 
        form = SearchForm(request.GET) 
        if form.is_valid(): 
            query = form.cleaned_data['query'] 
            results = Films.objects.filter(name__iregex=query)
    films = Films.objects.only('name').filter(film_serial = 'film')
    paginator=Paginator(films, 10)
    page=request.GET.get('page')
    try:
        films_page=paginator.page(page)
    except PageNotAnInteger:
        films_page=paginator.page(1)
    except EmptyPage:
        films_page=paginator.page(paginator.num_pages)
    context = {'films': films_page,
               'form': form, 
                'query': query, 
                'results': results}
    return render(request, 'cinema_site/films.html', context)
       
@login_required
def serials(request):
    """Выводит список сериалов"""
    form = SearchForm() 
    query = None 
    results = [] 
    if 'query' in request.GET: 
        form = SearchForm(request.GET) 
        if form.is_valid(): 
            query= form.cleaned_data['query'] 
            results = Films.objects.filter(name__iregex=query)
    serials = Films.objects.only('name').filter(film_serial = 'serial')
    paginator=Paginator(serials, 1)
    page=request.GET.get('page')
    try:
        serials_page=paginator.page(page)
    except PageNotAnInteger:
        serials_page=paginator.page(1)
    except EmptyPage:
        serials_page=paginator.page(paginator.num_pages)
    context = {'serials': serials_page,
               'form': form, 
                'query': query, 
                'results': results}
    return render(request, 'cinema_site/serials.html', context)

@login_required
def directors(request):
    """Выводит список режиссеров"""
    form = SearchForm() 
    query = None 
    results = [] 
    if 'query' in request.GET: 
        form = SearchForm(request.GET) 
        if form.is_valid(): 
            query = form.cleaned_data['query'] 
            results = Directors.objects.filter(last_name__iregex=query)
    directors = Directors.objects.order_by('last_name')
    paginator=Paginator(directors, 10)
    page=request.GET.get('page')
    try:
        directors_page=paginator.page(page)
    except PageNotAnInteger:
        directors_page=paginator.page(1)
    except EmptyPage:
        directors_page=paginator.page(paginator.num_pages)
    context = {'query': query, 'results': results, 'form': form, 'directors' : directors_page}
    return render(request, 'cinema_site/directors.html', context)

def search_director(request):
    """Поиск режиссеров по фамилии."""
    form = SearchForm() 
    query = None 
    results = [] 
    if 'query' in request.GET: 
        form = SearchForm(request.GET) 
        if form.is_valid(): 
            query = form.cleaned_data['query'] 
            results = Directors.objects.filter(last_name__iregex=query)
    context = {'form':form, 'query':query, 'results':results}
    return render(request, 'cinema_site/search_director.html', context)

@login_required
def director(request, director_id):
    """Выводит информацию о режиссере и список фильмов"""
    director_obj = get_object_or_404(Directors, id=director_id)
    films = director_obj.films_set.all()
    image = director_obj.mediadirectors_set.all()
    return render(request, 'cinema_site/director.html', {
        'director': director_obj,
        'director_first_name': director_obj.first_name,
        'director_last_name': director_obj.last_name,
        'director_data_of_birth': director_obj.data_of_birth,
        'director_data_of_death': director_obj.data_of_death,
        'films': films,
        'image': image
        })
    
@login_required
def film(request, film_id):
    """Выводит информацию о фильме."""
    film_obj = get_object_or_404(Films, id=film_id)
    sujgets = film_obj.entrynamefilm_set.order_by('-date_added')
    estimations = film_obj.entryestimationfilm_set.order_by('-date_added')
    raitings = []
    if estimations:    
        for estimation in estimations:
            raitings.append(int(estimation.estimation))
        raiting = [int(x) for x in raitings]
        if len(raiting)==1:
            raiting = float(raiting[0])
        else:
            raiting = float(sum(raiting)/len(raiting))
    else:
        raiting = 'отсутствует'
    image = film_obj.mediafilm_set.all()
    videos = film_obj.videofilm_set.all()
    context = {
        'film': film_obj,
        'film_name': film_obj.name,
        'film_genre': film_obj.genre,
        'film_country_production': film_obj.country_production,
        'film_year_of_release': film_obj.year_of_release,
        'film_film_serial': film_obj.film_serial,
        'film_dir': film_obj.directors,
        'raiting': raiting,
        'sujgets': sujgets,
        'image': image,
        'videos': videos
        }
    return render(request, 'cinema_site/film.html', context)

@login_required
def serial(request, serial_id):
    """Выводит информацию о сериале."""
    serial_obj = get_object_or_404(Films, id=serial_id)
    sujgets = serial_obj.entrynamefilm_set.order_by('-date_added')
    estimations = serial_obj.entryestimationfilm_set.order_by('-date_added')
    raitings = []
    if estimations:    
        for estimation in estimations:
            raitings.append(int(estimation.estimation))
        raiting = [int(x) for x in raitings]
        if len(raiting)==1:
            raiting = float(raiting[0])
        else:
            raiting = float(sum(raiting)/len(raiting))
    else:
        raiting = 'отсутствует'
    image = serial_obj.mediafilm_set.all()
    videos = serial_obj.videofilm_set.all()
    context = {
        'serial': serial_obj,
        'serial_name': serial_obj.name,
        'serial_genre': serial_obj.genre,
        'serial_director': serial_obj.directors,
        'serial_country_production': serial_obj.country_production,
        'serial_year_of_release': serial_obj.year_of_release,
        'serial_film_serial': serial_obj.film_serial,
        'raiting': raiting,
        'sujgets': sujgets,
        'image': image,
        'videos': videos
        }
    return render(request, 'cinema_site/serial.html', context)

@login_required
def new_film(request):
    """Добавляет новый фильм."""
    if request.method != 'POST':
       # Данные не отправлялись; создается пустая форма.
        form = FilmsForm()
    else:
        # Отправлены данные POST; обработать данные.
        form = FilmsForm(data=request.POST)
        if form.is_valid():
            new_film=form.save(commit=False)
            new_film.owner=request.user
            new_film.save()
            return redirect('cinema_site:films')
    # Вывести пустую или недействительную форму.
    context = {'form': form}
    return render(request, 'cinema_site/new_film.html', context)

@login_required
def new_serial(request):
    """Добавляет новый сериал."""
    if request.method != 'POST':
       # Данные не отправлялись; создается пустая форма.
        form = FilmsForm()
    else:
        # Отправлены данные POST; обработать данные.
        form = FilmsForm(data=request.POST)
        if form.is_valid():
            new_serial=form.save(commit=False)
            new_serial.owner=request.user
            new_serial.save()
            return redirect('cinema_site:serials')
    # Вывести пустую или недействительную форму.
    context = {'form': form}
    return render(request, 'cinema_site/new_serial.html', context)

@login_required
def new_director(request):
    """Добавляет нового режиссера."""
    if request.method != 'POST':
       # Данные не отправлялись; создается пустая форма.
        form = DirectorsForm()
    else:
        # Отправлены данные POST; обработать данные.
        form = DirectorsForm(data=request.POST)
        if form.is_valid():
            new_director=form.save(commit=False)
            new_director.owner=request.user
            new_director.save()
            return redirect('cinema_site:directors')
    # Вывести пустую или недействительную форму.
    context = {'form': form}
    return render(request, 'cinema_site/new_director.html', context)

@login_required
def new_entry_film(request, film_id):
    """Добавляет комментарии к фильму."""
    film = Films.objects.get(id=film_id)
    new_entry =film.entrynamefilm_set.all()
    if request.method != 'POST':
        # Данные не отправлялись; создается пустая форма.
        form = EntryFilmForm()
    else:
        # Отправлены данные POST; обработать данные.
        form = EntryFilmForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.films = film
            new_entry.owner = request.user
            new_entry.save()
            return redirect('cinema_site:film', film_id=film_id)
    # Вывести пустую или недействительную форму.
    context = {'film': film, 'form': form}
    return render(request, 'cinema_site/new_entry_film.html', context)

@login_required
def new_estimation_film(request, film_id):
    """Добавляет оценки фильма."""
    film = Films.objects.get(id=film_id)
    user_estimation_exists = film.entryestimationfilm_set.filter(owner=request.user).exists()
    if user_estimation_exists:
        raise Http404
    if request.method != 'POST':
        # Данные не отправлялись; создается пустая форма.
        form = EntryEstimationForm()
    else:
        # Отправлены данные POST; обработать данные.
        form = EntryEstimationForm(data=request.POST)
        if form.is_valid():
            new_estimation = form.save(commit=False)
            new_estimation.films = film
            new_estimation.owner = request.user
            new_estimation.save()
            return redirect('cinema_site:film', film_id=film_id)
    # Вывести пустую или недействительную форму.
    context = {'film': film, 'form': form}
    return render(request, 'cinema_site/new_estimation_film.html', context)

@login_required
def new_entry_serial(request, serial_id):
    """Добавляет комментарии к сериалу."""
    serial = Films.objects.get(id=serial_id)
    new_entry = serial.entrynamefilm_set.all()
    if request.method != 'POST':
        # Данные не отправлялись; создается пустая форма.
        form = EntryFilmForm()
    else:
        # Отправлены данные POST; обработать данные.
        form = EntryFilmForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.films = serial
            new_entry.owner = request.user
            new_entry.save()
            return redirect('cinema_site:serial', serial_id=serial_id)
    # Вывести пустую или недействительную форму.
    context = {'serial': serial, 'form': form}
    return render(request, 'cinema_site/new_entry_serial.html', context)

@login_required
def new_estimation_serial(request, serial_id):
    """Добавляет оценки сериала."""
    serial = Films.objects.get(id=serial_id)
    user_estimation_exists =serial.entryestimationfilm_set.filter(owner=request.user).exists
    if user_estimation_exists:
        raise Http404 
    if request.method != 'POST':
        # Данные не отправлялись; создается пустая форма.
        form = EntryEstimationForm()
    else:
        # Отправлены данные POST; обработать данные.
        form = EntryEstimationForm(data=request.POST)
        if form.is_valid():
            new_estimation = form.save(commit=False)
            new_estimation.films = serial
            new_estimation.owner = request.user
            new_estimation.save()
            return redirect('cinema_site:serial', serial_id=serial_id)
    # Вывести пустую или недействительную форму.
    context = {'serial': serial, 'form': form}
    return render(request, 'cinema_site/new_estimation_serial.html', context)

@login_required
def edit_entry_film(request, film_id):
    """Редактирует существующую запись фильма."""
    film = Films.objects.get(id=film_id)
    if film.owner != request.user:
         raise Http404
    if request.method != 'POST':
        # Данные не отправлялись; создается пустая форма.
        form = FilmsForm(instance=film)
    else:
        # Отправлены данные POST; обработать данные.
        form = FilmsForm(instance=film, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('cinema_site:film', film_id=film_id)
    # Вывести пустую или недействительную форму.
    context = {'film': film, 'form': form}
    return render(request, 'cinema_site/edit_entry_film.html', context)

@login_required
def edit_entry_serial(request, serial_id):
    """Редактирует существующую запись сериала."""
    serial = Films.objects.get(id=serial_id)
    if serial.owner != request.user:
         raise Http404
    if request.method != 'POST':
        # Данные не отправлялись; создается пустая форма.
        form = FilmsForm(instance=serial)
    else:
        # Отправлены данные POST; обработать данные.
        form = FilmsForm(instance=serial, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('cinema_site:serial', serial_id=serial_id)
    # Вывести пустую или недействительную форму.
    context = {'serial': serial, 'form': form}
    return render(request, 'cinema_site/edit_entry_serial.html', context)

@login_required
def edit_entry_director(request, director_id):
    """Редактирует существующую запись режиссера."""
    director = Directors.objects.get(id=director_id)
    if director.owner != request.user:
         raise Http404
    if request.method != 'POST':
        # Данные не отправлялись; создается пустая форма.
        form = DirectorsForm(instance=director)
    else:
        # Отправлены данные POST; обработать данные.
        form = DirectorsForm(instance=director, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('cinema_site:director', director_id=director_id)
    # Вывести пустую или недействительную форму.
    context = {'director': director, 'form': form}
    return render(request, 'cinema_site/edit_entry_director.html', context)

@login_required
def new_image_film(request, film_id):
    """Добавляет новое изображение к фильму"""
    film = get_object_or_404 (Films, id=film_id)
    if film.owner != request.user:
        raise Http404
    else:
        image = film.mediafilm_set.all()
        if image.count() >=3:
            context = {'film':film}
            return render(request,'cinema_site/image_film_limit.html', context)    
        else:
            if request.method == 'POST':
                form = ImageForm(request.POST, request.FILES)
                if form.is_valid():
                    new_entry = form.save(commit=False)
                    new_entry.films=film
                    new_entry.save()
                    # Get the current instance object to display in the template
                    return redirect('cinema_site:film', film_id=film_id)
            else:
                form = ImageForm()
    context = {'film': film, 'form': form}
    return render(request, 'cinema_site/new_image_film.html', context)

@login_required
def new_image_serial(request, serial_id):
    """Добавляет изображение к сериалу"""
    serial = get_object_or_404 (Films, id=serial_id)
    if serial.owner != request.user:
        raise Http404
    else:
        image = serial.mediafilm_set.all()
        if image.count() >=3:
            context = {'serial':serial}
            return render(request,'cinema_site/image_serial_limit.html', context)    
        else:
            if request.method == 'POST':
                form = ImageForm(request.POST, request.FILES)
                if form.is_valid():
                    new_entry = form.save(commit=False)
                    new_entry.films=serial
                    new_entry.save()
                    # Get the current instance object to display in the template
                    return redirect('cinema_site:serial', serial_id=serial_id)
            else:
                form = ImageForm()
    context = {'serial': serial, 'form': form}
    return render(request, 'cinema_site/new_image_serial.html', context)

@login_required
def new_image_director(request, director_id):
    """Добавляет фото режиссера"""
    director = get_object_or_404 (Directors, id=director_id)
    if director.owner != request.user:
        raise Http404
    else:
        image = director.mediadirectors_set.all()
        if image.count() >=1:
            context = {'director':director}
            return render(request,'cinema_site/image_director_limit.html', context)    
        else:
            if request.method == 'POST':
                form = ImageDirectorForm(request.POST, request.FILES)
                if form.is_valid():
                    new_entry = form.save(commit=False)
                    new_entry.directors=director
                    new_entry.save()
                    # Get the current instance object to display in the template
                    return redirect('cinema_site:director', director_id=director_id)
            else:
                form = ImageDirectorForm()
    context = {'director': director, 'form': form}
    return render(request, 'cinema_site/new_image_director.html', context)

@login_required
def new_video_film(request, film_id):
    """Добавляет новое видео к фильму"""
    film = get_object_or_404 (Films, id=film_id)
    if film.owner != request.user:
        raise Http404
    else:
        video = film.videofilm_set.all()
        if video.count() >=2:
            context = {'film':film}
            return render(request,'cinema_site/video_film_limit.html', context)    
        else:
            if request.method == 'POST':
                form = VideoFilmForm(request.POST, request.FILES)
                if form.is_valid():
                    new_entry = form.save(commit=False)
                    new_entry.films=film
                    new_entry.save()
                    # Get the current instance object to display in the template
                    return redirect('cinema_site:film', film_id=film_id)
            else:
                form = VideoFilmForm()
    context = {'film': film, 'form': form}
    return render(request, 'cinema_site/new_video_film.html', context)

@login_required
def new_video_serial(request, serial_id):
    """Добавляет новое видео к фильму"""
    serial = get_object_or_404 (Films, id=serial_id)
    if serial.owner != request.user:
        raise Http404
    else:
        video = serial.videofilm_set.all()
        if video.count() >=2:
            context = {'serial': serial}
            return render(request,'cinema_site/video_serial_limit.html', context)    
        else:
            if request.method == 'POST':
                form = VideoFilmForm(request.POST, request.FILES)
                if form.is_valid():
                    new_entry = form.save(commit=False)
                    new_entry.films=serial
                    new_entry.save()
                    # Get the current instance object to display in the template
                    return redirect('cinema_site:serial', serial_id=serial_id)
            else:
                form = VideoFilmForm()
    context = {'serial': serial, 'form': form}
    return render(request, 'cinema_site/new_video_serial.html', context)

@login_required
def delete_director(request, director_id):
    """Выводит фото режиссера."""
    director = Directors.objects.get(id=director_id)
    if director.owner != request.user:
        raise Http404
    else:
        images = director.mediadirectors_set.all()
        if not images:
            return redirect('cinema_site:director', director_id=director_id)     
    context = {'director':director, 'images': images}
    return render(request, 'cinema_site/delete_director.html', context)
    
   
@login_required   
def delete_film_id(request, image_id, film_id):
    """Удаляет изображение к фильму."""
    film = get_object_or_404(Films, id = film_id)
    image = get_object_or_404(MediaFilm, id=image_id, films__id=film_id)
    if request.method == 'POST':
        image.delete()
        return redirect('cinema_site:film', film_id=film_id)
    context = {'film': film, 'image': image}
    return render(request, 'cinema_site/delete_film_id.html', context)

@login_required   
def delete_film_video_id(request, video_id, film_id):
    """Удаляет видео к фильму."""
    film = get_object_or_404(Films, id = film_id)
    video = get_object_or_404(VideoFilm, id=video_id, films__id=film_id)
    if request.method == 'POST':
        video.delete()
        return redirect('cinema_site:film', film_id=film_id)
    context = {'film': film, 'video': video}
    return render(request, 'cinema_site/delete_film_video_id.html', context)

@login_required   
def delete_serial_id(request, image_id, serial_id):
    """Удаляет изображение к сериалу."""
    serial = get_object_or_404(Films, id = serial_id)
    image = get_object_or_404(MediaFilm, id=image_id, films__id=serial_id)
    if request.method == 'POST':
        image.delete()
        return redirect('cinema_site:serial', serial_id=serial_id)
    context = {'serial': serial, 'image': image}
    return render(request, 'cinema_site/delete_serial_id.html', context)

@login_required   
def delete_serial_video_id(request, video_id, serial_id):
    """Удаляет видео к фильму."""
    serial = get_object_or_404(Films, id = serial_id)
    video = get_object_or_404(VideoFilm, id=video_id, films__id=serial_id)
    if request.method == 'POST':
        video.delete()
        return redirect('cinema_site:serial', serial_id=serial_id)
    context = {'serial': serial, 'video': video}
    return render(request, 'cinema_site/delete_serial_video_id.html', context)


login_required   
def delete_director_id(request, image_id, director_id):
    """Удаляет изображение."""
    image = get_object_or_404(MediaDirectors, id=image_id, directors__id=director_id)
    if request.method == 'POST':
        image.delete()
        return redirect('cinema_site:delete_director', director_id=director_id)
    context = {'image': image}
    return render(request, 'cinema_site/delete_director_id.html', context)

def search_director_film(request):
    """Выводит информацию о фильме."""
    form = SearchForm() 
    query = None 
    results = [] 
    if 'query' in request.GET: 
        form = SearchForm(request.GET) 
        if form.is_valid(): 
            query = form.cleaned_data['query'] 
            results = Films.objects.filter(name__iregex=query)
    context = {'form':form, 'query':query, 'results':results}
    return render(request, 'cinema_site/search_director_film.html', context)

def add_film_director(request, film_id):
    """Добавляет режиссера на страницу с фильмом."""
    film=get_object_or_404(Films, id=film_id)
    form = SearchForm() 
    query = None 
    directors = [] 
    if 'query' in request.GET: 
        form = SearchForm(request.GET) 
        if form.is_valid(): 
            query = form.cleaned_data['query'] 
            directors = Directors.objects.filter(last_name__iregex=query)
    if request.method == 'POST':
        director_id=request.POST.get('director_id')
        director= get_object_or_404(Directors, id=director_id)
        film.directors=director
        film.save()
        return redirect('cinema_site:film', film_id=film_id)
    # Вывести пустую или недействительную форму.
    context = {'film':film, 'directors':directors, 'query': query, 'form': form}
    return render(request, 'cinema_site/add_film_director.html', context)

def add_serial_director(request, serial_id):
    """Добавляет режиссера на страницу с сериалом."""
    serial=get_object_or_404(Films, id=serial_id)
    form = SearchForm() 
    query = None 
    directors = [] 
    if 'query' in request.GET: 
        form = SearchForm(request.GET) 
        if form.is_valid(): 
            query = form.cleaned_data['query'] 
            directors = Directors.objects.filter(last_name__iregex=query)
    if request.method == 'POST':
        director_id=request.POST.get('director_id')
        director= get_object_or_404(Directors, id=director_id)
        serial.directors=director
        serial.save()
        return redirect('cinema_site:serial', serial_id=serial_id)
    # Вывести пустую или недействительную форму.
    context = {'serial':serial, 'directors':directors, 'query': query, 'form': form}
    return render(request, 'cinema_site/add_serial_director.html', context)
    

@login_required   
def delete_film_page(request, film_id):
    """Удаляет страницу с фильмом."""
    film = get_object_or_404(Films, id=film_id)
    if film.owner != request.user:
        raise Http404
    else:
        if request.method == 'POST':
            film.delete()
            return redirect('cinema_site:films')
    context = {'film': film}
    return render(request, 'cinema_site/delete_film_page.html', context)

@login_required   
def delete_serial_page(request, serial_id):
    """Удаляет страницу с сериалом."""
    serial = get_object_or_404(Films, id=serial_id)
    if serial.owner != request.user:
        raise Http404
    else:
        if request.method == 'POST':
            serial.delete()
            return redirect('cinema_site:serials')
    context = {'serial': serial}
    return render(request, 'cinema_site/delete_serial_page.html', context)

@login_required   
def delete_director_page(request, director_id):
    """Удаляет страницу с режиссером."""
    director = get_object_or_404(Directors, id=director_id)
    if director.owner != request.user:
        raise Http404
    else:
        if request.method == 'POST':
            director.delete()
            return redirect('cinema_site:directors')
    context = {'director': director}
    return render(request, 'cinema_site/delete_director_page.html', context)