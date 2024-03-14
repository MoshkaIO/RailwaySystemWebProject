from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Sum
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from .models import  Passanger, Train, Route, PreTicket, Seat, Ticket, RoutePoint, Carriage, Carriage_type, \
    Station, City
from .forms import RouteSearchForm, RouteSearchChoiseForm, PassengerChoiceForm, PassengerAddForm, \
    PassengerAddFormModel, antigay_PassengerChoiceForm_generator, RouteFormM, RoutePointFormM, TrainFormM
import datetime
# from django.shortcuts import redirect
from django.views.generic import DetailView, UpdateView, DeleteView, ListView, CreateView
from .statistik import checkTicketsIntersection, object_home

def timetable_home(request):
    if request.session.get('first_el') == None:
        first_el = 0
        last_el = 10
        if Route.objects.all().count() < 10:
            last_el = Route.objects.all().count()  # вроде тут не надо отнимать 1
    else:
        first_el = request.session.get('first_el')
        last_el = request.session.get('last_el')
    routes = Route.objects.all()[first_el:last_el]
    total = Route.objects.all().count()
    print("Ваша выборка: ")
    print(routes)
    request.session['first_el'] = first_el
    request.session['last_el'] = last_el
    if request.method == 'POST':
        print("начинаю перебирать")
        for butt in routes:  # смотрим, выбрал ли пользователь один из routes
            stroka = "b_detail_" + str(butt.id)
            print(stroka)
            if stroka in request.POST:
                print(" Кнопка " + stroka + " была нажата!")
                request.session['user_chosen_route_id'] = butt.id
                return redirect('route-detail')
        if "b_add10" in request.POST:
            print("Нажата кнопка b_add10")
            first_el = first_el + 10
            last_el = last_el + 10
            request.session['first_el'] = first_el
            request.session['last_el'] = last_el
            return redirect('route-home')
        if "b_sub10" in request.POST:
            print("Нажата кнопка b_sub10")
            first_el = first_el - 10
            last_el = last_el - 10
            if first_el < 0:
                first_el = 0
                last_el = 10
            request.session['first_el'] = first_el
            request.session['last_el'] = last_el
            return redirect('route-home')
    routes = Route.objects.all()[first_el:last_el]
    data = {
        'elements': routes,
        'first_el': first_el,
        'last_el': last_el,
        'total': total
    }
    return render(request, 'timetable/timetable.html', data)

class RouteDetailView(DetailView):
    model = Route
    template_name = 'route/details_view.html'  # шаблонч
    context_object_name = 'route'

class RouteSearchDetailView(DetailView):
    model = PreTicket
    template_name = 'route/pre_details_view.html'  # шаблонч
    context_object_name = 'route'

def route_search_detail(request):
    results = 1
    return render(request, 'route/details_view.html', {'results': results})

def passenger_home(request):
    passengers = Passanger.objects.order_by('first_name')
    passengers = Passanger.objects.annotate()
    return render(request, 'passenger/passenger_home.html', {'passengers': passengers})

class PassangerDetailView(DetailView):
    model = Passanger
    template_name = 'passenger/details_view.html'  # шаблонч
    context_object_name = 'passenger'


def train_home(request):
    trains = Train.objects.order_by('train_number')
    return render(request, 'train/train_home.html', {'trains': trains})


class SearchRoute(ListView):
    template_name = 'route/details_view.html'
    context_object_name = 'route'

