from difflib import get_close_matches

from ddgs import DDGS
from neura.predictor import Predictor


def ask_number(prompt, lo, hi, as_int=True):
    while True:
        try:
            v = int(input(prompt)) if as_int else float(input(prompt))
            if lo <= v <= hi:
                return v
            print(f"Допустимо: от {lo} до {hi}")
        except ValueError:
            print("Введите число")


def ask_bool(prompt):
    while True:
        v = input(f"{prompt} (да/нет): ").strip().lower()
        if v in ("да", "д", "1", "y", "yes"):
            return 1
        if v in ("нет", "н", "0", "n", "no"):
            return 0


def ask_choice(label, options):
    while True:
        print(f"\n{label}:")
        for i, o in enumerate(options, 1):
            print(f"  {i}. {o}")
        raw = input("Номер или название (Enter = 1): ").strip()
        if not raw:
            return options[0]
        if raw.isdigit() and 1 <= int(raw) <= len(options):
            return options[int(raw) - 1]
        match = get_close_matches(raw, options, n=1, cutoff=0.6)
        if match:
            print(f"-> {match[0]}")
            return match[0]
        print("Такого варианта нет")


def search_offers(company, type_name, ram, ssd, cpu):
    query = f"купить ноутбук {company} {type_name} {cpu} {ram}GB {ssd}GB SSD цена"
    try:
        with DDGS() as ddgs:
            return ddgs.text(query, max_results=3)
    except Exception as e:
        print(f"Поиск недоступен: {e}")
        return []


def main():
    p = Predictor()
    opt = p.options

    print("Введите характеристики ноутбука:")
    specs = {
        "Company": ask_choice("Производитель", opt["Company"]),
        "TypeName": ask_choice("Тип", opt["TypeName"]),
        "Ram": ask_number("RAM, ГБ: ", 2, 128),
        "Weight": ask_number("Вес, кг: ", 0.5, 5, as_int=False),
        "TouchScreen": ask_bool("Сенсорный экран"),
        "Ips": ask_bool("IPS матрица"),
        "Ppi": ask_number("PPI: ", 80, 400, as_int=False),
        "Cpu_brand": ask_choice("Процессор", opt["Cpu_brand"]),
        "HDD": ask_number("HDD, ГБ: ", 0, 4000),
        "SSD": ask_number("SSD, ГБ: ", 0, 4000),
        "Gpu_brand": ask_choice("Видеокарта", opt["Gpu_brand"]),
        "Os": ask_choice("ОС", opt["Os"]),
    }

    r = p.predict(specs)
    print(f"\nRUB: {r['rub']:,.2f}\nUSD: {r['usd']:,.2f}\nTJS: {r['tjs']:,.2f}")

    print("\nПохожие предложения:")
    for i, res in enumerate(search_offers(
            specs["Company"], specs["TypeName"], specs["Ram"],
            specs["SSD"], specs["Cpu_brand"]), 1):
        print(f"{i}. {res.get('title')}\n   {res.get('href')}")


if __name__ == "__main__":
    main()