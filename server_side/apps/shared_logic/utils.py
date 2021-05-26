import datetime

import stripe
from django.db.models import QuerySet

from server_side.apps.data_interaction import crud


def is_many(list_item):
    return isinstance(list_item, QuerySet)


def create_token(data):
    token = stripe.Token.create(
        card={
            "number": data["number"].replace(" ", ""),
            "exp_month": int(data["exp_month"]),
            "exp_year": int(data["exp_year"]),
            "cvc": int(data["cvc"]),
        },
    )
    return token


def create_description_payment(username, subscription):
    return str(username) + ": " + str(subscription)


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
        company["completeness"] = int((counter / len(company)) * 100)
    return data


def translate_market(data, language):
    if isinstance(data, list):
        for company in data:
            company["market"] = crud.read_market_translate(
                company["market"]["id"], language
            )
        return data
    data["market"] = crud.read_market_translate(data["market"]["id"], language)
    return data


def add_users(data, id_company):
    users = crud.read_workplace_company(id_company)
    data["users_count"] = users.count()
    data["users"] = []
    if users.count() != 0:
        for workplace in users:
            data["users"].append(
                {
                    "username": workplace.user.user.username,
                    "fist_name": workplace.user.user.first_name,
                    "last_name": workplace.user.user.last_name,
                    "position": workplace.position,
                    "date_joined": workplace.user.user.date_joined.strftime("%d.%m.%Y"),
                    "img": workplace.user.img,
                }
            )
    return data


def add_position(username):
    workplaces = crud.read_workplace_username(username)
    if workplaces.count() == 0:
        return {"position": "", "company": ""}
    return {"position": workplaces[0].position, "company": workplaces[0].company.name}


def add_all_users():
    users = crud.read_users()
    data = []
    if users.count() != 0:
        for user in users:
            data.append({"username": user.user.username})
    return {"all_users": data}


def add_markets(data, language):
    data = {"companies": data, "markets": []}
    markets = crud.read_markets()
    if markets.count() != 0:
        for market in markets:
            data["markets"].append(
                {
                    "market_id": market.id,
                    "name": crud.read_market_translation_language_id(
                        language, market.id
                    ),
                }
            )
    return data


def change_date(data):
    for item in data:
        item["time"] = datetime.datetime.strptime(
            item["time"], "%Y-%m-%dT%H:%M:%S.%fZ"
        ).strftime("%d.%m.%Y")
    return data


def add_rating_advices(data, username):
    for advice in data:
        rating = crud.read_advice_rating_username_id(username, advice["advice"]["id"])
        if rating == "":
            advice["rating_my"] = rating
        else:
            advice["rating_my"] = rating.rating
        advice["amount"] = crud.read_advice_rating_id(advice["advice"]["id"]).count()
        advice["rating"] = get_average_rating(
            crud.read_advice_rating_id(advice["advice"]["id"])
        )
    return data


def add_rating_articles(data, username):
    for article in data:
        rating = crud.read_article_rating_username_id(username, article["id"])
        if rating == "":
            article["rating_my"] = rating
        else:
            article["rating_my"] = rating.rating
        article["amount"] = crud.read_article_rating_id(article["id"]).count()
        article["rating"] = get_average_rating(
            crud.read_article_rating_id(article["id"])
        )
    return data


def get_average_rating(ratings):
    if ratings.count() == 0:
        return round(0, 2)
    sum_ = 0
    index_ = 1
    sum_index = 0
    ratings = ratings.order_by("time")
    for rating in ratings:
        sum_ += rating.rating * index_
        sum_index += index_
        index_ += 1
    return round(sum_ / sum_index, 2)


def get_disasters_type(language):
    disaster_types = crud.read_disaster_type_translation_language(language)
    data = []
    for disaster_type in disaster_types:
        data.append({"id": disaster_type.type.id, "name": disaster_type.name})
    return data


def get_companies_user(username):
    companies = crud.read_companies_username(username)
    data = []
    for company in companies:
        data.append({"id": company.id, "name": company.name})
    return data


def get_max_amount(data):
    max_ = 0
    for item in data:
        if item["amount"] > max_:
            max_ = item["amount"]
    return max_


def get_max_term(data):
    max_ = 0
    for item in data:
        if item["term"] > max_:
            max_ = item["term"]
    return max_


def filter_aid(data, filter_):
    new_data = []
    for advice in data:
        if float(advice["rating"]) <= float(filter_["rating"]) and float(
            advice["amount"]
        ) <= float(filter_["amount"]):
            new_data.append(advice)
    return new_data


def filter_disasters(data, filter_):
    new_data = []
    for disaster in data:
        if (
            float(disaster["intensity"]) <= float(filter_["intensity"])
            and float(disaster["term"]) <= float(filter_["term"])
            and float(disaster["readiness_degree"]) <= float(filter_["readiness"])
        ):
            new_data.append(disaster)
    return new_data


def add_disaster_type_translation_advice(data, language):
    for item in data:
        type_ = crud.read_disaster_type_translation_language_id(
            item["advice"]["type"]["id"], language
        )
        if type_ != "":
            item["advice"]["type"] = type_.name
        else:
            item["advice"]["type"] = type_
    return data


def add_disaster_type_translation_article(data, language):
    for item in data:
        type_ = crud.read_disaster_type_translation_language_id(
            item["type"]["id"], language
        )
        if type_ != "":
            item["type"] = type_.name
        else:
            item["type"] = type_
    return data


def get_search_request(language):
    search = ""
    disasters = crud.read_disaster_type_translation_language(language=language)
    if disasters.count() != 0:
        for disaster in disasters:
            search += disaster.name + " OR "
    search += get_base_search_request(language)
    return search


def filter_search_request(base_language, type_):
    search = ""
    if " " in base_language:
        languages = base_language.split()
        for num, language in enumerate(languages):
            search += get_search_disaster_language(type_, language)
            search += get_base_search_request(language)
            if num != len(languages) - 1:
                search += " OR "
    else:
        search += get_search_disaster_language(type_, base_language)
        search += get_base_search_request(base_language)
    return search


def get_search_disaster_language(type_, language):
    search = ""
    if " " in type_:
        types = type_.split()
        for item in types:
            disaster = crud.read_disaster_type_translation_language_id(item, language)
            if disaster != "":
                search += disaster.name + " OR "
    else:
        disaster = crud.read_disaster_type_translation_language_id(type_, language)
        if disaster != "":
            search += disaster.name + " OR "
    return search


def get_base_search_request(language):
    if language == "uk":
        return "катастрофа OR біда OR халепа OR проблема OR криза"
    if language == "en":
        return "catastrophe OR trouble OR problem OR crisis OR disaster"
    if language == "de":
        return "Katastrophe OR Ärger OR Kalamität OR Problem OR Krise"
    if language == "ru":
        return "катастрофа OR беда OR неприятность OR проблема OR кризис"
    if language == "be":
        return "катастрофа OR бяда OR праблема OR праблема OR крызіс"


def get_string(str_, dict_):
    if str_ in dict_:
        return dict_[str_]
    return ""


def add_img(data):
    for item in data:
        item["img"] = item["type"]["img"]
    return data