@login_required
def route_city_search(request):
    form = RouteSearchForm(initial={'departure_day': datetime.date.today()})
    fakeform = RouteSearchChoiseForm()
    error = ''
    query = None
    full_results = []  # results+ доп. инфа
    dep_ct = ""
    arr_ct = ""
    if request.method == 'POST':
        form = RouteSearchForm(request.POST)
        fakeform = RouteSearchChoiseForm(request.POST)
        if form.is_valid():
            dep_ct = form.cleaned_data['departure_city']
            arr_ct = form.cleaned_data['arrival_city']
            dep_day = form.cleaned_data['departure_day']
            results = Route.test1_get_routes_from_to_city(dep_ct, arr_ct,
                                                          dep_day)
            add_info_list = []
            for butt in results:  # смотрим, какой рейс был выбран
                stroka = "b" + str(butt.id - results.count())
                print(stroka)
                delta = butt.arr_time - butt.dep_time
                train_type = butt.id_route.id_train.train_type
                add_info = {'delta': delta,
                            'train_type': train_type}  # дополнительная инфа на каждую строчку результата (может заменить preticket в будущем)
                add_info_list.append(add_info)
                if stroka in request.POST:
                    print("Кнопка " + str(butt.id - results.count()) + " была нажата!")
                    mes = "ПРИЁМ-ПРИЁМ!!!!!!"
                    but_data = {'message': mes}
                    request.session['data'] = but_data
                    request.session['preticket_id'] = butt.id - results.count()
                    return redirect('place-search')
            full_results = zip(results, add_info_list)
            for key, value in request.POST.items():  # проверялка содержимого request-a
                print('Key: %s' % (key))
                print('Value %s' % (value))
        else:
            # form = RouteSearchForm(request.POST)
            error = "Форма заполнена плохо!"
    data = {
        'form': form,
        'fakeform': fakeform,
        'error': error,
        'query': query,
        'results': full_results,
        'dep_ct': dep_ct,
        'arr_ct': arr_ct

    }
    return render(request, "search/route_search_rezult.html", data)


@login_required
def place_search(request):
    print("ФУНКЦИЯ ПЛЭЭЭЙС СЁРЧ ЗАПУЩЕНА")
    for key, value in request.POST.items():  # проверялка содержимого request-a
        print('Key: %s' % (key))
        # print(f'Key: {key}') in Python >= 3.7
        print('Value %s' % (value))
    but_data = request.session.get('data')

    preticket_id = request.session.get('preticket_id')
    pr1 = PreTicket.objects.get(id=preticket_id)  # восстанавливаем preticket по переданному в сессии id
    route = Route.objects.get(id=pr1.id_route.id)
    tr = Train.objects.get(id=route.id_train.id)
    cars = tr.get_all_carriages()  # все вагоны поезда
    delta = pr1.arr_time - pr1.dep_time
    train_type = pr1.id_route.id_train.train_type

    chosen_car_number = request.session.get('car_number')
    print("Номер рассматриваемого вагона: " + str(chosen_car_number))
    if chosen_car_number == None:
        chosen_car_number = 1
        print("Сработал предохранитель от None")
    if chosen_car_number >= cars.count():  # защита от барахла в session
        chosen_car_number = 1

    chosen_car = cars.get(carriage_number=chosen_car_number)
    seats_of_car = Seat.objects.filter(id_carriage=chosen_car.id).order_by("place_number")  # места в выбранном вагоне
    len = seats_of_car.count()
    distance = pr1.hops_count
    price_list = []
    price_place_list = []  # лист кортежей место-цена
    for i in range(len):  # жеска заполняем price_place_list
        place = seats_of_car.get(place_number=i + 1)
        is_occupied = checkTicketsIntersection(place, pr1)
        price_place = {'price': distance * route.base_price * seats_of_car[i].price_coef,
                       'place': i, 'is_occupied': is_occupied}
        price_place_list.append(price_place)
        price_list.append(distance * route.base_price * seats_of_car[i].price_coef)

    if request.method == 'POST':
        form = RouteSearchForm(request.POST)  # НЕ ЗАДЕЙСТВОВАНО
        for butt in cars:  # смотрим, выбрал ли пользователь один из вагонов
            stroka = "b" + str(butt.carriage_number)
            print(stroka)
            if stroka in request.POST:  # если кнопка с именем stroka была нажата то мы это тут увидим
                print("Кнопка " + stroka + " была нажата!")
                chosen_car_number = butt.carriage_number
                seats_of_car = Seat.objects.filter(id_carriage=butt.id)
                request.session['car_number'] = chosen_car_number
                chosen_car = cars.get(carriage_number=chosen_car_number)
                seats_of_car = Seat.objects.filter(id_carriage=chosen_car.id).order_by(
                    "place_number")  # места в выбранном вагоне
                len = seats_of_car.count()
                price_place_list = []  # лист кортежей место-цена
                for i in range(len):  # жеска заполняем price_place_list
                    place = seats_of_car.get(place_number=i + 1)
                    is_occupied = checkTicketsIntersection(place, pr1)
                    price_place = {'price': distance * route.base_price * seats_of_car[i].price_coef,
                                   'place': i + 1, 'is_occupied': is_occupied}
                    price_place_list.append(price_place)
                    price_list.append(distance * route.base_price * seats_of_car[i].price_coef)

        print("Мы проверили все нажатия на вагоны...")

        for butt in seats_of_car:  # смотрим, выбрал ли пользователь одно из мест
            stroka = "sb" + str(butt.place_number)  # ебливый костыль ебливому питону и ебливому джанго
            if stroka in request.POST:  # если кнопка с именем stroka была нажата то мы это тут увидим
                print("Кнопка " + stroka + " была нажата!")
                mes = "Сообщение сессиии: вы редиректнулись из place search!!!!!!"
                but_data = {'message': mes}
                request.session['data'] = but_data
                request.session['car_number'] = chosen_car_number
                request.session['place_number'] = butt.place_number
                request.session['place_id'] = butt.id
                request.session['train_id'] = tr.id
                request.session['price'] = price_list[butt.place_number]
                return redirect('ticket-form')
        print("Мы проверили все нажатия на места...")

    data = {
        'route': pr1,
        'seats': seats_of_car,
        'cars': cars,
        'chosen_car_number': chosen_car_number,
        'price_list': price_list,
        'price_place_list': price_place_list,
        'train': tr,
        'delta': delta,
        'train_type': train_type

    }
    return render(request, 'search/place_search.html', data)

