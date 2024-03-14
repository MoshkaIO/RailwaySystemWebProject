from django.contrib.auth.models import User
from django.db import models
from django.db.models import Avg, Min, Value, F, Subquery, Max
import datetime


def id_str(id):
    return " [id: " + str(id) + "] "

class Passanger(models.Model):
    first_name = models.CharField('Имя', max_length=50)
    second_name = models.CharField('Фамилия', max_length=50)
    birthday = models.DateField('Дата рождения')
    doc_type = models.CharField('Тип документа:', max_length=50)
    doc_info = models.CharField('Серия и/или номер документа', max_length=50)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):  # колдовство
        return str(self.id) + " [" + self.first_name + " " + self.second_name + "] " + str(self.user_id)

    class Meta:
        verbose_name = 'Пассажир'
        verbose_name_plural = 'Пассажиры'

class Train(models.Model):
    train_type = models.CharField('Тип поезда', max_length=50)
    train_number = models.IntegerField('Номер поезда')
    def __str__(self):  # колдовство
        return self.train_type + " #" + str(self.id)

    def get_absolute_url(self):
        return f'/train/{self.id}'

    def seat_generator(self):  # генерирует места в конкретном поезде
        print("Запущен генератор мест для поезда № " + str(self.train_number))
        cars = self.get_all_carriages()  # вагоны этого поезда
        car_c = cars.count()
        print("Количество его вагонов: " + str(car_c))
        for i in range(car_c):  # перебираем вагоны этого поезда
            seats = cars[i].get_all_seats()  # все места в вагоне
            if seats.count() == 0:
                print("Обнаружен пустой вагон " + str(cars[i].carriage_number))
                cars[i].generate_all_seats()  # генерируем

    def seat_deleter(self):  # удаляет места в конкретном поезде
        print("Запущен УДАЛЯТОР мест для поезда № " + str(self.train_number))
        cars = self.get_all_carriages()  # вагоны этого поезда
        car_c = cars.count()
        print("Количество его вагонов: " + str(car_c))
        for i in range(car_c):  # перебираем вагоны этого поезда
            seats = cars[i].get_all_seats()  # все места в вагоне
            seats.delete()
            print("Удалены все места в вагоне " + str(i) + " , теперь их там " + str(cars[i].get_all_seats().count()))

    @staticmethod
    def generate_seats():  # для всей поездов активировать генератор мест
        tr = Train.objects.all()
        for i in range(tr.count()):
            tr[i].seat_generator()

    @property
    def count_of_carriages(self):  # ЧИСЛО вагонов в поезде
        return self.carriage_set.all().count()

    @property
    def count_of_seats(self):  # ЧИСЛО мест в поезде
        return self.get_all_seats().count()

    def get_all_carriages(self):  # ВОЗВРАТ вагонов в поезде
        car = self.carriage_set.all()
        return car

    def get_all_seats(self):  # ВОЗВРАТ мест в поезде
        cars = self.get_all_carriages()  # выбор всех вагонов поезда
        seats = Seat.objects.none()
        for i in range(cars.count()):
            seats_of_car = Seat.objects.filter(id_carriage=cars[i].id)
            seats |= seats_of_car

        return seats

    class Meta:
        verbose_name = 'Поезд'
        verbose_name_plural = 'Поезда'

class Carriage_type(models.Model):
    type_name = models.CharField('Разновидность вагона', max_length=50)
    number_of_Seat = models.IntegerField('Число мест в вагоне')

    def __str__(self):  # колдовство
        return str(self.id) + " [ " + self.type_name + " ]"

    def get_absolute_url(self):
        return f'/carriage/{self.id}'

    class Meta:
        verbose_name = 'Тип вагона'
        verbose_name_plural = 'Типы вагонов'

class Carriage(models.Model):
    id_carriage_type = models.ForeignKey(Carriage_type, on_delete=models.CASCADE)
    id_train = models.ForeignKey(Train, on_delete=models.CASCADE)
    carriage_number = models.IntegerField('Номер вагона')

    def __str__(self):  # колдовство
        return str(str(self.id) + " [ №" + str(self.carriage_number) + " в " + str(self.id_train.__str__()) + "] ")

    def get_all_seats(self):
        seats = Seat.objects.filter(id_carriage=self.id)
        return seats

    def generate_all_seats(self):
        car_t = Carriage_type.objects.get(id=self.id_carriage_type.id)
        seats = Seat.objects.filter(id_carriage=self)
        for i in range(car_t.number_of_Seat):
            if seats.filter(place_number=i + 1).count() > 0:
                print("Такое место уже есть!")
                continue
            new_seat = Seat(id_carriage=self, place_number=i + 1, place_type="Обычный", is_occupied=False,
                             price_coef=1)
            new_seat.save()  # сохраняем сгенерированные места
            print(new_seat.__str__())

    def delete_all_seats(self):
        Seat.objects.filter(id_carriage=self.id).delete()  # удаляем все места в вагоне

    def get_all_seats_data(self):
        seats = Seat.objects.filter(id_carriage=self.id)
        seats_query_len = seats.count()
        for i in range(seats_query_len):
            seat_data = seats[i].get_seat_data()
            print(seat_data)

    class Meta:
        verbose_name = 'Вагон'
        verbose_name_plural = 'Вагоны'

