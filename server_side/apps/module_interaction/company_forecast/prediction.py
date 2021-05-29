import json
import random
import requests
import datetime
import pandas as pd
from decouple import config
from django.utils import translation
from nltk.sentiment import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import TfidfVectorizer
from statsmodels.tsa.statespace.varmax import VARMAX

from server_side.apps.data_interaction import crud
from server_side.apps.module_interaction.additional_modules.danger_test import (
    find_danger,
    clean_text,
    process_text,
)
from server_side.apps.module_interaction.company_forecast import constants


def make_prediction(company, id_disaster, language, info, data):
    market_values = get_market_dates_values(company["market"]["ticker"], data["dates"])
    danger = find_danger(id_disaster, language)
    main_indicator = get_normalize(find_main_indicator(company, language, info, danger))
    varmax = make_varmax_forecast(data["data"], market_values, main_indicator)
    last_date = datetime.datetime.strptime(data["dates"][-1], "%Y-%m-%d")
    for i in range(int(config("STEPS_COMPANY"))):
        last_date += datetime.timedelta(days=constants.DELTA)
        data["dates"].insert(len(data["dates"]), last_date.strftime("%Y-%m-%d*"))
    base_language = translation.get_language()
    translation.activate(language)
    r = lambda: random.randint(0, 255)
    result = {"labels": data["dates"], "datasets": []}
    for item in varmax:
        result["datasets"].append(
            {
                "label": list(item.keys())[0],
                "data": list(item.values())[0],
                "borderColor": "#%02X%02X%02X" % (r(), r(), r()),
            }
        )
    translation.activate(base_language)
    return result


def get_market_dates_values(ticker, dates):
    market_data = get_market_data(ticker)
    if market_data == "":
        return ""
    time_series = market_data["Time Series (Daily)"]
    market_dates = list(time_series.keys())
    market_values = []
    for index, item in enumerate(list(time_series.values())):
        if market_dates[index] in dates:
            market_values.append(float(item["4. close"]))
    market_values.reverse()
    return market_values


def find_main_indicator(company, language, info, danger):
    text = company["description"] + " " + info
    translation_ = crud.read_market_translation_language_id(
        company["market"]["id"], language
    )
    if translation_ == "":
        text = text + " " + translation_
    text = clean_text(text)
    text = process_text(text, language)
    indicator = make_content_analysis(text, language, company["id"])
    return danger * indicator


def make_varmax_forecast(endogenous_data, exogenous_data, danger):
    danger = 1 / 0.001 if danger == 0 else 1 / danger
    data = list()
    length_ = len(list(endogenous_data[0].values())[0])
    for i in range(length_):
        row = [float(list(d.values())[0][i]) for d in endogenous_data]
        data.append(row)
    model = VARMAX(data, exog=exogenous_data, order=(1, 1))
    model_fit = model.fit(disp=False)
    danger_exogenous = []
    random.seed(danger)
    for i in range(int(config("STEPS_COMPANY"))):
        danger_exogenous.append([danger])
        danger += random.random()
    forecast = model_fit.forecast(exog=danger_exogenous, steps=int(config("STEPS_COMPANY")))
    for item in forecast:
        for index, value in enumerate(endogenous_data):
            list(value.values())[0].append(item[index])
    return endogenous_data


def get_market_data(ticker):
    request_data = {
        "function": "TIME_SERIES_DAILY",
        "symbol": ticker,
        "outputsize": "full",
        "apikey": config("ALPHA_VANTAGE_API_KEY"),
    }
    response = requests.get(config("ALPHA_VANTAGE_URL"), params=request_data)
    if response.status_code != 200:
        return ""
    return json.loads(response.text)


def make_content_analysis(text, language, id_company):
    sid = SentimentIntensityAnalyzer()
    crud.update_company_description(id_company, text)
    dictionary = make_dictionary(id_company)
    dictionary.insert(0, text)
    tfidf_vectorizer = TfidfVectorizer()
    values = tfidf_vectorizer.fit_transform(dictionary)
    feature_names = tfidf_vectorizer.get_feature_names()
    data = pd.DataFrame(values.toarray(), columns=feature_names)
    data = data.T[data.T[0] != 0]
    words = list(data.index)
    sum_ = 0
    sum_f = 0
    for word in words:
        polarity = sid.polarity_scores(word)["compound"]
        frequency = data[0][word]
        sum_f += frequency
        sum_ += polarity * frequency
    return sum_ + sum_f


def make_dictionary(id_company):
    companies = crud.read_companies()
    dictionary = []
    for company in companies:
        if company.description_clean != "" and company.id != id_company:
            dictionary.append(company.about_clean)
    return dictionary


def get_normalize(indicator):
    if indicator <= 0:
        return 0
    list_ = [0, indicator, constants.MAX_DANGER]
    return round([100 * float(i) / max(list_) for i in list_][1], 2)