@login_required
def ticket_forming(request):
    print(" ФУНКЦИЯ ТИКЕТ ФОРМИНГ ЗАПУЩЕНА")
    for key, value in request.POST.items():  # проверялка содержимого request-a
        print('Key: %s' % (key))
        # print(f'Key: {key}') in Python >= 3.7
        print('Value %s' % (value))
    but_data = request.session.get('data')
    message = but_data['message']
    preticket_id = request.session.get('preticket_id')
    chosen_place_number = request.session.get('place_number')
    chosen_place_id = request.session.get('place_id')
    chosen_car_number = request.session.get('car_number')
    price = request.session.get('price')
    tr_id = request.session.get('train_id')
    tr = Train.objects.get(id=tr_id)
    place = Seat.objects.get(id=chosen_place_id)
    pr1 = PreTicket.objects.get(id=preticket_id)  # восстанавливаем preticket по переданному в сессии id
    delta = pr1.arr_time - pr1.dep_time
    train_type = pr1.id_route.id_train.train_type
    print("Переданный через сессию id: ")
    print(preticket_id)
    print("Проверка передачи message: ")
    print(message)  # эта поебень успешно передаёт инфу! урааааааааааааааааааааааа
    print("Выбрано место № " + str(chosen_place_number) + " ( тип: " + place.place_type + ") " + " в вагоне № " + str(
        chosen_car_number))
    print("Цена: " + str(price) + " рублей")
    pr1 = PreTicket.objects.get(id=preticket_id)  # восстанавливаем preticket по переданному в сессии id
    pas = Passanger.objects.filter(user_id=request.user.id)
    form = antigay_PassengerChoiceForm_generator(request.user.id)
    print("Мы предложили на выбор:")
    print(Passanger.objects.filter(user_id=request.user.id))
    data = {
        'form': form,
        'route': pr1,
        'chosen_car_number': chosen_car_number,
        'chosen_place_number': chosen_place_number,
        'price': price,
        'place': place,
        'train': tr,
        'delta': delta,
        'train_type': train_type
    }
    return render(request, 'search/ticket_forming.html', data)

