import datetime
import json
import requests
from decouple import config
from django.utils import translation
from django.utils.translation import ugettext as _
from statsmodels.tsa.vector_ar.var_model import VAR
from statsmodels.tsa.statespace.varmax import VARMAX

from server_side.apps.module_interaction.additional_modules.danger_test import find_danger
from server_side.apps.module_interaction.market_forecast import constants


def make_prediction(market, id_disaster, language, method="fast"):
    data = get_market_data(market["ticker"])
    danger = find_danger(id_disaster, language)
    if data == '':
        return ''
    time_series = data["Time Series (Daily)"]
    dates = list(time_series.keys())
    values_low = []
    values_high = []
    for item in time_series.values():
        values_low.append(float(item["3. low"]))
        values_high.append(float(item["2. high"]))
    values_high.reverse()
    values_low.reverse()
    if method == "fast":
        varmax_low, varmax_high = make_var_forecast(values_low, values_high)
    else:
        varmax_low, varmax_high = make_varmax_forecast(values_low[constants.NUMBERS_SLOW:],
                                                       values_high[constants.NUMBERS_SLOW:], danger)
    last_date = datetime.datetime.strptime(dates[0], '%Y-%m-%d')
    for i in range(constants.STEPS):
        last_date += datetime.timedelta(days=constants.DELTA)
        dates.insert(0, last_date.strftime('%Y-%m-%d*'))
    dates.reverse()
    base_language = translation.get_language()
    translation.activate(language)
    data = {
        "labels": dates[constants.NUMBERS:],
        "datasets": [
            {
                'label': _('Varmax_low'),
                'data': varmax_low[constants.NUMBERS:],
                'backgroundColor': "#e35454"
            },
            {
                'label': _('Varmax_high'),
                'data': varmax_high[constants.NUMBERS:],
                'backgroundColor': "#41bd3a"
            }
        ]
    }
    translation.activate(base_language)
    return data


def get_market_data(ticker):
    request_data = {
        "function": "TIME_SERIES_DAILY",
        "symbol": ticker,
        "outputsize": "full",
        "apikey": config("ALPHA_VANTAGE_API_KEY")
    }
    response = requests.get(
        config("ALPHA_VANTAGE_URL"), params=request_data
    )
    if response.status_code != 200:
        return ''
    return json.loads(response.text)


def make_varmax_forecast(values_low, values_high, danger):
    data = list()
    for i, val in enumerate(values_low):
        row = [val, values_high[i]]
        data.append(row)
    model = VARMAX(data, order=(1, 1))
    model_fit = model.fit(disp=False)
    data_exog = [[danger]]
    forecast = model_fit.forecast(exog=data_exog, steps=constants.STEPS)
    for item in forecast:
        values_low.append(item[0])
        values_high.append(item[1])
    return values_low, values_high


def make_var_forecast(values_low, values_high):
    data = list()
    for i, val in enumerate(values_low):
        row = [val, values_high[i]]
        data.append(row)
    model = VAR(data)
    model_fit = model.fit()
    forecast = model_fit.forecast(model_fit.y, steps=constants.STEPS)
    for item in forecast:
        values_low.append(item[0])
        values_high.append(item[1])
    return values_low, values_high
