def generate_name() -> str:
    from random import randint
    names = ["Жираф", "Енот", "Медведь", "Собака", "Цыпленок",
            "Куница", "Норка", "Гиппо", "Слоник", "Бобёр",
            "Мышка", "Попугай", "Черепашка", "Крот", "Антилопа"]
    jobs = ["Плотник", "Дизайнер", "Программист", "Архитектор", "Учитель",
        "Шахтёр", "Грузчик", "Врач", "Следователь", "Полицейский",
        "Маляр", "Биолог", "Физик", "Охранник", "Директор"]
    
    return f"{names[randint(0, len(names)-1)]}-{jobs[randint(0, len(jobs)-1)]} {randint(0, 100)}"


def generate_user_tag() -> str:
    from random import randint
    tag_number: int = randint(1, 0xFFFFFF)
    return "@{:06x}".format(tag_number)

if __name__ == "__main__":
    print(generate_user_tag())
