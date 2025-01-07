class Road:

    def __init__(self,start,end,distance):
        self.start = start # Стартовая точка
        self.end = end # Конечная точка
        self.distance = distance # Дистанция

class Warehouse:

    def __init__(self,name,content = 0): # Имя, содержание склада
        self.name = name
        self.content = content
        self.road_out = None
        self.queue_in = []
        self.queue_out = []

    def __str__(self):
        return 'Склад {} груза {}'.format(self.name,self.content)

    def set_road_out(self,road): # Дорога со склада
        self.road_out = road

    def track_arrived(self,truck): # Грузовик пришел на склад
        self.queue_in.append(truck)
        print('{} прибыл грузовик {}'.format(self.name,truck))

    def get_next_truck(self): # Следующий грузовик на погрузке
        if self.queue_in:
            truck = self.queue_in.pop()
            return truck

    def truck_ready(self,truck): # Грузовик загружен
        self.queue_out.append(truck)
        print('{} грузовик готов {}'.format(self.name, truck))
    def act(self):
        while self.queue_out:
            truck = self.queue_out.pop()
            truck.go_to(road = self.road_out)

class Vehicle:
    fuel_rate = 0 # Расход

    def __init__(self,model):
        self.model = model
        self.fuel = 0


    def __str__(self):
        return '{} топлива {}'.format(self.model,self.fuel)

    def tank_up(self):
        self.fuel +=1000 # Заправиться
        print('{} заправился'.format(self.model))

class Truck(Vehicle):
    fuel_rate = 50
    def __init__(self,model,body_space = 1000):
        super().__init__(model = model)
        self.body_space = body_space
        self.cargo = 0
        self.velocity = 100
        self.place = None
        self.distance_to_target = 0

    def __str__(self):
        res = super().__str__()
        return res + ' груза {}'.format(self.cargo)

    def ride(self):
        self.fuel -= self.fuel_rate
        if self.distance_to_target > self.velocity:
            self.distance_to_target -= self.velocity
            print('{} ехать по дороге , осталось {} '.format(self.model,self.distance_to_target) )
        else:
            self.place.end.track_arrived(self)
            print('{} доехал '.format(self.model))
    def go_to(self,road):
        self.place = road
        self.distance_to_target = road.distance
        print('{} выехал в путь'.format(self.model))

    def act(self):
        if self.fuel <= 10:
            self.tank_up()
        elif isinstance(self.place,Road):
            self.ride()

class AutoLoader(Vehicle):
    fuel_rate = 30
    def __init__(self, model, backet_capacity = 100, warehouse = None, role = 'loader'):
        super().__init__(model=model)
        self.backet_capacity = backet_capacity
        self.warehouse = warehouse
        self.role = role
        self.truck = None

    def __str__(self):
        res = super().__str__()
        return res + ' грузим  {}'.format(self.truck)

    def act(self):
        if self.fuel <= 10:
            self.tank_up()
        elif self.truck is None:
            self.truck = self.warehouse.get_next_truck()
            print('{} взял в работу {}'.format(self.model,self.truck))
        elif self.role == 'loader':
            self.load()
        else: self.unload()
    def load(self):
        self.fuel -= self.fuel_rate
        truck_cargo_rest = self.truck.body_space - self.truck.cargo
        if truck_cargo_rest > self.backet_capacity:
            self.warehouse.content -= self.backet_capacity
            self.truck.cargo += self.backet_capacity
        else:
            self.warehouse.content -=  truck_cargo_rest
            self.truck.cargo += truck_cargo_rest
        print('{} загрузил {}'.format(self.model, self.truck))
        if self.truck.cargo == self.truck.body_space:
            self.warehouse.truck_ready(self.truck)
            self.truck = None
    def unload(self):
        self.fuel -= self.fuel_rate
        if self.truck.cargo >= self.backet_capacity:
            self.truck.cargo -= self.backet_capacity
            self.warehouse.content += self.backet_capacity
        else:
            self.truck.cargo -= self.truck.cargo
            self.warehouse.content += self.truck.cargo
        print('{} разгружал {}'.format(self.model, self.truck))
        if self.truck.cargo == 0:
            self.warehouse.truck_ready(self.truck)
            self.truck = None


TOTAL_CARGO = 100000

moscow = Warehouse(name ='Моска', content = TOTAL_CARGO)
ulyanovsk = Warehouse(name ='Ульяновск',content = 0)

moscow_uulyanovsk = Road(start = moscow,end = ulyanovsk,distance = 1000)
ulyanovsk_moscow = Road(start = ulyanovsk,end = moscow,distance = 1078)

moscow.set_road_out(moscow_uulyanovsk)
ulyanovsk.set_road_out(ulyanovsk_moscow)

loader_1 = AutoLoader(model = 'Bobcat', backet_capacity = 1000, warehouse = moscow , role = 'loader')
loader_2 = AutoLoader(model = 'Lonking', backet_capacity = 500, warehouse = ulyanovsk , role = 'unloader')

truck_1 = Truck(model= 'Камаз' , body_space = 5000)
truck_2 = Truck(model='Газ', body_space=2000)

moscow.track_arrived(truck_1)
moscow.track_arrived(truck_2)

hour = 0
while ulyanovsk.content < TOTAL_CARGO:
    hour += 1
    print('------------- Час {} ---------------'.format(hour))
    truck_1.act()
    truck_2.act()
    loader_1.act()
    loader_2.act()
    moscow.act()
    ulyanovsk.act()
    print(truck_1)
    print(truck_2)
    print(loader_1)
    print(loader_2)
    print(moscow)
    print(ulyanovsk)



