import re
import hashlib
import json
import os
import datetime


def registr():
    """
    Собирает имя пользователя, пароль пользователя, email пользователя.
    """
    print("Регистрация в сети пиццерий Elliot Pizza\n")

    # Сбор имени пользователя
    username = input("Введите имя пользователю: ").strip()
    if not username:
        print("Имя пользователя должно иметь хотя бы один символ")
        return None
    
    # Сбор пароля пользователя
    password = input("Введите пароль пользователю: ").strip()
    if not password:
        print("Пароль пользователя должен иметь хотя бы один символ")
        return None
    
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    # Сбор email пользователя
    email = input("Введите email пользователю: ").strip().lower()
    email_pattern = re.compile(
        r'^[a-z0-9]+([._-][a-z0-9]+)*@[a-z0-9]+([.-][a-z0-9]+)*\.[a-z]{2,}$'
    )    

    if not email_pattern.match(email):
        print("Некорректный формат email! Формат xxxx@xxxx.xxx")
        return None
    

    users = load_users()  

    
    new_user = {
        "id": len(users) + 1,
        "username": username,
        "email": email,
        "password_hash": password_hash
    }

    # Сохраняем в файл
    users.append(new_user)
    save_users(users)

    print(f"\nРегистрация успешна! Ваш ID: {new_user['id']}")
    return new_user

def login():
    """Выполняет вход пользователя по логину и паролю."""
    print("Вход в аккаунт Elliot Pizza\n")

    username = input("Введите имя пользователя: ").strip()
    password = input("Введите пароль: ").strip()

    if not username or not password:
        print("Все поля обязательны для заполнения!")
        return None

    users = load_users()
    for user in users:
        if user["username"] == username:
            # Проверяем хеш пароля
            entered_hash = hashlib.sha256(password.encode()).hexdigest()
            if user["password_hash"] == entered_hash:
                print(f"Добро пожаловать, {username}!")
                return user
            else:
                print("Неверный пароль!")
                return None

    print("Пользователь не найден!")
    return None
    

def promocodes(total_price):
    """Применяет промокод из JSON-базы."""
    promocode = input("Введите промокод (если есть), или 'nobody0': ").strip().lower()
    promocodes = load_promocodes()

    if promocode in promocodes and promocodes[promocode]["active"]:
        discount = promocodes[promocode]["discount"]
        final_price = total_price * (1 - discount / 100)
        print(f"Промокод принят! Скидка {discount}%.")
        return final_price, discount
    else:
        print("Неверный или неактивный промокод.")
        return total_price, 0


def load_users():
    """Читает users_pizza_elliot.json, возвращает список пользователей."""
    try:
        if not os.path.exists("users_pizza_elliot.json"):
          return []
        with open("users_pizza_elliot.json", "r", encoding="utf-8") as elliot_pizza:
          return json.load(elliot_pizza)
    except json.JSONDecodeError:
        print("Ошибка чтения файла users_pizza_elliot.json!")
        return []    

def save_users(users):
    """Сохраняет список пользователей в users_pizza_elliot.json."""
    with open("users_pizza_elliot.json", "w", encoding="utf-8") as elliot_pizza:
        json.dump(users, elliot_pizza, indent=2, ensure_ascii=False)

def load_orders():
    """Читает orders_pizza_elliot.json."""
    try:
        if not os.path.exists("orders_pizza_elliot.json"):
          return []
        with open("orders_pizza_elliot.json", "r", encoding="utf-8") as elliot_pizza:
          return json.load(elliot_pizza)
    except json.JSONDecodeError:
        print("Ошибка чтения файла orders_pizza_elliot.json!")
        return []    

def save_orders(orders):
    """Сохраняет заказы."""
    with open("orders_pizza_elliot.json", "w", encoding="utf-8") as elliot_pizza:
        json.dump(orders, elliot_pizza, indent=2, ensure_ascii=False)

def load_promocodes():
    """Читает промокоды из файла."""
    try:
        with open("promocodes_pizza_elliot.json", "r", encoding="utf-8") as elliot_pizza:
          return json.load(elliot_pizza)
    except json.JSONDecodeError:
        print("Ошибка чтения файла promocodes_pizza_elliot.json!")
        return []    


