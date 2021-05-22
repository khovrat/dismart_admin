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


def add_all_users():
    users = crud.read_users()
    data = []
    if users.count() != 0:
        for user in users:
            data.append(
                {
                    'username': user.user.username
                }
            )
    return {'all_users': data}


def add_markets(data, language):
    data = {
        'companies': data,
        'markets': []
    }
    markets = crud.read_markets()
    if markets.count() != 0:
        for market in markets:
            data['markets'].append(
                {
                    'market_id': market.id,
                    'name': crud.read_market_translation_language_id(language, market.id)
                }
            )
    return data


def change_date(data):
    for item in data:
        item['time'] = datetime.datetime.strptime(item['time'], '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%d.%m.%Y')
    return data


def add_rating_advices(data, username):
    for advice in data:
        advice["rating_my"] = crud.read_advice_rating_username_id(username, advice["advice"]["id"]).rating
        advice["amount"] = crud.read_advice_rating_id(advice["advice"]["id"]).count()
        advice["rating"] = get_average_rating(crud.read_advice_rating_id(advice["advice"]["id"]))
    return data


def get_average_rating(ratings):
    if ratings.count() == 0:
        return round(0, 2)
    sum_ = 0
    for rating in ratings:
        sum_ += rating.rating
    return round(sum_ / ratings.count(), 2)


def get_disasters_type(language):
    disaster_types = crud.read_disaster_type_translation_language(language)
    data = []
    for disaster_type in disaster_types:
        data.append({
            'id': disaster_type.type.id,
            'name': disaster_type.name
        })
    return data


def get_max_amount(data):
    max_ = 0
    for item in data:
        if item["amount"] > max_:
            max_ = item["amount"]
    return max_


def filter_advice(data, filter_):
    new_data = []
    for advice in data:
        if float(advice["rating"]) <= float(filter_["rating"]) and float(advice["amount"]) <= float(filter_["amount"]):
            new_data.append(advice)
    return new_data


def add_disaster_type_translation(data, language):
    for item in data:
        item["advice"]["type"] = crud.read_disaster_type_translation_language_id(item["advice"]["type"]["id"], language).name
    return data
