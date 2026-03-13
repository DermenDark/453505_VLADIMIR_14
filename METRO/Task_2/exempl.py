def calculate_discount(age, amount, day):
    discount = 0

    # 1 условие
    if age < 18:
        discount += 5
    else:
        discount += 2

    # цикл
    i = 0
    while i < amount:
        # вложенное условие
        if i % 2 == 0:
            discount += 1
        i += 1

    # множественный выбор
    match day:
        case "monday":
            discount += 3
        case "tuesday":
            discount += 2
        case "wednesday":
            discount += 4
        case "friday":
            discount += 6
        case _:
            discount += 1

    return discount