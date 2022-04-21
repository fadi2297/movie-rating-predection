from django import forms
from extract_data import *
from django.core import validators

def check_genres(value):
    if len(value) > 3:
        raise forms.ValidationError("You've selected more than 3 genres.")


def check_production(value):
    flag = False
    productions = [pro.lower() for pro in extract_productions()]
    for pro in productions:
        if value.lower() in correct_production_company(pro).lower():
            flag = True
            break
    if flag == False:
        raise forms.ValidationError("Your production company does not exists in our database.")

def check_actors(value):
    actors = [act.lower() for act in extract_actors()]
    if value.lower() not in actors:
        raise forms.ValidationError("Your actor/actress does not exists in our database.")

def check_director(value):
    directors =  [dir.lower() for dir in extract_directors()]
    if value.lower() not in directors:
        raise forms.ValidationError("Your director does not exists in our database.")


class MovieForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={
                            'class': 'form-control',
                            'placeholder': 'Example: 1/1997'},
                            format='%m/%Y'),
                            input_formats=('%m/%Y',),
                            label= 'The Date of Publishing The Movie:')

    GENRE_CHOICES = [(str(idx), coun.capitalize()) for idx, coun in enumerate(genres_list)]
    genre = forms.MultipleChoiceField(label= 'Select At Most 3 Genres Of The Movie:',
                                    choices = GENRE_CHOICES,
                                    widget = forms.CheckboxSelectMultiple,
                                    validators = [check_genres])

    duration = forms.IntegerField(label= 'The Duration Of The Movie (in minutes):',
                                widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Example: 194'}))

    countries = ['-----']
    countries += extract_countires()

    COUNTRIES_CHOICES = [(str(idx), coun.capitalize()) for idx, coun in enumerate(countries)]
    country1 = forms.TypedChoiceField(label= 'The Main Production Country:',
                                    choices = COUNTRIES_CHOICES, coerce = str,
                                    widget = forms.Select(attrs={'class': 'form-control'}))

    country2 = forms.TypedChoiceField(label= 'The Second Main Production Country:',
                                    choices = COUNTRIES_CHOICES, coerce = str,
                                    required = False, help_text= 'Not required!',
                                    widget = forms.Select(attrs={'class': 'form-control'}))

    languages = ['-----']
    languages += extract_languages()

    LANGUAGES_CHOICES = [(str(idx), coun.capitalize()) for idx, coun in enumerate(languages)]
    language1 = forms.TypedChoiceField(label= 'The Main Language:',
                                    choices = LANGUAGES_CHOICES, coerce = str,
                                    widget = forms.Select(attrs={'class': 'form-control'}))

    language2 = forms.TypedChoiceField(label= 'The Second Main Language:',
                                    choices = LANGUAGES_CHOICES, coerce = str,
                                    required = False, help_text= 'Not required!',
                                    widget = forms.Select(attrs={'class': 'form-control'}))

    production = forms.CharField(label= 'The Production Company:',
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Example: Twentieth Century Fox'}),
                                validators = [check_production])

    budget = forms.IntegerField(label= 'The Budget Of The Film (in $):',
                                    widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Example: 200,000,000'}))

    actor1 = forms.CharField(label= 'The Main Actor/Actress:',
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Example: Leonardo Dicaprio'}),
                                validators = [check_actors])

    actor2 = forms.CharField(label= 'The Second Main Actor/Actress:',
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Example: Kate Winslet'}),
                                validators = [check_actors])

    director = forms.CharField(label= 'The Director:',
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Example: James Cameron'}),
                                validators = [check_director])