@login_required
def ticket_buy(request):
    print(" ФУНКЦИЯ ТИКЕТ БАЙИНГ ЗАПУЩЕНА")
    for key, value in request.POST.items():  # проверялка содержимого request-a
        print('Key: %s' % (key))
        # print(f'Key: {key}') in Python >= 3.7
        print('Value %s' % (value))

    but_data = request.session.get('data')
    message = but_data['message']
    preticket_id = request.session.get('preticket_id')
    chosen_place_number = request.session.get('place_number')
    chosen_place_id = request.session.get('place_id')
    chosen_car_number = request.session.get('car_number')
    chosen_passenger_id = request.session.get('passenger')
    price = request.session.get('price')
    pr1 = PreTicket.objects.get(id=preticket_id)  # восстанавливаем preticket по переданному в сессии id
    delta = pr1.arr_time - pr1.dep_time
    train_type = pr1.id_route.id_train.train_type

    place = Seat.objects.get(id=chosen_place_id)
    if request.method == 'POST':
        form = PassengerChoiceForm(request.POST)
        if form.is_valid():
            # query=form.cleaned_data['query']
            chosen_passenger = form.cleaned_data['passenger']
            chosen_passenger_id = chosen_passenger.id
            print("В сессии лежал вот такой вот id выбранного пассажира: " + str(chosen_passenger_id))

        else:
            chosen_passenger_id = 1
    pr1 = PreTicket.objects.get(id=preticket_id)  # восстанавливаем preticket по переданному в сессии id
    route = Route.objects.get(id=pr1.id_route.id)
    tr = Train.objects.get(id=route.id_train.id)
    pas = Passanger.objects.get(id=chosen_passenger_id)
    delta = pr1.arr_time - pr1.dep_time
    train_type = pr1.id_route.id_train.train_type
    request.session['passenger'] = chosen_passenger_id
    data = {
        'route': pr1,
        'chosen_car_number': chosen_car_number,
        'chosen_place_number': chosen_place_number,
        'price': price,
        'chosen_passenger': pas,
        'place': place,
        'train': tr,
        'delta': delta,
        'train_type': train_type,
    }
    return render(request, 'search/ticket_buying.html', data)

@login_required
def ticket_buy_completed(request):
    print(" ФУНКЦИЯ ticket_buy_completed ЗАПУЩЕНА")

    but_data = request.session.get('data')
    message = but_data['message']
    preticket_id = request.session.get('preticket_id')
    chosen_place_number = request.session.get('place_number')
    chosen_place_id = request.session.get('place_id')
    chosen_car_number = request.session.get('car_number')
    chosen_passenger_id = request.session.get('passenger')
    print("Возможный пассажир: " + str(chosen_passenger_id))
    price = request.session.get('price')
    pr1 = PreTicket.objects.get(id=preticket_id)  # восстанавливаем preticket по переданному в сессии id
    delta = pr1.arr_time - pr1.dep_time
    train_type = pr1.id_route.id_train.train_type
    place = Seat.objects.get(id=chosen_place_id)

    new_ticket = Ticket(id_preticket=PreTicket.objects.get(id=preticket_id),
                        id_passenger=Passanger.objects.get(id=chosen_passenger_id),
                        id_place=Seat.objects.get(id=chosen_place_id),
                        price=price)
    new_ticket.save()
    print("В качестве билета у нас получилось:")
    print(new_ticket)
    pr1 = PreTicket.objects.get(id=preticket_id)  # восстанавливаем preticket по переданному в сессии id
    route = Route.objects.get(id=pr1.id_route.id)
    tr = Train.objects.get(id=route.id_train.id)
    pas = Passanger.objects.get(id=chosen_passenger_id)
    data = {
        'route': pr1,
        'chosen_car_number': chosen_car_number,
        'chosen_place_number': chosen_place_number,
        'price': price,
        'chosen_passenger': pas,
        'place': place,
        'train': tr,
        'delta': delta,
        'train_type': train_type
    }
    return render(request, 'search/ticket_buying_complete.html', data)