class Seat(models.Model):
    id_carriage = models.ForeignKey(Carriage, on_delete=models.CASCADE)
    place_number = models.IntegerField('Номер места')
    place_type = models.CharField('Тип места', max_length=50)
    is_occupied = models.BooleanField('Занято ли место')  # максимально спорная фигня, к удалению!
    price_coef = models.FloatField('Коэффициент цены')

    def __str__(self):  # колдовство
        return str(
            "[" + str(self.id) + "] " + "Место " + str(self.place_number) + " в  вагоне " + self.id_carriage.__str__())

    def get_seat_data(self):
        seat_data = {
            'number': self.place_number,
            'type': self.place_type,
            'occup': self.is_occupied
        }
        return seat_data

    class Meta:
        verbose_name = 'Место'
        verbose_name_plural = 'Места'
class Route(models.Model):
    id_train = models.ForeignKey(Train, on_delete=models.CASCADE)
    base_price = models.IntegerField('Базовая цена билета')  # пока что считается ценой за 1 остановку

    def __str__(self):  # колдовство
        rplist = self.find_dep_arr_obj()
        dep_rp = rplist[0]
        arr_rp = rplist[1]
        if dep_rp.exists():
            if (dep_rp[0].id != arr_rp[0].id):  # если 2 разных йопта
                return str(self.id) + " [ " + str(self.id_train.__str__()) + " ] из " + str(
                    dep_rp[0].__str__()) + " в " + str(arr_rp[0].__str__())
            return str(self.id) + " [ " + str(self.id_train.__str__()) + " ] из " + str(dep_rp[0].__str__())
        return str(self.id) + " [ " + str(self.id_train.__str__()) + " ]"

    def get_absolute_url(self):
        return '/timetable/'

    def find_dep_arr_obj(self):
        dep_rp = RoutePoint.objects.filter(id_route=Value(self.id))
        dep_time = dep_rp.aggregate(dep_time=Min('departure_time'))
        dep_rp = dep_rp.filter(departure_time=dep_time['dep_time'])
        arr_rp = RoutePoint.objects.filter(id_route=Value(self.id))  # это немного лишнее >:(
        arr_time = arr_rp.aggregate(arrive_time=Max('arrive_time'))
        arr_rp = arr_rp.filter(arrive_time=arr_time['arrive_time'])
        rp_list = []
        rp_list.append(dep_rp)
        rp_list.append(arr_rp)
        return rp_list

    def get_dep_arr_data(self):  # информация о станциях отправления и прибытия рейса
        rplist = self.find_dep_arr_obj()
        dep_rp = rplist[0]
        arr_rp = rplist[1]
        dep_rp = dep_rp.first()
        arr_rp = arr_rp.first()
        st_data = {
            'arrive_time': arr_rp.arrive_time,
            'departure_time': dep_rp.departure_time,
            'dep_station_name': dep_rp.id_station.station_name,
            'arr_station_name': arr_rp.id_station.station_name
        }
        return st_data

    def get_absolute_url(self):
        return f'/route/{self.id}'

    def get_count_of_stations(self):
        return self.routepoint_set.all().count()

    def get_all_stations(self):
        return self.routepoint_set.all().order_by('-id_station')

    def get_station(self, s_id):
        return self.routepoint_set.all().filter(id=s_id)

    def get_first_station(self):  # станция отправления
        rp = RoutePoint.objects.get(id_route=self.id).filter(departure_time=Min('departure_time'))
        st = Station.objects.get(id=rp.id_station)
        rp.aggregate(dep_st=st.name)
        return rp

    def get_last_station(self):  # станция прибытия
        return self.routepoint_set.aggregate(arr=Max('arrive_time'))

    def get_rp_in_city(self, city_name):
        ct = City.objects.filter(name=Value(city_name)).only('id').all()
        st = Station.objects.filter(city__in=ct).only('id').all()
        rp = RoutePoint.objects.filter(id_station__in=st).all()
        rp1 = rp.filter(id_route=self.id)
        return rp1

    def get_all_places(self):  # выдача всех мест
        tr = Train.objects.filter(id=self.id_train).only('id').all()  # выбираем поезд
        car = Carriage.objects.filter(id_train__in=tr).only('id').all()  # выбираем вагоны

    @staticmethod
    def get_routes_in_city(city_name):
        ct = City.objects.filter(name=Value(city_name)).only('id').all()
        st = Station.objects.filter(city__in=ct).only('id').all()
        rp = RoutePoint.objects.filter(id_station__in=st).all()
        rt = Route.objects.filter(id__in=rp)
        return rt;

    @staticmethod
    def test1_get_rt_from_to_cityname(dep_city_name, arr_city_name, date):
        dep_ct = City.objects.get(name=Value(dep_city_name))  # город отправления
        arr_ct = City.objects.get(name=Value(arr_city_name))  # город прибытия
        return Route.test1_get_routes_from_to_city(dep_ct, arr_ct, date)  # да поможет нам Перун

    @staticmethod
    def test1_get_routes_from_to_city(dep_city, arr_city, date):
        dep_ct = dep_city
        dep_st = Station.objects.filter(city=dep_ct).only('id').all()  # все станции города
        dep_rp_q = RoutePoint.objects.filter(id_station__in=dep_st)  # все rp в этих станцрях
        dep_rp = list(dep_rp_q.values_list('id_route', flat=True))  # обновлённая версия
        rt_dep = Route.objects.filter(id__in=dep_rp)  # рейсы, в которых есть "dep_rp
        final = Route.objects.none()
        rt_query_len = rt_dep.count()
        for i in range(rt_query_len):  # перебираем все рейсы, в которых есть "dep_rp
            dep_rp_cit = dep_rp_q.filter(id_route=rt_dep[i].id)  # rp города отправления
            drp = dep_rp_cit[0].departure_time  # время отправления из города отправления
            if drp == None:
                continue

            arr_rp = RoutePoint.objects.filter(id_route=rt_dep[i]).filter(
                arrive_time__time__gt=drp)  # ищем все rp данного рейса которые позже
            arr_rp_list = list(arr_rp.values_list('id_station', flat=True))  # обновлённая версия
            arr_st = Station.objects.filter(id__in=arr_rp_list).all()  # станции
            arr_st_list = list(arr_st.values_list('city', flat=True))
            arr_ct = City.objects.filter(id__in=arr_st_list).filter(
                name=Value(arr_city.name)).all()  # города, а среди них город прибытия
            arr_st = Station.objects.filter(city__in=arr_ct).only('id').all()  # все станции города
            arr_rp_q = RoutePoint.objects.filter(id_station__in=arr_st)  # все rp в этих станцрях
            arr_rp_q = arr_rp_q.filter(id_route=rt_dep[i].id)  # конкретный rp ёпта
            if arr_ct.exists():
                data12 = rt_dep[i].get_dep_arr_data()
                distance = rt_dep[i].count_distance(dep_rp_cit[0], arr_rp_q[0])
                # вычисляем разность между date и dep_time
                print("У нас " + str(dep_rp_cit[0].departure_time) + " и " + str(date))

                dep_time = dep_rp_cit[0].departure_time
                arr_time = arr_rp_q[0].arrive_time
                dep_day = dep_time.date()
                date_dif = date - dep_day
                user_dep_time = dep_time + date_dif  # получаем то же время, но нужный день
                user_arr_time = arr_time + date_dif
                print("Разница в днях: " + str(date_dif))
                print("ПРЕДПОЛОЖИТЕЛЬНОЕ время отправления: " + str(user_dep_time))
                print(" прибытие: " + str(user_arr_time))

                bonus = PreTicket(id_route=rt_dep[i], dep_st_name=dep_rp_cit[0].id_station.station_name,
                                  arr_st_name=arr_rp_q[0].id_station.station_name,
                                  dep_time=user_dep_time, arr_time=user_arr_time,
                                  tr_dep_city=data12['dep_station_name'], tr_arr_city=data12['arr_station_name'],
                                  hops_count=distance, day_dif=date_dif.days)
                bonus.save()
                final |= PreTicket.objects.filter(id=bonus.id)
                print("сейчас final=")
                print(final)
                print("Бонусная информация:")
                print(bonus)
                print("расстояние между станциями " + dep_rp_cit[0].id_station.station_name + " и "
                      + arr_rp_q[0].id_station.station_name + " оценивается как "
                      + str(distance))
        return final

    def count_distance(self, rp1, rp2):  # rp1 - откуда, rp2 - куда
        if (rp1.id == rp2.id):
            return 0
        distance = 1
        drp = rp1.departure_time  # время отправления из города отправления
        if drp == None:  # это последняя станция в рейсе.
            return 0;
        arr_rp = RoutePoint.objects.filter(id_route=self.id).filter(
            arrive_time__time__gt=drp).order_by('arrive_time')  # ищем все rp данного рейса которые позже
        length = arr_rp.count()
        for i in range(length):
            if arr_rp[i].id != rp2.id:
                distance += 1
            else:
                return distance
        return 0  # ничего не нашлось

    class Meta:
        verbose_name = 'Рейс'
        verbose_name_plural = 'Рейсы'

