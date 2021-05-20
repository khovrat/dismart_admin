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
    for company in data:
        company['market'] = crud.read_market_translate(company['market']['id'], language)
    return data
