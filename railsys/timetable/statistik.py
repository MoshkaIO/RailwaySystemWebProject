from django.shortcuts import redirect, render

from .models  import RoutePoint, Station, Ticket, PreTicket


def checkTicketsIntersection(place,preticket_check):# проверяем, есть ли билеты на конкретное место
    # ищем все билеты на рейс route.
    # ищем билеты на это место
    # если есть, то проверяем пересекаются ли они по времени
    # rt=Route.objects.filter()
    route=preticket_check.id_route
    days=preticket_check.day_dif
    dep_time=preticket_check.dep_time
    arr_time=preticket_check.arr_time
    pretickets=PreTicket.objects.filter(id_route=route).filter(day_dif=days) #все претикеты на route и на текущую дату
    tickets=Ticket.objects.filter(id_preticket__in=pretickets) #все билеты, оформленные с preticket
    tickets_in_place=tickets.filter(id_place=place)
    #if tickets_in_place.count()>0:
    for i in range(tickets_in_place.count()):
        dep_time2=tickets_in_place[i].id_preticket.dep_time
        arr_time2=tickets_in_place[i].id_preticket.arr_time
        if has_overlap(dep_time,arr_time,dep_time2,arr_time2):
            print(" По предварительным данным интервалы "+str(dep_time)+ " - "+str(arr_time)+" и "+
                  str(dep_time2)+" - "+str(arr_time2)+" ПЕРЕСЕКАЮТСЯ")
            print("Подробнее: уже есть билет на место  "+str(tickets_in_place[i].id_place)+" в это время")
            return True

    return False

def has_overlap(a_start, a_end, b_start, b_end):
    latest_start = max(a_start, b_start)
    earliest_end = min(a_end, b_end)
    return latest_start <= earliest_end

def findRPwithStation(station_name,route):
    st=Station.objects.filter(station_name=station_name).only('id') #все станции с таким названием
    rp=RoutePoint.objects.filter()
    return False
def convertSecondsToHoursAndMinutes(seconds):
    #заглушка
    return seconds

def object_home(request, obj_class, session_key, detail_url_name, home_url_name, home_url, create_url_name):
    if request.session.get('first_el') == None:
        first_el = 0
        last_el = 10
        if obj_class.objects.all().count() < 10:
            last_el = obj_class.objects.all().count()  # вроде тут не надо отнимать 1
    else:
        first_el = request.session.get('first_el')
        last_el = request.session.get('last_el')
    rp = obj_class.objects.all()[first_el:last_el]
    total = obj_class.objects.all().count()
    print("Ваша выборка: ")
    print(rp)
    request.session['first_el'] = first_el
    request.session['last_el'] = last_el
    if request.method == 'POST':
        print("начинаю перебирать")
        for butt in rp:  # смотрим, выбрал ли пользователь один из routes
            stroka = "b_detail_" + str(butt.id)
            print(stroka)
            if stroka in request.POST:
                print(" Кнопка " + stroka + " была нажата!")
                request.session[session_key] = butt.id
                return redirect(detail_url_name)
        if "b_add10" in request.POST:
            print("Нажата кнопка b_add10")
            first_el = first_el + 10
            last_el = last_el + 10
            request.session['first_el'] = first_el
            request.session['last_el'] = last_el
            print("Перенаправляю на "+home_url_name)
            return redirect(home_url_name)
        if "b_sub10" in request.POST:
            print("Нажата кнопка b_sub10")
            first_el = first_el - 10
            last_el = last_el - 10
            if first_el < 0:
                first_el = 0
                last_el = 10
            request.session['first_el'] = first_el
            request.session['last_el'] = last_el
            print("Перенаправляю на " + home_url_name)
            return redirect(home_url_name)
    rp = obj_class.objects.all()[first_el:last_el]
    data = {
        'elements': rp,
        'first_el': first_el,
        'last_el': last_el,
        'total': total,
        'home_url_name': home_url_name,
        'create_url_name':create_url_name,
    }
    return render(request, home_url, data)
