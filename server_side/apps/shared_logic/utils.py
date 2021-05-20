import stripe


def is_many(list_item):
    return list_item.count() > 1


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

