from server_side.apps.shared_logic import utils
from server_side.apps.data_interaction import serializers as ds


def get_serialize_profile(profile):
    return ds.ProfileSerializer(profile).data


def get_serialize_user_review(list_item):
    if utils.is_many(list_item):
        return ds.UserReviewSerializer(list_item, many=True).data
    return ds.UserReviewSerializer(list_item).data


def get_serialize_user_question(list_item):
    if utils.is_many(list_item):
        return ds.UserQuestionSerializer(list_item, many=True).data
    return ds.UserQuestionSerializer(list_item).data


def get_serialize_disaster_type(list_item):
    if utils.is_many(list_item):
        return ds.DisasterTypeSerializer(list_item, many=True).data
    return ds.DisasterTypeSerializer(list_item).data


def get_serialize_disaster_type_translation(list_item):
    if utils.is_many(list_item):
        return ds.DisasterTypeTranslationSerializer(list_item, many=True).data
    return ds.DisasterTypeTranslationSerializer(list_item).data


def get_serialize_disaster(list_item):
    if utils.is_many(list_item):
        return ds.DisasterSerializer(list_item, many=True).data
    return ds.DisasterSerializer(list_item).data


def get_serialize_advice(list_item):
    if utils.is_many(list_item):
        return ds.AdviceSerializer(list_item, many=True).data
    return ds.AdviceSerializer(list_item).data


def get_serialize_advice_translation(list_item):
    if utils.is_many(list_item):
        return ds.AdviceTranslationSerializer(list_item, many=True).data
    return ds.AdviceTranslationSerializer(list_item).data


def get_serialize_advice_rating(list_item):
    if utils.is_many(list_item):
        return ds.AdviceRatingSerializer(list_item, many=True).data
    return ds.AdviceRatingSerializer(list_item).data


def get_serialize_article(list_item):
    if utils.is_many(list_item):
        return ds.ArticleSerializer(list_item, many=True).data
    return ds.ArticleSerializer(list_item).data


def get_serialize_article_rating(list_item):
    if utils.is_many(list_item):
        return ds.ArticleRatingSerializer(list_item, many=True).data
    return ds.ArticleRatingSerializer(list_item).data


def get_serialize_market(list_item):
    if utils.is_many(list_item):
        return ds.MarketSerializer(list_item, many=True).data
    return ds.MarketSerializer(list_item).data


def get_serialize_market_translation(list_item):
    if utils.is_many(list_item):
        return ds.MarketTranslationSerializer(list_item, many=True).data
    return ds.MarketTranslationSerializer(list_item).data


def get_serialize_company(list_item):
    if utils.is_many(list_item):
        return ds.CompanySerializer(list_item, many=True).data
    return ds.CompanySerializer(list_item).data


def get_serialize_workplace(list_item):
    if utils.is_many(list_item):
        return ds.WorkplaceSerializer(list_item, many=True).data
    return ds.WorkplaceSerializer(list_item).data


def get_serialize_audience_type(list_item):
    if utils.is_many(list_item):
        return ds.TargetAudienceTypeSerializer(list_item, many=True).data
    return ds.TargetAudienceTypeSerializer(list_item).data


def get_serialize_audience_type_translation(list_item):
    if utils.is_many(list_item):
        return ds.TargetAudienceTypeTranslationSerializer(list_item, many=True).data
    return ds.TargetAudienceTypeTranslationSerializer(list_item).data


def get_serialize_audience(list_item):
    if utils.is_many(list_item):
        return ds.TargetAudienceSerializer(list_item, many=True).data
    return ds.TargetAudienceSerializer(list_item).data


def get_serialize_market_forecast(list_item):
    if utils.is_many(list_item):
        return ds.MarketForecastSerializer(list_item, many=True).data
    return ds.MarketForecastSerializer(list_item).data


def get_serialize_company_forecast(list_item):
    if utils.is_many(list_item):
        return ds.CompanyForecastSerializer(list_item, many=True).data
    return ds.CompanyForecastSerializer(list_item).data


def get_serialize_company_stress_test(list_item):
    if utils.is_many(list_item):
        return ds.CompanyStressTestSerializer(list_item, many=True).data
    return ds.CompanyStressTestSerializer(list_item).data


def get_serialize_audience_behaviour(list_item):
    if utils.is_many(list_item):
        return ds.TargetAudienceBehaviourSerializer(list_item, many=True).data
    return ds.TargetAudienceBehaviourSerializer(list_item).data
