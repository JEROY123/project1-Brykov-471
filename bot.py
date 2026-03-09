import json
import os
from datetime import datetime

DATA_FILE = "data.json"


# =========================
# Робота з файлом
# =========================

def load_data():
    """Завантажує дані з JSON-файлу або створює нову структуру."""
    if not os.path.exists(DATA_FILE):
        return {"budget": 0, "expenses": []}

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_data(data):
    """Зберігає дані у JSON-файл."""
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


# =========================
# Функції бота
# =========================

def show_help():
    """Виводить список команд."""
    print("""
Доступні команди:
- допомога
- встановити бюджет
- додати витрату
- показати витрати
- витрати за датою
- витрати за період
- витрати за категорією
- залишок
- звіт за категоріями
- вийти
""")


def set_budget(data):
    """Встановлення бюджету."""
    amount = float(input("Введіть суму бюджету: "))
    data["budget"] = amount
    save_data(data)
    print("Бюджет встановлено!")


def add_expense(data):
    """Додає нову витрату."""
    amount = float(input("Сума: "))
    category = input("Категорія: ")
    date = input("Дата (рррр-мм-дд): ")
    comment = input("Коментар (необов'язково): ")

    expense = {
        "amount": amount,
        "category": category,
        "date": date,
        "comment": comment
    }

    data["expenses"].append(expense)
    save_data(data)

    print("Витрату додано!")

    # Перевірка перевищення бюджету
    total_spent = sum(exp["amount"] for exp in data["expenses"])
    if total_spent > data["budget"]:
        print("⚠ УВАГА! Бюджет перевищено!")


def show_expenses(data):
    """Показує всі витрати."""
    if not data["expenses"]:
        print("Список витрат порожній.")
        return

    for exp in data["expenses"]:
        print(f"{exp['date']} | {exp['category']} | {exp['amount']} грн | {exp['comment']}")


def expenses_by_date(data):
    """Фільтр за датою."""
    date = input("Введіть дату (рррр-мм-дд): ")
    for exp in data["expenses"]:
        if exp["date"] == date:
            print(f"{exp['date']} | {exp['category']} | {exp['amount']} грн")


def expenses_by_period(data):
    """Фільтр за періодом."""
    start = input("Початкова дата (рррр-мм-дд): ")
    end = input("Кінцева дата (рррр-мм-дд): ")

    start_date = datetime.strptime(start, "%Y-%m-%d")
    end_date = datetime.strptime(end, "%Y-%m-%d")

    for exp in data["expenses"]:
        exp_date = datetime.strptime(exp["date"], "%Y-%m-%d")
        if start_date <= exp_date <= end_date:
            print(f"{exp['date']} | {exp['category']} | {exp['amount']} грн")


def expenses_by_category(data):
    """Фільтр за категорією."""
    category = input("Введіть категорію: ")
    for exp in data["expenses"]:
        if exp["category"].lower() == category.lower():
            print(f"{exp['date']} | {exp['amount']} грн | {exp['comment']}")


def show_balance(data):
    """Показує залишок бюджету."""
    total_spent = sum(exp["amount"] for exp in data["expenses"])
    balance = data["budget"] - total_spent
    print(f"Залишок бюджету: {balance} грн")


def report_by_category(data):
    """Звіт по категоріях."""
    report = {}

    for exp in data["expenses"]:
        category = exp["category"]
        report[category] = report.get(category, 0) + exp["amount"]

    for category, total in report.items():
        print(f"{category}: {total} грн")


# =========================
# Головна функція
# =========================

def main():
    data = load_data()

    print("Вітаю! Це бот 'Фінансовий трекер студента' 😊")
    show_help()

    while True:
        command = input("\nВведіть команду: ").lower()

        if command == "допомога":
            show_help()
        elif command == "встановити бюджет":
            set_budget(data)
        elif command == "додати витрату":
            add_expense(data)
        elif command == "показати витрати":
            show_expenses(data)
        elif command == "витрати за датою":
            expenses_by_date(data)
        elif command == "витрати за період":
            expenses_by_period(data)
        elif command == "витрати за категорією":
            expenses_by_category(data)
        elif command == "залишок":
            show_balance(data)
        elif command == "звіт за категоріями":
            report_by_category(data)
        elif command == "вийти":
            print("До побачення!")
            break
        else:
            print("Невідома команда. Введіть 'допомога'.")


if __name__ == "__main__":
    main()