from django import forms
from .models import Films, EntryNameFilm, Directors, MediaFilm, MediaDirectors, EntryEstimationFilm, VideoFilm

class FilmsForm(forms.ModelForm):
    class Meta:
        model = Films
        fields = ['name', 'genre', 'country_production', 'year_of_release', 'film_serial']
        labels = {'name': '', 'genre': '', 'country_production': '',
                  'year_of_release': '', 'film_serial': ''
                }

class DirectorsForm(forms.ModelForm):
    class Meta:
        model = Directors
        fields = ['last_name', 'first_name', 'data_of_birth', 'data_of_death']
        labels = {'last_name': '', 'first_name': '', 'data_of_birth': '', 'data_of_death': ''}
        widgets = {'data_of_death': forms.DateInput(format='%d.%m.%Y', attrs={'placeholder':'дд.мм.гггг'}), 'data_of_birth': forms.DateInput(format='%d.%m.%Y', attrs={'placeholder':'дд.мм.гггг'})}

class EntryEstimationForm(forms.ModelForm):
    class Meta:
        model = EntryEstimationFilm
        fields = ['estimation']
        labels = {'estimation':''}

class EntryFilmForm(forms.ModelForm):
    class Meta:
        model = EntryNameFilm
        fields = ['about_film']
        labels = {'about_film': ''}
        widgets = {'about_film': forms.Textarea(attrs={'cols': 80})}
        
class ImageForm(forms.ModelForm):
    class Meta:
        model = MediaFilm
        fields = ['image']
        labels = {'image': ''}

class ImageDirectorForm(forms.ModelForm):
    class Meta:
        model = MediaDirectors
        fields = ['image']
        labels= {'image': ''}

class VideoFilmForm(forms.ModelForm):
    class Meta:
        model = VideoFilm
        fields = ['videos']
        labels = {'videos':''}
        
class SearchForm(forms.Form): 
    query = forms.CharField(max_length=100, label='', widget=forms.TextInput(attrs={'size': '40', 'placeholder': 'Введите поисковый запрос'}))
            
class AddDirectorForm(forms.Form):
    # Явно определяем поле формы для настройки queryset или виджета
    director = forms.ModelChoiceField(
        queryset=Directors.objects.all(), # Пример фильтрации
        required=False,
        empty_label=("выберите режиссера"),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

