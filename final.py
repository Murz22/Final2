import json
import logging

# Настройка логов
logging.basicConfig(filename="shelter.log",
                    level=logging.INFO,
                    format="%(asctime)s - %(message)s")


# Базовый класс
class Animal:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.__health = "good"  # приватное свойство

    def info(self):
        return f"{self.name}, {self.age} лет"


# Наследники
class Dog(Animal):
    pass

class Cat(Animal):
    pass

class Parrot(Animal):
    pass

# Бонусный класс
class Hamster(Animal):
    pass


# Класс приюта
class Shelter:
    def __init__(self):
        self.animals = []

    def add_animal(self, animal):
        self.animals.append(animal)
        logging.info(f"Добавлено животное {animal.name}, возраст {animal.age}")

    def remove_animal(self, name):
        for a in self.animals:
            if a.name == name:
                self.animals.remove(a)
                logging.info(f"Усыновлено/удалено животное {name}")
                return True
        logging.error(f"Животное {name} не найдено")
        return False

    def find_by_name(self, name):
        for a in self.animals:
            if a.name == name:
                logging.info(f"Найдено животное {name}")
                return a
        logging.error(f"Животное {name} не найдено")
        return None

    def show_all(self):
        if not self.animals:
            print("Животных нет")
        for a in self.animals:
            print(a.info())

    def save(self):
        data = [{"type": type(a).__name__, "name": a.name, "age": a.age} for a in self.animals]
        with open("animals.json", "w") as f:
            json.dump(data, f)
        logging.info("Данные сохранены в JSON")

    def load(self):
        try:
            with open("animals.json", "r") as f:
                data = json.load(f)
            for d in data:
                cls = {"Dog": Dog, "Cat": Cat, "Parrot": Parrot, "Hamster": Hamster}.get(d["type"], Animal)
                self.animals.append(cls(d["name"], d["age"]))
            logging.info("Данные загружены из JSON")
        except Exception as e:
            logging.error(f"Ошибка загрузки: {e}")

    # Бонус: статистика
    def stats(self):
        if not self.animals:
            print("Животных нет")
            return
        count = len(self.animals)
        avg_age = sum(a.age for a in self.animals) / count
        oldest = max(self.animals, key=lambda x: x.age)
        print(f"Всего животных: {count}, средний возраст: {avg_age:.1f}, самый старый: {oldest.info()}")


# Консольное меню
shelter = Shelter()
shelter.load()

while True:
    print("\n1 Добавить животное")
    print("2 Показать всех")
    print("3 Найти животное")
    print("4 Усыновление / Удалить")
    print("5 Сохранить")
    print("6 Статистика")
    print("0 Выход")

    choice = input("Выбор: ")

    if choice == "1":
        type_a = input("Тип (dog/cat/parrot/hamster): ").lower()
        name = input("Имя: ")
        age = int(input("Возраст: "))
        cls = {"dog": Dog, "cat": Cat, "parrot": Parrot, "hamster": Hamster}.get(type_a)
        if cls:
            shelter.add_animal(cls(name, age))
        else:
            print("Неизвестный тип животного")

    elif choice == "2":
        shelter.show_all()

    elif choice == "3":
        name = input("Имя: ")
        a = shelter.find_by_name(name)
        if a:
            print(a.info())
        else:
            print("Не найдено")

    elif choice == "4":
        name = input("Имя: ")
        if shelter.remove_animal(name):
            print(f"{name} усыновлен/удален")
        else:
            print("Животное не найдено")

    elif choice == "5":
        shelter.save()

    elif choice == "6":
        shelter.stats()

    elif choice == "0":
        shelter.save()
        break

        #подсказки
        #Shelter хранит список животных и содержит методы добоавления удаления поиска и сохранения
        #Почему  используется JSON? Ответ: JSON удобен для хранения данных его легко читать и записывать в пайтон
        #logging.basicConfig()? Ответ: Он настраивает логирование куда писать логи, уровень логов и формат записи.