# Приветствие с клиентом
print("Здравствуйте!")
print("Это сеть пиццерий Elliot Pizza\n")

print("Хотите ли зарегистрироваться? Вы сможете получать скидки, применять промокоды и тд")


auth = input("Введите вход/регистрация/гость: ").strip().lower()
user = None
if auth == "вход":
    user = login()
elif auth == "регистрация":
    user = registr()
elif auth == "гость":
    print("Продолжаем как Гость.")
else:
    print("Неизвестный вариант. Продолжаем без авторизации.")
    


# Предложить меню клиенту
need_menu = input("Нужно ли вам меню? Скажите 'да' или 'нет': ").lower().strip()


if need_menu == "да":
    menu_food = {
        "Пицца Пепперони": "650 рублей",
        "Пицца Маргарита": "600 рублей",
        "Пицца Ветчина и Сыр": "625 рублей",
        "Пицца Барбекю": "670 рублей",
        "Пицца Цыпленок": "675 рублей",
        "Пицца Песто": "705 рублей",
        "Пицца Песто и Креветки": "800 рублей",
        "Пицца Бургер": "855 рублей",
        "Кока Кола Добрый": "85 рублей",
        "Кока Кола без сахара Добрый": "85 рублей",
        "Спрайт Добрый": "80 рублей",
        "Фанта Добрый": "80 рублей",
        "Мохито": "85 рублей",
        "Чай черный": "55 рублей",
        "Чай зелёный": "65 рублей",
        "Пиво": "95 рублей"
    }
    print("\nМеню:")
    for dish, price in menu_food.items():
        print(f"{dish:<25} {price:>10}")
elif need_menu == "нет":
    print("Видимо, кто‑то знает меню нашей пиццерии!")
else:
    print("Нам не понятен ваш ответ!")

# Уточняем, будет ли заказ
order = input("Будете ли что‑то заказывать? Скажите 'да' или 'нет': ").lower().strip()


if order == "нет":
    print("Жаль, что вы не будете заказывать. Ждём вас в другой раз!")
elif order == "да":
    basket_dish = []  # Список заказанных блюд
    total_price = 0  # Общая сумма заказа


    print("\nНачинаем приём заказа. Чтобы завершить, введите «готово».")


    while True:
        order_food = input("Ваша корзина: ").lower().strip()

        if order_food == "готово":
            break

        # Проверяем, есть ли блюдо в меню
        found = False
        for dish, price_str in menu_food.items():
            if order_food in dish.lower():
                # Извлекаем цену как число
                price = int(price_str.split()[0])  # Убираем «рублей» и берём число
                basket_dish.append(dish)
                total_price += price
                print(f"Добавлено: {dish} ({price_str})")
                found = True
                break

        if not found:
            print("Такого блюда нет в меню. Проверьте написание или посмотрите меню ещё раз.")

    # Выводим итоговый заказ
    if basket_dish:
        print("\nВаш заказ:")
        for item in basket_dish:
            print(f"  {item}")
        print(f"Общая сумма: {total_price} рублей")

        # Применяем промокод (только для зарегистрированных)
        if user is not None:
            final_price, discount = promocodes(total_price)
            if discount > 0:
                print(f"Скидка {discount}%! К оплате: {final_price:.0f} рублей")
            else:
                print(f"К оплате: {final_price:.0f} рублей")
        else:
            print("Промокоды доступны только зарегистрированным пользователям.")
            print(f"К оплате: {total_price} рублей")

        print("Спасибо за заказ! Ждём вас снова!")
    else:
        print("Вы не выбрали ни одного блюда. До свидания!")


    orders = load_orders()
    new_order = {
        "order_id": len(orders) + 1,
        "user_id": user["id"] if user else None,
        "items": basket_dish,
        "total_price": total_price,
        "final_price": final_price,
        "discount": discount,
        "timestamp": datetime.datetime.now().isoformat()
    }
    orders.append(new_order)
    save_orders(orders)
    print(f"Ваш заказ №{new_order['order_id']} сохранён в историю.")

    print("Спасибо за заказ! Ждём вас снова!")