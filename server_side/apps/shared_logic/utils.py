import datetime

import stripe
from django.db.models import QuerySet

from server_side.apps.data_interaction import crud


def is_many(list_item):
    return isinstance(list_item, QuerySet)


def create_token(data):
    token = stripe.Token.create(
        card={
            "number": data['number'].replace(" ", ""),
            "exp_month": int(data['exp_month']),
            "exp_year": int(data['exp_year']),
            "cvc": int(data['cvc'])
        },
    )
    return token


def create_description_payment(username, subscription):
    return str(username) + ': ' + str(subscription)


def get_amount_payment(subscription):
    if subscription == "DEFAULT":
        return 0
    if subscription == "MAXIMUM":
        return 100
    if subscription == "ULTRA":
        return 200


def add_completeness(data):
    for company in data:
        counter = 0
        for item in company:
            if item is not None:
                counter += 1
        company['completeness'] = int((counter / len(company)) * 100)
    return data


def translate_market(data, language):
    if isinstance(data, list):
        for company in data:
            company['market'] = crud.read_market_translate(company['market']['id'], language)
        return data
    data['market'] = crud.read_market_translate(data['market']['id'], language)
    return data


def add_users(data, id_company):
    users = crud.read_workplace_company(id_company)
    data['users_count'] = users.count()
    data['users'] = []
    if users.count() != 0:
        for workplace in users:
            data['users'].append(
                {
                    'username': workplace.user.user.username,
                    'fist_name': workplace.user.user.first_name,
                    'last_name': workplace.user.user.last_name,
                    'position': workplace.position,
                    'date_joined': workplace.user.user.date_joined.strftime('%d.%m.%Y'),
                    'img': workplace.user.img
                }
            )
    return data


def add_position(username):
    workplaces = crud.read_workplace_username(username)
    if workplaces.count() == 0:
        return {
            'position': "",
            'company': ""
        }
    return {
        'position': workplaces[0].position,
        'company': workplaces[0].company.name
    }