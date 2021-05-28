import text2emotion as te
from django.utils import translation
from django.utils.translation import ugettext as _
from server_side.apps.data_interaction import crud
from server_side.apps.module_interaction.audience_forecast import constants
from server_side.apps.module_interaction.additional_modules.danger_test import find_danger, process_text, clean_text


def make_prediction(audience, id_disaster, language):
    danger = find_danger(id_disaster, language)
    if danger == '':
        return ''
    conservatism = find_conservatism(audience)
    conformity = find_conformity(audience)
    main_indicator = danger * conformity * conservatism
    profile = find_profile(audience, language)
    base_language = translation.get_language()
    translation.activate(language)
    return [
        {
            "name": _("sympathy"),
            "importance": 1,
            "value": get_normalize(profile["Happy"] * main_indicator, main_indicator)
        },
        {
            "name": _("indifference"),
            "importance": 1,
            "value": get_normalize(profile["Sad"] / main_indicator, 1 / main_indicator)
        },
        {
            "name": _("fear"),
            "importance": 2,
            "value": get_normalize((profile["Fear"] + profile["Angry"]) / main_indicator, 2 / main_indicator)
        },
        {
            "name": _("integrity"),
            "importance": 2,
            "value": get_normalize((profile["Happy"] + profile["Surprise"]) * main_indicator, 2 * main_indicator)
        },
        {
            "name": _("responsibility"),
            "importance": 3,
            "value": get_normalize((profile["Happy"] - profile["Sad"]) * main_indicator, main_indicator)
        },
    ]


def find_conservatism(audience):
    age_left = [constants.MIN_AGE, int(audience['age_left']), constants.MAX_AGE]
    age_right = [constants.MIN_AGE, int(audience['age_right']), constants.MAX_AGE]
    left_conservatism = [float(i) / max(age_left) for i in age_left][1]
    right_conservatism = [float(i) / max(age_right) for i in age_right][1]
    return left_conservatism * right_conservatism


def find_conformity(audience):
    size = [constants.MIN_SIZE, int(audience['size']), constants.MAX_SIZE]
    conformity = [float(i) / max(size) for i in size][1]
    return conformity


def find_profile(audience, language):
    if audience["features_clean"]:
        return te.get_emotion(audience["features_clean"])
    text = audience['features']
    translation = crud.read_audience_type_translation_language_id(audience["type_id"], language)
    if translation == "":
        text = text + ' ' + translation
    text = clean_text(text)
    text = process_text(text, language)
    crud.update_audience_features(audience["id"], text)
    return te.get_emotion(text)


def get_normalize(indicator, max_):
    if indicator <= 0:
        return 0
    list_ = [0, indicator, max_]
    return round([100 * float(i) / max(list_) for i in list_][1])
