from .models import  Passanger, Train, Route, City, RoutePoint
from django.forms import ModelForm, TextInput, DateTimeInput, Textarea, DateInput, forms
from django import forms



class DateInput(forms.DateInput):
    input_type = 'date'

class DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime-local'
# class RoutesForm(ModelForm):
#     class Meta:
#         model=Routes
#         fields=['from_to','description','big_text','date','end_date']
#
#         widgets ={
#             "from_to": TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Откуда и куда'
#             }),
#             "description": TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'краткое описание'
#             }),
#             "big_text": Textarea(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'большой текст'
#             }),
#             "date": DateTimeInput(attrs={
#                 'class':'form-control',
#                         'placeholder': 'отправление'
#             }),
#             "end_date": DateTimeInput(attrs={
#                 'class': 'form-control',
#                          'placeholder': 'прибытие'
#             })
#         }
class PassangersForm(ModelForm):
    class Meta:
        model=Passanger
        fields = ['first_name', 'second_name', 'birthday']

        widgets ={
            "first_name": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Имя'
            }),
            "second_name": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Фамилия'
            }),
            "birthday": DateInput(attrs={
                'class': 'form-control',
                'placeholder': 'Дата Рождения'
            }),

        }
class TrainForm(ModelForm):
    class Meta:
        model=Train
        fields = ['train_type','train_number']
        widgets = {
            "train_type": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Тип поезда'
            }),
            "train_number": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Номер поезда'
            }),
        }
class RouteSearchForm(forms.Form):
    #departure_city=forms.CharField()
    departure_city=forms.ModelChoiceField(queryset=City.objects.all(),label='Откуда')
    arrival_city = forms.ModelChoiceField(queryset=City.objects.all(),label='Куда')
    departure_day=forms.DateField(widget=DateInput)

class PassengerAddForm(forms.Form):
    DOC_CHOICES = [
        ('Паспорт', 'Паспорт'),
        ('Свид-во о рождении', 'Свидетельство о рождении (для лиц младше 14 лет)'),
        ('Загранпаспорт', 'Заграничный паспорт гражданина РФ'),
        ('Военный билет', 'Военный билет (для военнослужащих, состоящих на срочной службе в текущий момент)'),
        ('Паспорт моряка','Паспорт моряка')
    ]
    first_name = forms.CharField(label="прмогите", help_text='Имя')
    second_name = forms.CharField(help_text='Фамилия')
    birthday = forms.DateTimeField(help_text='Дата рождения', widget=DateInput)
    document_type=forms.CharField(label='Выберите тип документа',
                                     widget=forms.RadioSelect(choices=DOC_CHOICES), )
    document_number = forms.CharField(label='Серия и/или номер')




class PassengerAddFormModel(ModelForm):
    class Meta:
        model=Passanger
        fields = ['first_name','second_name','birthday','doc_type','doc_info']
        widgets = {
             "first_name": TextInput(attrs={
                 'class': 'form-control',
                 'placeholder': 'Имя'
             }),
             "second_name": TextInput(attrs={
                 'class': 'form-control',
                 'placeholder': 'Фамилия'
             }),
            "birthday": DateInput(attrs={
                'class': 'form-control',
                'placeholder': 'Дата Рождения'
            }),
            "doc_type": TextInput(attrs={
                 'class': 'form-control',
                 'placeholder': 'Тип документа'
             }),
            "doc_info": TextInput(attrs={
                 'class': 'form-control',
                 'placeholder': 'Серия и/или номер документа'
             }),
        }


class PassengerChoiceForm(forms.Form):
    #passenger = forms.ModelChoiceField()
    passenger = forms.ModelChoiceField(queryset=Passanger.objects.all())
    #def set_pas(self,q):
        #self.passenger=q
def antigay_PassengerChoiceForm_generator(user_id): #удивительно, но работает
    pas=Passanger.objects.filter(user_id=user_id)
    class PassengerChoiceForm(forms.Form):
        # passenger = forms.ModelChoiceField()
        passenger = forms.ModelChoiceField(queryset=pas)
    return PassengerChoiceForm



class RouteSearchChoiseForm(forms.Form):
    FRUIT_CHOICES = [
        ('ВЫБРАТЬ РЕЙС', 'ВЫБРАТЬ РЕЙС'),
    ]
    radio_choise = forms.CharField(label='Выберите рейс и нажмите кнопку',
                                     widget=forms.RadioSelect(choices=FRUIT_CHOICES))

#class PlaceSearchChoiseForm(forms.Form):
     #place = forms.ModelChoiceField(queryset)
class RouteFormM(ModelForm):
    class Meta():
        model=Route
        fields = ['id_train','base_price']
class RoutePointFormM(ModelForm):
    class Meta():
        model=RoutePoint
        fields = ['id_station','id_route','arrive_time','departure_time','boarding']
        widgets = {
            'arrive_time': DateTimeInput,
            'departure_time':DateTimeInput
        }
class TrainFormM(ModelForm):
    class Meta():
        model=Train
        fields = ['train_type','train_number']


"""class SearchRouteForm(ModelForm):
    class Meta:
        model=Route
        fields = ['departure_city','arrival_city','departure_time']
        widgets = {
            "departure_city": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Тип поезда'
            }),
            "arrival_city": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Номер поезда'
            }),
            "departure_time": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Дата и время отправления'
            }),
        }
        """