class Station(models.Model):
    station_name = models.CharField('Название станции', max_length=50)
    city = models.ForeignKey("City", on_delete=models.CASCADE)
    def __str__(self):  # колдовство
        return id_str(self.id) + self.station_name + " ( " + self.city.name + " )"

    def get_absolute_url(self):
        return f'/Station/{self.id}'

    def get_city(self):
        return self.city.name

    class Meta:
        verbose_name = 'Станция'
        verbose_name_plural = 'Станция'

class RoutePoint(models.Model):
    id_station = models.ForeignKey(Station, on_delete=models.CASCADE)
    id_route = models.ForeignKey(Route, on_delete=models.CASCADE)
    arrive_time = models.DateTimeField('Время прибытия', null=True, blank=True)
    departure_time = models.DateTimeField('Время отправления', null=True, blank=True)
    boarding = models.BooleanField('Посадка в поезд',default=True)

    def __str__(self):  # колдовство
        if self.departure_time == None:
            return id_str(self.id) + self.id_station.station_name + "  приб: " + str(self.arrive_time)
        if self.arrive_time == None:
            return id_str(self.id) + self.id_station.station_name + " отпр: " + str(self.departure_time)
        return id_str(self.id) + self.id_station.station_name + "  приб: " + str(self.arrive_time) + " ; отпр: " + str(
            self.departure_time)

    def get_absolute_url(self):
        return f'/RoutePoint/{self.id}'

    def get_station_inf(self):
        st = Station.objects.get(id=self.id_station.id)
        return {'name': st.station_name}

    def get_city_of_station(self):
        return self.id_station.get_city()

    class Meta:
        verbose_name = 'Остановка'
        verbose_name_plural = 'Остановки'

