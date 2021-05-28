import text2emotion as te
from django.utils import translation
from django.utils.translation import ugettext as _

from server_side.apps.data_interaction import crud
from server_side.apps.module_interaction.additional_modules.danger_test import find_danger, process_text, clean_text


def make_prediction(company, id_disaster, language, info):
    danger = find_danger(id_disaster, language)
    if danger == '':
        return ''
    company_profile = find_profile(company, language, info)
    base_language = translation.get_language()
    translation.activate(language)
    data = [
        {
            "name": _("profitability"),
            "importance": 1,
            "value": get_normalize(company_profile["Happy"] * danger, danger)
        },
        {
            "name": _("perplexity"),
            "importance": 1,
            "value": get_normalize(company_profile["Sad"] / danger, 1 / danger)
        },
        {
            "name": _("spontaneity"),
            "importance": 3,
            "value": get_normalize((company_profile["Fear"] + company_profile["Angry"]) / danger, 2 / danger)
        },
        {
            "name": _("stability"),
            "importance": 2,
            "value": get_normalize((company_profile["Happy"] + company_profile["Surprise"]) * danger, 2 * danger)
        },
        {
            "name": _("stress_tolerance"),
            "importance": 1,
            "value": get_normalize((company_profile["Happy"] - company_profile["Sad"]) * danger, danger)
        },
    ]
    translation.activate(base_language)
    return data


def find_profile(company, language, info):
    text = company['description'] + ' ' + info
    translation_ = crud.read_market_translation_language_id(company["market"]["id"], language)
    if translation_ == "":
        text = text + ' ' + translation_
    text = clean_text(text)
    text = process_text(text, language)
    crud.update_company_description(company["id"], text)
    return te.get_emotion(text)


def get_normalize(indicator, max_):
    if indicator <= 0:
        return 0
    list_ = [0, indicator, max_]
    return round([100 * float(i) / max(list_) for i in list_][1])
