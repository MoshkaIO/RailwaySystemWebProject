 D=1
 """
     @staticmethod


     def get_routes_from_to_city(dep_city,arr_city):
        dep_ct = City.objects.filter(name=Value(dep_city)).only('id').all()
        print(dep_ct)
        print("Название города:"+dep_ct[0].name) #эксперимент 1

        arr_ct = City.objects.filter(name=Value(arr_city)).only('id').all()
        print(arr_ct)

        dep_st = Station.objects.filter(city__in=dep_ct).only('id').all()
        print(dep_st)

        arr_st = Station.objects.filter(city__in=arr_ct).only('id').all()
        print("arr_st= ")
        print(arr_st)

        #dep_rp = RoutePoint.objects.filter(id_station__in=dep_st).only('id_route').all()
        #test_ids = list(TestSubjectSet.objects.all().values_list('test_id', flat=True))
        dep_rp = list(RoutePoint.objects.filter(id_station__in=dep_st).values_list('id_route',flat=True))
        print("dep_rp=")
        print(dep_rp)

        #arr_rp = RoutePoint.objects.filter(id_station__in=arr_st).only('id_route').all()
        arr_rp = list(RoutePoint.objects.filter(id_station__in=arr_st).values_list('id_route', flat=True))
        print("arr_rp=")
        print(arr_rp)

        rt=Route.objects.all()
        print("все rt:")
        print(rt)
        #rt = Route.objects.filter(id__in=dep_rp).filter(id__in=arr_rp).all()

        rt=rt.filter(id__in=dep_rp)
        print("rt через город отправления ")
        print(rt)
        #print(rt[0].id)
        #rt_id=rt.only('id')
        #wtf=RoutePoint.objects.filter(id_route__in=rt_id) #
        #print("содержимое wtf:")
        #print(wtf)
        rt=rt.filter(id__in=arr_rp)
        print("rt через город отправления и город прибытия: ")
        print(rt)
        #dep_rp=RoutePoint.objects.filter(id__in=rt)
        return rt
 
 
 """
 """
     id_route=models.ForeignKey(Route, on_delete=models.CASCADE, null=True, blank=True)
    id_dep_city=models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True)
    id_arr_city=models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True)
    id_dep_st=models.ForeignKey(Station, on_delete=models.CASCADE, null=True, blank=True)
    id_arr_st=models.ForeignKey(Station, on_delete=models.CASCADE, null=True, blank=True)
    id_dep_rp=models.ForeignKey(RoutePoint, on_delete=models.CASCADE, null=True, blank=True)
    id_arr_rp = models.ForeignKey(RoutePoint, on_delete=models.CASCADE, null=True, blank=True)
 """