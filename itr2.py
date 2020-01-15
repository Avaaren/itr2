import sys, argparse, random, csv,string

from mimesis import Generic
from mimesis.builtins import RussiaSpecProvider
from mimesis.enums import Gender
import time 
import json
import requests
from faker import Faker

gender = ['male', 'female']
start_time = time.time()
faker_by = Faker('be_BY')
faker_en = Faker('en_US')
faker_ru = Faker('ru_RU')

#----LOCALES----
en = 'en'
ru = 'ru'
by = 'by'
FILENAME = 'user_data.csv'


operations = ['delete', 'move', 'add']
parameters = ['full_name', 'address', 'phone_number']
list1 = []
# af8fa33706408074786

def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('number_of_strings')
    parser.add_argument('locale')
    parser.add_argument('number_of_errors')
    return parser

def choice_operation_method(string_to_mistake, choice_of_operation,choice_of_char):
    if choice_of_operation == 'delete':
        string_to_mistake = string_to_mistake.replace(string_to_mistake[choice_of_char], '')
    if choice_of_operation == 'move':
        # print(string_to_mistake)
        # print(string_to_mistake[choice_of_char])
        string_to_mistake = string_to_mistake.replace(string_to_mistake[choice_of_char], string_to_mistake[choice_of_char+1])
    if choice_of_operation == 'add':
        string_to_mistake = string_to_mistake[:choice_of_char]+random.choice(string.ascii_letters)+string_to_mistake[choice_of_char:]
    return string_to_mistake


def make_mistakes(choice, string_to_mistake):
    if choice == 'full_name':
        if len(string_to_mistake)-2 >= 1:
            choice_of_char = random.randint(0, len(string_to_mistake)-2)
        
            choice_of_operation = random.choice(operations)
            string_to_mistake = choice_operation_method(string_to_mistake, choice_of_operation,choice_of_char)
        else:
            pass
    if choice == 'address':
        if len(string_to_mistake)-2 >= 1:
            choice_of_char = random.randint(0, len(string_to_mistake)-2)
        
            choice_of_operation = random.choice(operations)
            string_to_mistake = choice_operation_method(string_to_mistake, choice_of_operation,choice_of_char)
        else:
            pass
    if choice == 'phone_number':
        if len(string_to_mistake)-2 >= 1:
            choice_of_char = random.randint(0, len(string_to_mistake)-2)
        
            choice_of_operation = random.choice(operations)
            string_to_mistake = choice_operation_method(string_to_mistake, choice_of_operation,choice_of_char)
        else:
            pass
        
    return string_to_mistake

def errors_below_one(number_of_errors):
    k = 1
    while (number_of_errors < 1):
        number_of_errors = number_of_errors * 10
        k = k*10
    
    return number_of_errors*k

def create_list(locale, cl_locale, number_of_strings, number_of_errors):
    generic = Generic(locale)
    person_gender = random.choice(gender)
    for i in range(number_of_strings):
        if locale == 'ru':
            address = faker_ru.street_address()
            if person_gender == 'male':
                full_name = f'{faker_ru.last_name_male()} {faker_ru.first_name_male()} {faker_ru.middle_name_male()}'
            else:
                full_name = f'{faker_ru.last_name_female()} {faker_ru.first_name_female()} {faker_ru.middle_name_female()}'
        if locale == 'en':
            address = faker_en.street_address()
            if person_gender == 'male':
                full_name = f'{faker_en.last_name_male()} {faker_en.first_name_male()} {faker_en.middle_name_male()}'
            else:
                full_name = f'{faker_en.last_name_female()} {faker_en.first_fename_male()} {faker_en.middle_name_female()}'
        if locale == 'by':
            address = faker_by.street_address()
            if person_gender == 'male':
                full_name = f'{faker_by.last_name_male()} {faker_by.first_name_male()} {faker_by.middle_name_male()}'
            else:
                full_name = f'{faker_by.last_name_female()} {faker_by.first_fename_male()} {faker_by.middle_name_female()}'
            
        if cl_locale == 'us_US':
            phone_number = generic.person.telephone('-1 (###) ###-####')
        if cl_locale == 'ru_RU':
            phone_number = generic.person.telephone('-7 (###) ###-##-##')
        if cl_locale == 'be_BY':
            phone_number = generic.person.telephone('-8 (###) ###-##-##')  

        if number_of_errors < 1 and number_of_errors !=0:
            stringsToError = int(errors_below_one(number_of_errors))
            if i == 0:
                pass
            elif (i / stringsToError >= 1 and i % stringsToError == 0):
                choice = random.choice(parameters)
                if choice == 'full_name':
                    full_name = make_mistakes(choice, full_name)
                if choice == 'address':
                    address = make_mistakes(choice, address)
                if choice == 'phone_number':
                    phone_number = make_mistakes(choice, phone_number)
        if number_of_errors == 0:
            pass
        else:
            number_of_errors = int(number_of_errors)
            for error_number in range(number_of_errors):
                choice = random.choice(parameters)
                if choice == 'full_name':
                    full_name = make_mistakes(choice, full_name)
                if choice == 'address':
                    address = make_mistakes(choice, address)
                if choice == 'phone_number':
                    phone_number = make_mistakes(choice, phone_number)
            


        csv_string = [full_name, address, phone_number]
        list1.append(csv_string)
    return list1




if __name__ == '__main__':
    parser = create_parser()
    namespace = parser.parse_args()

    try:
        number_of_strings = int(namespace.number_of_strings)
        locale = namespace.locale
        number_of_errors = float(namespace.number_of_errors)
    except ValueError:
        print('Incorrect args')

    
    
    if locale == 'us_US':
        list_data = create_list(en, locale, number_of_strings, number_of_errors)
        with open(FILENAME, 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file, delimiter = ';')
            for line in list_data:
                writer.writerow(line)

    if locale == 'ru_RU':
        list_data = create_list(ru, locale, number_of_strings, number_of_errors)
        with open(FILENAME, 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file, delimiter = ';')
            for line in list_data:
                writer.writerow(line)

    if locale == 'be_BY':
        list_data = create_list(by, locale, number_of_strings, number_of_errors)        
        with open(FILENAME, 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file, delimiter = ';')
            for line in list_data:
                writer.writerow(line)

    print(time.time() - start_time)


    