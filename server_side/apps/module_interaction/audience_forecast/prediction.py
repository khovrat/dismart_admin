from server_side.apps.module_interaction.audience_forecast import constants


def make_prediction(audience, id_disaster, language):
    conservatism = find_conservatism(audience)
    conformity = find_conformity(audience)
    return []


def find_conservatism(audience):
    left_conservatism = int(audience['age_left']) / constants.MAX_AGE
    right_conservatism = int(audience['age_right']) / constants.MAX_AGE
    return left_conservatism * right_conservatism


def find_conformity(audience):
    left_conservatism = int(audience['age_left']) / constants.MAX_AGE
    right_conservatism = int(audience['age_right']) / constants.MAX_AGE
    return left_conservatism * right_conservatism
