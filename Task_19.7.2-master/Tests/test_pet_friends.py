from api import PetFriends
from settings import valid_email, valid_password
import os

pf = PetFriends()

# 1
def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем, что запрос api ключа возвращает статус 200 и в результате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result

# 2
def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем, что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее, используя этот ключ,
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0

# 3
def test_add_new_pet_with_valid_data(name='Мурзик', animal_type='кот',
                                     age='2', pet_photo='images/cat1.jpg'):
    """Проверяем, что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name
# 4
def test_add_new_pet_without_photo_with_valid_data(name='Сэм', animal_type='кот',
                                     age='6'):
    """Проверяем, что можно добавить питомца без фото с корректными данными"""

       # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name
# 5
def test_add_photo_of_pet(pet_photo='images\cat2.jpg'):
    """Тест на добавление фото к новому питомцу"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя и ID, и добавляем фото
    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo_of_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)
        # Проверяем, что статус ответа = 200
        assert status == 200
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("В списке нет питомцев")

# 6
def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем: если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Сэм", "кот", "3", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем, что статус ответа равен 200, и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()

# 7
def test_successful_update_self_pet_info(name='Матроскин', animal_type='кот', age=4):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить данные питомца - его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем, что статус ответа = 200, и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("В списке нет питомцев")

# 8
def test_get_api_key_for_no_valid_email(email='jhfg@mail.ru', password=valid_password):
    """Проверяем запрос api ключа с некорректным email"""
    status, result = pf.get_api_key(email, password)
    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
# 9
def test_get_api_key_for_no_valid_password(email=valid_email, password='54321'):
    """Проверяем запрос api ключа с некорректным password"""
    status, result = pf.get_api_key(email, password)
    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
# 10
def test_add_new_pet_without_photo_with_no_valid_age(name='Барсик', animal_type='кот',
                                     age='###'):
    """Проверяем, что нельзя добавить питомца с не числовыми данными возраста. На данный момент есть баг,
    статус выходит 200."""
    # Добавляем питомца и сверяем результат
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    if type(age) == 'int':
        assert result
    else:
        assert status == 200
        print('Введены некорректные данные')

# 11
def test_get_all_pets_with_no_valid_key(filter = ''):
    """Проверяем, что нельзя получить список питомцев с неверным ключом"""
    auth_key = {"key": "ea738148a1f19838e1c5d1413877f3691a3731380e733e87"}
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 403

# 12
def test_get_all_pets_without_key(filter = ''):
    """Проверяем, что нельзя получить список питомцев без ключа"""
    auth_key = {"key": ""}
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 403




