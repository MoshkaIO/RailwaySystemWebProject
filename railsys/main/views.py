from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect


# Create your views here.
def index(request):
    data={
        'title':'Главная страница 2',
        'values': ['train1','train22','train33'],
        'obj': {
            'title': 'ОБЪЕКТИЩЕ',
            'values': ['train7', 'train8', 'train9']
        }
    }
    #return HttpResponse("<h4>Проверко работы views.py </h4>")
    #return render(request,'main/index.html',{'title':'Главная страница 1'});
    return render(request, 'main/index.html', data);
def about(request):
    return render(request,'main/about.html')
def registration(request):

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # получаем имя пользователя и пароль из формы
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            # выполняем аутентификацию
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'registration/sign_up.html', {'form': form})