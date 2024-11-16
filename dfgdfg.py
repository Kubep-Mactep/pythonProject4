import random

def log_function_call(func):
    def wrapper(*args, **kwargs):
        instance = args[0]
        if hasattr(instance, "function_log"):
            instance.function_log.append(func.__name__)
        return func(*args, **kwargs)
    return wrapper

class Human:
    def __init__(self, name="Людина", job=None, home=None, car=None):
        self.name = name
        self.money = 10000
        self.gladness = 50
        self.satiety = 50
        self.job = job
        self.car = car
        self.home = home
        self.first_day = True
        self.days_since_last_job_change = 0
        self.function_log = []

    @log_function_call
    def buy_home(self):
        self.home = House()
        self.money -= 5000

    @log_function_call
    def buy_car(self, brand):
        car_price = brands_of_car[brand]["price"]
        self.car = Auto({brand: brands_of_car[brand]})
        self.money -= car_price

    @log_function_call
    def improve_car(self):
        cars_by_price = sorted(brands_of_car.items(), key=lambda x: x[1]["price"], reverse=True)
        for brand, details in cars_by_price:
            if details["price"] <= self.money and (
                    self.car is None or details["price"] > brands_of_car[self.car.brand]["price"]):
                self.buy_car(brand)
                break

    @log_function_call
    def get_job(self):
        if self.car.drive():
            pass
        else:
            self.to_repair()
            return
        self.job = Job(job_list)

    @log_function_call
    def apply_for_better_job(self):
        if self.days_since_last_job_change < 7:
            return

        potential_jobs = sorted(job_list.items(), key=lambda x: x[1]["salary"], reverse=True)
        for job, details in potential_jobs:
            if details["salary"] > self.job.salary:
                acceptance_chance = 100 if self.first_day else random.randint(0, 100)
                if acceptance_chance >= 50:
                    self.job = Job({job: details})
                    self.first_day = False
                    self.days_since_last_job_change = 0
                    break

    @log_function_call
    def eat(self):
        if self.home.food <= 0:
            self.shopping("food")
        else:
            if self.satiety >= 100:
                self.satiety = 100
                return
            self.satiety += 5
            self.home.food -= 5

    @log_function_call
    def work(self):
        if self.car.drive():
            pass
        else:
            if self.car.fuel < 20:
                self.shopping("fuel")
                return
            else:
                self.to_repair()
                return
        self.money += self.job.salary
        self.gladness -= self.job.gladness_less
        self.satiety -= 4

    @log_function_call
    def shopping(self, manage):
        if self.car.drive():
            pass
        else:
            if self.car.fuel < 20:
                manage = "fuel"
            else:
                self.to_repair()
                return
        if manage == "fuel":
            self.money -= 100
            self.car.fuel += 100
        elif manage == "food":
            self.money -= 50
            self.home.food += 50
        elif manage == "delicacies":
            self.gladness += 10
            self.satiety += 2
            self.money -= 15

    @log_function_call
    def chill(self):
        self.gladness += 10
        self.home.mess += 5

    @log_function_call
    def clean_home(self):
        self.gladness -= 5
        self.home.mess = 0

    @log_function_call
    def to_repair(self):
        self.car.strength += 100
        self.money -= 50

    @log_function_call
    def days_indexes(self, day):
        day_info = f" Сьогодні день {day} життя {self.name} "
        print(f"{day_info:=^50}", "\n")
        human_indexes = f"Показники {self.name}"
        print(f"{human_indexes:^50}", "\n")
        print(f"Гроші – {self.money}")
        print(f"Ситість – {self.satiety}")
        print(f"Щастя – {self.gladness}")
        home_indexes = "Показники будинку"
        print(f"{home_indexes:^50}", "\n")
        print(f"Їжа – {self.home.food}")
        print(f"Безлад – {self.home.mess}")
        car_indexes = f"Показники машини {self.car.brand}"
        print(f"{car_indexes:^50}", "\n")
        print(f"Паливо – {self.car.fuel}")
        print(f"Стан – {self.car.strength}")

    @log_function_call
    def is_alive(self):
        if self.gladness < 0:
            print("Депресія…")
        elif self.satiety < 0:
            print("Помер від голоду…")
        elif self.money < -500:
            print("Збанкрутував…")
        else:
            return True
        return False

    @log_function_call
    def live(self, day):
        if self.home is None:
            self.buy_home()
        if self.car is None:
            self.improve_car()
        if self.job is None:
            self.get_job()
            print(f"Отримав першу роботу: {self.job.job} з зарплатою {self.job.salary}")
        else:
            self.apply_for_better_job()

        self.days_indexes(day)

        if not self.is_alive():
            print(f"Кінець дня {day}. {self.name} більше не може продовжувати життя.\n")
            return

        self.days_since_last_job_change += 1
        dice = random.randint(1, 4)
        if self.satiety < 20:
            print("Йду поїсти")
            self.eat()
        elif self.gladness < 20:
            if self.home.mess > 15:
                print("Хочу відпочити, але в будинку безлад…\n Тому прибираю")
                self.clean_home()
            else:
                print("Час відпочити!")
                self.chill()
        elif self.money < 0:
            print("Час працювати")
            self.work()
        elif self.car.strength < 15:
            print("Потрібно відремонтувати машину")
            self.to_repair()
        elif dice == 1:
            print("Час відпочити!")
            self.chill()
        elif dice == 2:
            print("Час працювати")
            self.work()
        elif dice == 3:
            print("Час прибирати!")
            self.clean_home()
        elif dice == 4:
            print("Час для смаколиків!")
            self.shopping(manage="delicacies")
        print(f"Закінчив день {day}\n")

class Auto:
    def __init__(self, brand_list):
        self.brand = random.choice(list(brand_list))
        self.fuel = brand_list[self.brand]["fuel"]
        self.strength = brand_list[self.brand]["strength"]
        self.consumption = brand_list[self.brand]["consumption"]

    def drive(self):
        if self.strength > 0 and self.fuel >= self.consumption:
            self.fuel -= self.consumption
            self.strength -= 1
            return True
        else:
            print("Машина не може рухатись")
            return False

class House:
    def __init__(self):
        self.mess = 0
        self.food = 0

job_list = {
    "Java developer": {"salary": 50, "gladness_less": 10},
    "Python developer": {"salary": 40, "gladness_less": 3},
    "C++ developer": {"salary": 45, "gladness_less": 25},
    "Rust developer": {"salary": 70, "gladness_less": 1},
}
brands_of_car = {
    "BMW": {"fuel": 100, "strength": 100, "consumption": 6, "price": 5000},
    "Lada": {"fuel": 50, "strength": 40, "consumption": 10, "price": 1500},
    "Volvo": {"fuel": 70, "strength": 150, "consumption": 8, "price": 3000},
    "Ferrari": {"fuel": 80, "strength": 120, "consumption": 14, "price": 10000},
}

class Job:
    def __init__(self, job_list):
        self.job = random.choice(list(job_list))
        self.salary = job_list[self.job]["salary"]
        self.gladness_less = job_list[self.job]["gladness_less"]

nick = Human(name="Нік")
for day in range(1, 365):
    nick.live(day)

print("\nЛог викликаних функцій:")
for function_name in nick.function_log:
    print(f"- {function_name}")