@login_required
def profile_view(request):
    return render(request, 'passenger/profile.html')


@login_required
def user_ticket_list(request):
    print("ФУНКЦИЯ user_ticket_list ЗАПУЩЕНА")
    pas = Passanger.objects.filter(user_id=request.user.id).only('id').all()  # все пассажиры пользователя
    tickets = Ticket.objects.filter(id_passenger__in=pas)  # все билеты, которые купил пользователь на их имена
    len = tickets.count()
    preticket_list = []
    pas_list = []
    place_list = []
    add_info_list = []
    for i in range(len):  # жеска заполняем price_place_list
        preticket = PreTicket.objects.get(id=tickets[i].id_preticket.id)
        preticket_list.append(preticket)
        pas_list.append(Passanger.objects.get(id=tickets[i].id_passenger.id))
        price = tickets[i].price

        place = {'place_number': tickets[i].id_place.place_number,
                 'place_type': tickets[i].id_place.place_type,
                 'car_number': tickets[i].id_place.id_carriage.carriage_number,
                 'train_number': tickets[i].id_place.id_carriage.id_train.train_number,
                 'price': price,
                 'ticket_id': tickets[i].id}
        place_list.append(place)
        delta = preticket.arr_time - preticket.dep_time
        train_type = preticket.id_route.id_train.train_type
        add_info = {'delta': delta, 'train_type': train_type}
        add_info_list.append(add_info)

    mylist = zip(pas_list, preticket_list, place_list, add_info_list)
    data = {
        'mylist': mylist,
    }

    if request.method == 'POST':
        for butt in tickets:  # смотрим, выбрал ли пользователь один из билетов.
            stroka = "b_del_" + str(butt.id)
            if stroka in request.POST:  # если кнопка  УДАЛЕНИЯ с именем stroka была нажата то мы это тут увидим
                print("Кнопка " + stroka + " была нажата!")
                # request.session['pas_to_del_id'] = butt.id
                chosen_ticket = Ticket.objects.get(id=butt.id)
                print(" ЩА УДАЛИМ " + str(chosen_ticket))
                chosen_ticket.delete()
                return redirect('ticket-list')
        print("Мы проверили все нажатия на билеты...")
    return render(request, 'ticket/ticket_list.html', data)


@login_required
def user_passengers_view(request):
    print("ФУНКЦИЯ user_passengers_view ЗАПУЩЕНА")
    pas = Passanger.objects.filter(user_id=request.user.id)  # все пассажиры, которых зарегистрировал пользователь
    data = {
        'pas': pas
    }
    if request.method == 'POST':
        for butt in pas:  # смотрим, выбрал ли пользователь одного из пассажиров.
            stroka = "b_upd_" + str(butt.id)
            print(stroka)
            if stroka in request.POST:  # если кнопка  РЕДАКТ-Я с именем stroka была нажата то мы это тут увидим
                print("Кнопка " + stroka + " была нажата!")
                request.session['pas_to_upd_id'] = butt.id
                return redirect('pas-update')
            stroka = "b_del_" + str(butt.id)
            if stroka in request.POST:  # если кнопка  УДАЛЕНИЯ с именем stroka была нажата то мы это тут увидим
                print("Кнопка " + stroka + " была нажата!")
                request.session['passenger'] = butt.id
                return redirect('pas-delete')
        print("Мы проверили все нажатия на пассажиров...")
    return render(request, 'passenger/passenger_home.html', data)


