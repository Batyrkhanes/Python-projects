# ⁡⁢⁣⁢MyProfile app⁡

SEPARATOR = '------------------------------------------'

# user profile
name = ''
age = 0
phone = ''
email = ''
info = ''
ogrnip = 0   #⁡⁢⁣⁣ОГРНИП⁡
inn = ""    #⁡⁢⁣⁣ИНН⁡
index = ""
address = ""

current_account = 0 #⁡⁢⁣⁣Расчетный счет⁡
bank_name = ""
bik = 0        #⁡⁢⁣⁣БИК⁡
correspondent_account = 0 #⁡⁢⁣⁣Корреспондентский счёт⁡

def count_numbers(count_check):
    count = 0
    while count_check > 0:
        count_check //= 10
        count += 1
    return count

def general_info_user(name_parameter, age_parameter, phone_parameter, email_parameter, info_parameter, index_parameter, address_parameter):
    print(SEPARATOR)
    print('Имя:    ', name_parameter)
    if 11 <= age_parameter % 100 <= 19:
        years_parameter = 'лет'
    elif age_parameter % 10 == 1:
        years_parameter = 'год'
    elif 2 <= age_parameter % 10 <= 4:
        years_parameter = 'года'
    else:
        years_parameter = 'лет'

    print('Возраст:', age_parameter, years_parameter)
    print('Телефон:', phone_parameter)
    print('E-mail: ', email_parameter)
    print("Индекс: ", index_parameter)

    if address_parameter:
        print(f"Адрес: {address_parameter}")
    else:
        print("Адрес: -")

    if info_parameter:
        print('')
        print('Дополнительная информация:')
        print(info_parameter)

def full_info_user(ogrnip_parameter, inn_parameter,current_account_parameter, bank_name_parameter, bik_parameter, correspondent_account_parameter):
    general_info_user(name, age, phone, email, info, index, address)
    print()
    print("Информация о предпринимателе")
    print(f"ОГРНИП: {ogrnip_parameter}")
    print(f"ИНН: {inn_parameter}")
    print(f"Банковские реквизиты")
    print(f"Р/c: {current_account_parameter}")
    print(f"Банк: {bank_name_parameter}")
    print(f"БИК: {bik_parameter}")
    print(f"К/с: {correspondent_account_parameter}")

print('Приложение MyProfile')
print('Сохраняй информацию о себе и выводи ее в разных форматах')

while True:
    # main menu
    print(SEPARATOR)
    print('ГЛАВНОЕ МЕНЮ')
    print('1 - Ввести или обновить информацию')
    print('2 - Вывести информацию')
    print('0 - Завершить работу')

    option = int(input('Введите номер пункта меню: '))
    if option == 0:
        break

    if option == 1:
        # submenu 1: edit info
        while True:
            print(SEPARATOR)
            print('ВВЕСТИ ИЛИ ОБНОВИТЬ ИНФОРМАЦИЮ')
            print('1 - Личная информация')
            print("2 - Информация о предпринимателе")
            print('0 - Назад')

            option2 = int(input('Введите номер пункта меню: '))
            if option2 == 0:
                break
            elif option2 == 1:
                # input general info
                name = input('Введите имя: ')
                while True:
                    # validate user age
                    age = int(input('Введите возраст: '))
                    if age > 0:
                        break
                    print('Возраст должен быть положительным')

                uph = input('Введите номер телефона (+7ХХХХХХХХХХ): ')
                phone = ''
                for ch in uph:
                    if ch == '+' or ('0' <= ch <= '9'):
                        phone += ch

                email = input('Введите адрес электронной почты: ')

                index_no_filter = input("Введите почтовый индекс: ")
                for numbers_in_index in index_no_filter:
                    if "0" <= numbers_in_index <= "9":
                        index += numbers_in_index


                address = input("Введите почтовый адрес (без индекса): ")
                info = input('Введите дополнительную информацию:\n')

            elif option2 == 2:
                while True:
                    ogrnip =  int(input("Введите ОГРНИП: "))
                    count_ogrnip = ogrnip
                    count_numbers_check = count_numbers(count_ogrnip)
                    if count_numbers_check == 15:
                        break
                    print("ОГРНИП должен содержать 15 цифр")

                inn = input("Введите ИНН: ")
                while True:
                    current_account = int(input("Введите расчетный счет: "))
                    count_current_account = current_account
                    count_numbers_check = count_numbers(count_current_account)
                    if count_numbers_check == 20:
                        break
                    print("Расчетный счет должен содержать 20 цифр")

                bank_name = input("Введите название банка: ")
                bik = int(input("Введите БИК: "))
                correspondent_account = int(input("Введите корреспондентский счёт: "))
            else:
                print('Введите корректный пункт меню')
    elif option == 2:
        # submenu 2: print info
        while True:
            print(SEPARATOR)
            print('ВЫВЕСТИ ИНФОРМАЦИЮ')
            print('1 - Общая информация')
            print("2 - Вся информация")
            print('0 - Назад')

            option2 = int(input('Введите номер пункта меню: '))
            if option2 == 0:
                break
            elif option2 == 1:
                general_info_user(name, age, phone, email, info, index, address)
            elif option2 == 2:
                full_info_user(ogrnip, inn,current_account, bank_name, bik, correspondent_account)
            else:
                print('Введите корректный пункт меню')
    else:
        print('Введите корректный пункт меню')
