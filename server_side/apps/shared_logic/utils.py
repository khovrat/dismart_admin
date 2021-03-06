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
            market = crud.read_market_translate(company["market"]["id"], language)
            company["market"] = market.name if not market == "" else ""
        return data
    market = crud.read_market_translate(data["market"]["id"], language)
    data["market"] = market.name if not market == "" else ""
    return data


def add_amount_users(data, id_company):
    users = crud.read_workplace_company(id_company)
    data["users_count"] = users.count()
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
            m = crud.read_market_translation_language_id(
                id_market=market.id, language=language
            )
            if m == "":
                data["markets"].append(
                    {
                        "market_id": market.id,
                        "name": m,
                    }
                )
            else:
                data["markets"].append(
                    {
                        "market_id": market.id,
                        "name": m.name,
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


def get_audience_type(language):
    audience_types = crud.read_audience_type_translation_language(language)
    data = []
    for audience_type in audience_types:
        data.append({"id": audience_type.type.id, "name": audience_type.name})
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


def get_max_size(data):
    max_ = 0
    for item in data:
        if item["size"] > max_:
            max_ = item["size"]
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


def filter_audiences(data, filter_):
    new_data = []
    for audience in data:
        if (
            float(audience["size"]) <= float(filter_["size"])
            and float(audience["age_left"]) >= float(filter_["age_left"])
            and float(audience["age_right"]) <= float(filter_["age_right"])
        ):
            new_data.append(audience)
    return new_data


def add_disaster_type_translation_advice(data, language):
    for item in data:
        type_ = crud.read_disaster_type_translation_language_id(
            id_type=item["advice"]["type"]["id"], language=language
        )
        if type_ != "":
            item["advice"]["type"] = type_.name
        else:
            item["advice"]["type"] = type_
    return data


def add_disaster_type_translation_article(data, language):
    for item in data:
        type_ = crud.read_disaster_type_translation_language_id(
            id_type=item["type"]["id"], language=language
        )
        if type_ != "":
            item["type"] = type_.name
        else:
            item["type"] = type_
    return data


def add_audience_type_translation(data, language):
    for item in data:
        type_ = crud.read_audience_type_translation_language_id(
            id_type=item["type"]["id"], language=language
        )
        if type_ != "":
            item["type"] = type_.name
        else:
            item["type"] = type_
    return data


def add_audience_type_translation_single(data, language):
    type_ = crud.read_audience_type_translation_language_id(
        id_type=data["type"]["id"], language=language
    )
    data["type_id"] = data["type"]["id"]
    if type_ != "":
        data["type"] = type_.name
    else:
        data["type"] = type_
    return data


def add_market_translation_single(data, language):
    translation_ = crud.read_market_translation_language_id(
        id_market=data["id"], language=language
    )
    if translation_ != "":
        data["name"] = translation_.name
        data["description"] = translation_.description
    else:
        data["name"] = translation_
        data["description"] = translation_
    return data


def add_company_market_translation_single(data, language):
    translation_ = crud.read_market_translation_language_id(
        id_market=data["market"]["id"], language=language
    )
    if translation_ != "":
        data["market"]["name"] = translation_.name
    else:
        data["market"]["name"] = translation_
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
        return "???????????????????? OR ???????? OR ???????????? OR ???????????????? OR ??????????"
    if language == "en":
        return "catastrophe OR trouble OR problem OR crisis OR disaster"
    if language == "de":
        return "Katastrophe OR ??rger OR Kalamit??t OR Problem OR Krise"
    if language == "ru":
        return "???????????????????? OR ???????? OR ???????????????????????? OR ???????????????? OR ????????????"
    if language == "be":
        return "???????????????????? OR ???????? OR ???????????????? OR ???????????????? OR ????????????"


def get_string(str_, dict_):
    if str_ in dict_:
        return dict_[str_]
    return ""


def add_img(data):
    for item in data:
        item["img"] = item["type"]["img"]
    return data


def add_img_single(data):
    data["img"] = data["type"]["img"]
    return data


def transform_age_group(data):
    for item in data:
        age_group = item["age_group"]
        item.pop("age_group")
        ages = age_group.split("-")
        item["age_left"] = ages[0]
        item["age_right"] = ages[1]
    return data


def transform_age_group_single(data):
    age_group = data["age_group"]
    data.pop("age_group")
    ages = age_group.split("-")
    data["age_left"] = ages[0]
    data["age_right"] = ages[1]
    return data


def add_market_size(data):
    companies = crud.read_companies_market_id(data["id"])
    data["size"] = companies.count()
    return data
