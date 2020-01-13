import sys, argparse, random, csv

from mimesis import Generic
from mimesis.builtins import RussiaSpecProvider
from mimesis.enums import Gender
import time 
import json
import requests


start_time = time.time()


#----LOCALES----
en = 'en'
ru = 'ru'
FILENAME = 'user_data.csv'
API = 'trnsl.1.1.20200112T220923Z.5d6803ff56ec93a3.4c200fab657566d38fc110de249beee8b8323f53'
URL = f'https://translate.yandex.net/api/v1.5/tr.json/translate?lang=ru-be&key={API}'

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
        string_to_mistake = string_to_mistake.replace(string_to_mistake[3], string_to_mistake[5])
    if choice_of_operation == 'add':
        string_to_mistake = string_to_mistake[:choice_of_char]+'f'+string_to_mistake[choice_of_char:]
    return string_to_mistake


def make_mistakes(choice, string_to_mistake):
    if choice == 'full_name':
        choice_of_char = random.randint(0, len(string_to_mistake)-1)
        choice_of_operation = random.choice(operations)
        string_to_mistake = choice_operation_method(string_to_mistake, choice_of_operation,choice_of_char)
    if choice == 'address':
        choice_of_char = random.randint(0, len(string_to_mistake)-1)
        choice_of_operation = random.choice(operations)
        string_to_mistake = choice_operation_method(string_to_mistake, choice_of_operation,choice_of_char)
    if choice == 'phone_number':
        choice_of_char = random.randint(0, len(string_to_mistake)-1)
        choice_of_operation = random.choice(operations)
        string_to_mistake = choice_operation_method(string_to_mistake, choice_of_operation,choice_of_char)
        
    return string_to_mistake

def errors_below_one(number_of_errors):
    k = 1
    while (number_of_errors < 1):
        number_of_errors = number_of_errors * 10
        k = k*10
    number_of_strings_for_error = number_of_errors * k
    return number_of_strings_for_error

def create_list(locale, cl_locale, number_of_strings, number_of_errors):
    generic = Generic(locale)
    person_gender = random.choice(list(Gender))
    r = RussiaSpecProvider()

    for i in range(number_of_strings):
        ###---Full-name----###
        if locale == 'ru':
            
            full_name = f'{generic.person.full_name(gender = person_gender)} {r.patronymic(gender = person_gender)}'
            if cl_locale == 'be_BY':
                params1 = {'text':full_name}
                response = requests.get(URL, params=params1)
                full_name = response.json()['text'][0]
                # full_name = response.json()[text]
        else:
            full_name = f'{generic.person.full_name(gender = person_gender)}'
        
        
            ###########Address###########
        address = f'{generic.address.address()}' 
        if locale == 'ru':
            address = address[:-1] 
            if cl_locale == 'be_BY':
                params1 = {'text':address}
                response = requests.get(URL, params=params1)
                address = response.json()['text'][0]

###################Phone ###################
        if cl_locale == 'us_US':
            phone_number = generic.person.telephone('-1 (###) ###-####')
        if cl_locale == 'ru_RU':
            phone_number = generic.person.telephone('-7 (###) ###-##-##')
        if cl_locale == 'be_BY':
            phone_number = generic.person.telephone('-8 (###) ###-##-##')  
       #MAKING ERRORS
        if number_of_errors < 1:
            stringsToError = errors_below_one(number_of_errors)
            if i == 0:
                pass
            elif (i / stringsToError >= 1 and i % stringsToError == 0):
                # print (i / stringsToError)
                # print (stringsToError % i)
                # print(i)
                choice = random.choice(parameters)
                if choice == 'full_name':
                    full_name = make_mistakes(choice, full_name)
                if choice == 'address':
                    address = make_mistakes(choice, address)
                if choice == 'phone_number':
                    phone = make_mistakes(choice, phone_number)

        else:
            for error_number in range(number_of_errors):
                choice = random.choice(parameters)
                if choice == 'full_name':
                    full_name = make_mistakes(choice, full_name)
                if choice == 'address':
                    address = make_mistakes(choice, address)
                if choice == 'phone_number':
                    phone = make_mistakes(choice, phone_number)
            


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
        list_data = create_list(ru, locale, number_of_strings, number_of_errors)        
        with open(FILENAME, 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file, delimiter = ';')
            for line in list_data:
                writer.writerow(line)

    print(time.time() - start_time)


    