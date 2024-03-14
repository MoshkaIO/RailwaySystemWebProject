from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [

    path('', views.timetable_home, name='timetable'),

    path('routes', views.route_home, name='route-home'),
    path('route/create', views.RouteCreateView.as_view(), name='route-create'),
    path('route/<int:pk>/update', views.RouteUpdateView.as_view(), name='route-update'),
    path('route/<int:pk>/delete', views.RouteDeleteView.as_view(), name='route-delete'),
    path('route/<int:pk>/r', views.RouteDetailView.as_view(), name='route-detailM'),
    path('route/detail', views.route_view, name='route-detail'),

    path('route_points', views.route_point_home, name='route-point-home'),
    path('route_point/create', views.RoutePointCreateView.as_view(), name='route-point-create'),
    path('route_point/<int:pk>/update', views.RoutePointUpdateView.as_view(), name='route-point-update'),
    path('route_point/<int:pk>/delete', views.RoutePointDeleteView.as_view(), name='route-point-delete'),
    path('route_point/<int:pk>/r', views.RoutePointDetailView.as_view(), name='route-point-detailM'),
    path('route_point/detail', views.route_point_view, name='route-point-detail'),

    path('trains', views.train_home, name='train-home'),
    path('train/create', views.TrainCreateView.as_view(), name='train-create'),
    path('train/<int:pk>/update', views.TrainUpdateView.as_view(), name='train-update'),
    path('train/<int:pk>/delete', views.TrainDeleteView.as_view(), name='train-delete'),
    path('train/<int:pk>/r', views.TrainDetailView.as_view(), name='train-detailM'),
    path('train/detail', views.train_view, name='train-detail'),

    path('pas/<int:pk>', views.PassangerDetailView.as_view(), name='passenger-detail'),
    path('pas', views.passenger_home, name='passenger_home'),

    path('route/<int:pk>', views.RouteSearchDetailView.as_view(), name='route-search-detail'),

    path('route/search', views.route_city_search, name='route-search'),
    path('route/search/place', views.place_search, name='place-search'),
    path('route/search/place/form', views.ticket_forming, name='ticket-form'),
    path('route/search/place/form/buy', views.ticket_buy, name='ticket-buy'),
    path('route/search/place/form/buy/success', views.ticket_buy_completed, name='ticket-buy-success'),

    path('profile', views.profile_view, name='profile'),
    path('profile/tickets', views.user_ticket_list, name='ticket-list'),

    path('profile/passengers', views.user_passengers_view, name="pas-list"),
    path('profile/passengers/create', views.user_passenger_add, name="pas-create"),
    path('profile/passengers/update', views.user_passenger_update, name='pas-update'),
    path('profile/passengers/delete', views.user_passenger_delete, name='pas-delete'),

    path('admin/home', views.admin_home, name='admin-home'),
    path('admin/views', views.admin_views_menu, name='admin-views-menu'),
path('admin/statistic', views.admin_statistic, name='admin-statistic'),

]