@login_required
def user_passenger_delete(request):
    chosen_pas_id = request.session.get('passenger')
    chosen_pas = Passanger.objects.get(id=chosen_pas_id)
    tickets = Ticket.objects.filter(id_passenger=chosen_pas_id)
    message = ""
    mylist = []
    if tickets.count() > 0:  # если на этого пассажира есть билеты, то удалять его не следует
        message = "Вы не можете удалить данного пассажира, т.к. вы приобрели на него следующие билеты: "
        len = tickets.count()
        # preticket_pas_list = []
        preticket_list = []
        place_list = []
        add_info_list = []
        for i in range(len):  # жеска заполняем price_place_list
            preticket = PreTicket.objects.get(id=tickets[i].id_preticket.id)
            preticket_list.append(preticket)
            price = tickets[i].price

            place = {'place_number': tickets[i].id_place.place_number,
                     'place_type': tickets[i].id_place.place_type,
                     'car_number': tickets[i].id_place.id_carriage.carriage_number,
                     'train_number': tickets[i].id_place.id_carriage.id_train.train_number,
                     'price': price,
                     'ticket_id': tickets[i].id}
            place_list.append(place)
            delta = preticket.arr_time - preticket.dep_time
            train_type = preticket.id_route.id_train.train_type
            add_info = {'delta': delta, 'train_type': train_type}
            add_info_list.append(add_info)

        mylist = zip(preticket_list, place_list, add_info_list)
    else:
        chosen_pas.delete()
        chosen_pas = 0

    data = {
        'chosen_passenger': chosen_pas,
        'tickets': tickets,
        'message': message,
        'mylist': mylist,
    }
    return render(request, 'passenger/passenger_delete.html', data)


@login_required
def user_passenger_add(request):
    print("Вы создаёте пассажира")

    error = ""
    if request.method == 'POST':
        form = PassengerAddForm(request.POST)
        if form.is_valid():
            print("ФОРМА валидна")
            nfirst_name = form.cleaned_data['first_name']
            nsecond_name = form.cleaned_data['second_name']
            nbirthday = form.cleaned_data['birthday']
            ndocument_type = form.cleaned_data['document_type']
            ndocument_number = form.cleaned_data['document_number']
            nuser = request.user
            new_pas = Passanger(first_name=nfirst_name, second_name=nsecond_name,
                                birthday=nbirthday, doc_type=ndocument_type,
                                doc_info=ndocument_number, user_id=nuser)
            new_pas.save()
            return redirect('pas-list')  # наверное сюда, я хз
        else:
            print("ФОРМА НЕвалидна")
            error = 'Форма заполнена фигово'
    form = PassengerAddForm
    data = {
        'form': form,
        'error': error,
        'page_title': "Добавление нового пассажира",
        'add_buttom_text': "Добавить",
    }
    return render(request, 'passenger/passenger_create.html', data)


@login_required
def user_passenger_update(request):
    print("Вы изменяете пассажира")
    chosen_pas_id = request.session.get('pas_to_upd_id')
    chosen_pas = Passanger.objects.get(id=chosen_pas_id)
    error = ""
    form = PassengerAddForm(initial={'first_name': chosen_pas.first_name, 'second_name': chosen_pas.second_name,
                                     'birthday': chosen_pas.birthday, 'document_type': chosen_pas.doc_type,
                                     'document_number': chosen_pas.doc_info})
    if request.method == 'POST':
        form = PassengerAddForm(request.POST)
        if form.is_valid():
            print("ФОРМА валидна")
            nfirst_name = form.cleaned_data['first_name']
            nsecond_name = form.cleaned_data['second_name']
            nbirthday = form.cleaned_data['birthday']
            ndocument_type = form.cleaned_data['document_type']
            ndocument_number = form.cleaned_data['document_number']
            chosen_pas.first_name = nfirst_name
            chosen_pas.second_name = nsecond_name
            chosen_pas.birthday = nbirthday
            chosen_pas.doc_type = ndocument_type
            chosen_pas.doc_info = ndocument_number
            chosen_pas.save()
            return redirect('pas-list')  # наверное сюда, я хз
        else:
            print("ФОРМА НЕвалидна")
            error = 'Форма заполнена фигово'

    data = {
        'form': form,
        'error': error,
        'page_title': "Редактировать информацию о пассажире",
        'add_buttom_text': "Сохранить изменения",
    }
    return render(request, 'passenger/passenger_create.html', data)


