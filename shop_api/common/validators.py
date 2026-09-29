from datetime import date
from rest_framework.exceptions import ValidationError, PermissionDenied


def validate_user_age(request):
    token = request.auth
    
    if not token:
        raise PermissionDenied('Авторизуйтесь чтобы выполнить действие.')

    birth_date_str = token.get('birthdate')
    
    if not birth_date_str:
        raise ValidationError('Укажите дату рождения, чтобы создать продукт.')
    
    birth_date = date.fromisoformat(birth_date_str)
    
    # считаем возраст
    today = date.today()
    age = today.year - birth_date.year

     # если день рождения в этом году ещё не наступил уменьшаем возраст на 1
    if today.month < birth_date.month:
        age -= 1
    elif today.month == birth_date.month and today.day < birth_date.day:
        age -= 1
    
    if age < 18:
        raise ValidationError('Вам должно быть 18 лет, чтобы создать продукт.')
    
    return True 