class City(models.Model):
    name = models.CharField('Название населённого пункта', max_length=50)
    region = models.CharField('Регион', max_length=50)

    def __str__(self):  # колдовство
        return self.name + " " + self.region + " [id: " + str(self.id) + "] "

    def get_absolute_url(self):
        return f'/RoutePoint/{self.id}'

    class Meta:
        verbose_name = 'Населённый пункт'
        verbose_name_plural = 'Населённые пункты'


class PreTicket(models.Model):
    id_route = models.ForeignKey(Route, on_delete=models.CASCADE)
    dep_st_name = models.CharField('Название станции отправления', max_length=50, null=True, blank=True)
    arr_st_name = models.CharField('Название станции прибытия', max_length=50, null=True, blank=True)
    dep_time = models.DateTimeField('Время отправления', null=True, blank=True)
    arr_time = models.DateTimeField('Время прибытия', null=True, blank=True)
    tr_dep_city = models.CharField('Город отправления рейса', max_length=50, null=True, blank=True)
    tr_arr_city = models.CharField('Город прибытия рейса', max_length=50, null=True, blank=True)
    hops_count = models.IntegerField('Число хопов между этими станциями')
    day_dif = models.IntegerField('Разница в днях от эталона')

    def __str__(self):  # колдовство
        return "Талон: " + str(self.dep_time) + " " + self.dep_st_name + " " + str(
            self.arr_time) + " " + self.arr_st_name

    def get_absolute_url(self):
        return f'/route/{self.id}'

class Ticket(models.Model):
    id_preticket = models.ForeignKey(PreTicket, on_delete=models.PROTECT)
    id_passenger = models.ForeignKey(Passanger, on_delete=models.PROTECT)
    id_place = models.ForeignKey(Seat, on_delete=models.PROTECT)
    price = models.IntegerField('Цена за билет')

    def __str__(self):  # колдовство
        return str(self.id_preticket.__str__()) + " " + str(self.id_passenger.__str__())