@login_required
def admin_home(request):
    data = {
        'add_buttom_text': "Заглшука",
    }
    return render(request, 'admin/admin_home.html', data)


def admin_views_menu(request):
    data = {
        'add_buttom_text': "Заглшука",
    }
    return render(request, 'admin/admin_views_menu.html', data)

def admin_statistic(request):
    tr_count=Train.objects.all().count()
    car_count=Carriage.objects.all().count()
    car_type_count=Carriage_type.objects.all().count()
    seat_count=Seat.objects.all().count()
    tr_count=Train.objects.all().count()
    rp_count=RoutePoint.objects.all().count()
    st_count=Station.objects.all().count()
    ct_count=City.objects.all().count()
    tic_count=Ticket.objects.all().count()
    money=Ticket.objects.aggregate(Sum("price"))
    ev_price=Ticket.objects.aggregate(Avg('price'))
    ev_places=Carriage_type.objects.aggregate(Sum("number_of_Seat"))
    data = {
        'add_buttom_text': "Заглшука",
        'tr_count': tr_count,
        'car_count':car_count,
            'car_type_count':car_type_count,
        'seat_count':seat_count,
            'tr_count':tr_count,
        'rp_count':rp_count,
            'st_count':st_count,
        'ct_count':ct_count,
            'money':money,
        'ev_price':ev_price,
            'ev_places':ev_places,
    }
    return render(request, 'admin/admin_statistic.html', data)


def route_home(request):
    if request.session.get('first_el') == None:
        first_el = 0
        last_el = 10
        if Route.objects.all().count() < 10:
            last_el = Route.objects.all().count()  # вроде тут не надо отнимать 1
    else:
        first_el = request.session.get('first_el')
        last_el = request.session.get('last_el')
    routes = Route.objects.all()[first_el:last_el]
    total = Route.objects.all().count()
    print("Ваша выборка: ")
    print(routes)
    request.session['first_el'] = first_el
    request.session['last_el'] = last_el
    if request.method == 'POST':
        print("начинаю перебирать")
        for butt in routes:  # смотрим, выбрал ли пользователь один из routes
            stroka = "b_detail_" + str(butt.id)
            print(stroka)
            if stroka in request.POST:
                print(" Кнопка " + stroka + " была нажата!")
                request.session['admin_chosen_route_id'] = butt.id
                return redirect('route-detail')
                print(" Я бесполезная шлюха, неумеющая перенаправлять, извините")
        if "b_add10" in request.POST:
            print("Нажата кнопка b_add10")
            first_el = first_el + 10
            last_el = last_el + 10
            request.session['first_el'] = first_el
            request.session['last_el'] = last_el
            return redirect('route-home')
        if "b_sub10" in request.POST:
            print("Нажата кнопка b_sub10")
            first_el = first_el - 10
            last_el = last_el - 10
            if first_el < 0:
                first_el = 0
                last_el = 10
            request.session['first_el'] = first_el
            request.session['last_el'] = last_el
            return redirect('route-home')
    routes = Route.objects.all()[first_el:last_el]
    data = {
        'elements': routes,
        'first_el': first_el,
        'last_el': last_el,
        'total': total
    }
    return render(request, 'route/route_home.html', data)

def route_view(request):
    print("Просмотр details_view")
    chosen_id = request.session.get('admin_chosen_route_id')
    mes = ""
    if (Route.objects.filter(id=chosen_id).count() > 0):
        route = Route.objects.get(id=chosen_id)
    else:
        mes = "Такого объекта не существует!"
        return render(request, 'route/details_view.html', {'mes': mes})
    rp = RoutePoint.objects.filter(id_route=chosen_id).order_by('departure_time')
    print(rp)
    data = {
        'route': route,
        'mes': mes,
        'rp': rp
    }
    return render(request, 'route/details_view.html', data)

