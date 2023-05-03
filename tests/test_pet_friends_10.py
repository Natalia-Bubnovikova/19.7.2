from api import PetFriends
from settings import valid_email, valid_password
import os

pf = PetFriends()


# №1

def test_get_api_key_for_invalid_user(email='ghj@gmail.com', password='123456'):
    """ Негативный тест. Проверяем что если ввести некорректные данные в поля логина и пароля или оставить поля пустыми,
     тест не будет пройден, api_key не будет получен. """

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200


# №2

def test_add_new_pet_without_photo(name='кузя', animal_type='свин',
                                     age='4'):
    """Проверяем что можно добавить питомца с корректными данными без фото"""


    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

# №3
def test_add_photo_of_pet(pet_photo='images/2.jpg'):
    """Проверяем что можно добавить фото для уже существующего питомца"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet_without_photo(auth_key, "Кузя", "свин", 4)
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")


    # Добавляем фото питомца
    pet_id = my_pets['pets'][0]['id']
    status, result = pf.add_photo_of_pet(auth_key, pet_id, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200


# №4
def test_add_new_pet_without_photo_invalid_age(name='кузя', animal_type='свин', age=160):
    """Негативный тест. Добавление питомца без фото с некорректными данными в графе возраст.
    При вводе числа меньше 0 или больше 150 - тест не будет пройден."""


    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца

    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert 0 < int(result['age']) <= 150


# №5
def test_add_new_pet_with_invalid_name(name='Ccслишкомдлиннаякличка', animal_type='пес',
                                     age='7', pet_photo='images/2.jpg'):
    """Негативный тест. Добавление питомца со слишком длинным именем (20 символов и более) или с отсутствием имени в поле ввода.
     При вводе имени, состоящего из 20 символов и более или при невведении имени в графу - тест не будет пройден."""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом

    nameLength = len(result['name'])
    assert status == 200
    assert 1 < nameLength < 20


# №6
def test_add_new_pet_with_invalid_animal_type(name='Челси', animal_type='Мохнатокрылая острозубая собака-енот',
                                     age='7', pet_photo='images/2.jpg'):
    """Негативный тест. Добавление питомца со слишком длинным типом животного (35 символов и более) или с отсутствием типа в поле ввода.
     При вводе типа животного, состоящего из 35 символов и более или при невведении имени в графу - тест не будет пройден."""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом

    typeLength = len(result['animal_type'])
    assert status == 200
    assert 0 < typeLength < 35


# №7
def test_successful_update_self_pet_info_invalid_name(name='Ccслишкомдлиннаякличка', animal_type='Котэ', age=5):
    """Негативный тест.Проверяем возможность изменения текущего имени на слишком длинное имя (20 символов и более) или на отсутствие имени в поле ввода.
     При вводе имени, состоящего из 20 символов и более или при невведении имени в графу - тест не будет пройден."""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Еслди список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        nameLength = len(result['name'])
        assert status == 200
        assert 1 < nameLength < 20
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

# №8
def test_successful_update_self_pet_info_invalid_animal_type(name='Челси', animal_type='Мохнатокрылая острозубая собака-енот' , age=5):
    """Негативный тест. Проверяем возможность изменения текущего типа животного на слишком длинный тип (35 символов и
    более) или на отсутствие типа в поле ввода.
    При вводе типа, состоящего из 35 символов и более или при отсутствии ввода типа в графу - тест не будет пройден."""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Еслди список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        typeLength = len(result['animal_type'])
        assert status == 200
        assert 1 < typeLength < 35
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

# №9
def test_successful_update_self_pet_info_invalid_age(name='кузя', animal_type='свин', age=160):
    """Негативный тест. Проверяем возможность изменения возраста питомца.
    При вводе числа меньше 0 или больше 150 - тест не будет пройден."""


    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца

    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert 0 < int(result['age']) <= 150

# №10
def test_add_new_pet_with_invalid_name_with_numbers(name='%:??;', animal_type='пес', age='7',
                                                    pet_photo='images/2.jpg'):
    """Негативный тест. Добавление питомца со слишком именем, состоящим из цифр или специальных символов.
     При вводе имени, состоящего из цифр или специальных символов - тест не будет пройден."""

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом

    assert status == 200
    assert result['name'].isalpha()