class RouteUpdateView(UpdateView):
    model = Route
    template_name = 'route/route_create.html'  # шаблонч
    form_class = RouteFormM
    success_url = 'r'
class RouteDeleteView(DeleteView):
    model = Route
    template_name = 'route/route_delete.html'  # шаблонч
    success_url = reverse_lazy('route-home')
class RouteCreateView(CreateView):
    template_name = 'route/route_create.html'  # шаблонч
    model = Route
    form_class = RouteFormM
    success_url = 'route-home'

    def form_valid(self, form):
        print("KILLYOURSELF")
        Route.objects.create(**form.cleaned_data)
        return redirect('route-home')

######################################################
def route_point_home(request):
    return object_home(request, RoutePoint, 'admin_chosen_rp_id','route-point-detail',
                'route-point-home', 'route_point/route_point_home.html',
                       'route-point-create')
def route_point_view(request):
    print("Просмотр details_view")
    chosen_id = request.session.get('admin_chosen_rp_id')
    mes = ""
    if (RoutePoint.objects.filter(id=chosen_id).count() > 0):
        rp = RoutePoint.objects.get(id=chosen_id)
    else:
        mes = "Такого объекта не существует!"
        return render(request, 'route_point/details_view.html', {'mes': mes})
    data = {
        'rp': rp,
        'mes': mes,
        }
    return render(request, 'route_point/details_view.html', data)

class RoutePointUpdateView(UpdateView):
    model = RoutePoint
    template_name = 'route_point/route_point_create.html'  # шаблонч
    form_class = RoutePointFormM
    success_url = 'r'

class RoutePointDeleteView(DeleteView):
    model = RoutePoint
    template_name = 'route_point/route_point_delete.html'  # шаблонч
    success_url = reverse_lazy('route-point-home')

class RoutePointCreateView(CreateView):
    template_name = 'route_point/route_point_create.html'  # шаблонч
    model = RoutePoint
    form_class = RoutePointFormM
    success_url = 'route-home'

    def form_valid(self, form):
        print("СОЗДАНИЕ ВЫПОЛНЕНО")
        RoutePoint.objects.create(**form.cleaned_data)
        return redirect('route-point-home')

class RoutePointDetailView(DetailView):
    model = RoutePoint
    template_name = 'route_point/details_view.html'  # шаблонч
    context_object_name = 'route'

###########################
#поезда
#########################
def train_home(request):
    return object_home(request, Train, 'admin_chosen_train_id','train-detail',
                'train-home', 'train/train_home.html',
                       'train-create')

def train_view(request):
    print("Просмотр details_view")
    chosen_id = request.session.get('admin_chosen_train_id')
    mes = ""
    if (Train.objects.filter(id=chosen_id).count() > 0):
        tr = Train.objects.get(id=chosen_id)
        cars=Carriage.objects.filter(id_train=chosen_id)
    else:
        mes = "Такого объекта не существует!"
        return render(request, 'train/details_view.html', {'mes': mes})
    data = {
        'tr': tr,
        'cars':cars,
        'mes': mes,
        }
    return render(request, 'train/details_view.html', data)

class TrainUpdateView(UpdateView):
    model = Train
    template_name = 'train/train_create.html'  # шаблонч
    form_class = TrainFormM
    success_url = 'r'

class TrainDeleteView(DeleteView):
    model = Train
    template_name = 'train/train_delete.html'  # шаблонч
    success_url = reverse_lazy('route-point-home')

class TrainCreateView(CreateView):
    template_name = 'train/train_create.html'  # шаблонч
    model = Train
    form_class = TrainFormM
    success_url = 'route-home'

    def form_valid(self, form):
        print("СОЗДАНИЕ ВЫПОЛНЕНО")
        RoutePoint.objects.create(**form.cleaned_data)
        return redirect('route-point-home')

class TrainDetailView(DetailView):
    model = Train
    template_name = 'train/details_view.html'  # шаблонч
    context_object_name = 'route'
