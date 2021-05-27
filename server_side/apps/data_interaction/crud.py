from django.contrib.auth.models import User

import server_side.apps.data_interaction.models as dm


def create_profile(data):
    if User.objects.filter(username=data["username"]).exists():
        return False
    user = User(
        username=data["username"],
        first_name=data["first_name"],
        last_name=data["last_name"],
        email=data["email"],
    )
    user.set_password(data["password"])
    user.save()
    if "img" in data:
        user.profile.img = data["img"]
    if "subscription" in data:
        user.profile.subscription = data["subscription"]
    user.save()
    return True


def create_company(data):
    if dm.Company.objects.filter(name=data["name"]).exists():
        return False
    company = dm.Company(
        name=data["name"],
        website=data["website"],
        size=data["size"],
        revenue=float(data["revenue"].replace(',', '.')),
        location=data["location"],
        description=data["description"],
        img=data["img"],
        market_id=data["market_id"]

    )
    company.save()
    return True


def create_workplace(data):
    if dm.Workplace.objects.filter(user__user__username=data["username"],
                                   company__name=data["name"],
                                   position=data["position"]).exists():
        return False
    workplace = dm.Workplace(
        user_id=dm.Profile.objects.get(user__username=data["username"]).id,
        company_id=dm.Company.objects.get(name=data["name"]).id,
        position=data["position"]
    )
    workplace.save()
    return True


def create_advice_rating(data):
    if dm.AdviceRating.objects.filter(user__user__username=data["username"], advice_id=data["id"]).exists():
        update_advice_rating(data)
        return True
    advice_rating = dm.AdviceRating(
        user_id=dm.Profile.objects.get(user__username=data["username"]).id,
        advice_id=data["id"],
        rating=data["rating"]
    )
    advice_rating.save()
    return True


def create_article_rating(data):
    if dm.ArticleRating.objects.filter(user__user__username=data["username"], article_id=data["id"]).exists():
        update_article_rating(data)
        return True
    article_rating = dm.ArticleRating(
        user_id=dm.Profile.objects.get(user__username=data["username"]).id,
        article_id=data["id"],
        rating=data["rating"]
    )
    article_rating.save()
    return True


def create_review(data):
    profile = read_profile_by_username(data["username"])
    review = dm.UserReview(user_id=profile.id, review=data["review"])
    review.save()


def create_article(data):
    if dm.Article.objects.filter(author=data["username"], name=data["name"]).exists():
        return False
    article = dm.Article(
        author=data["username"],
        name=data["name"],
        type_id=data["type"],
        language=data["language"],
        img=data["img"],
        text=data["text"]
    )
    article.save()
    return True


def create_disaster(data):
    profile = read_profile_by_username(data["username"])
    disaster = dm.Disaster(
        user_id=profile.id,
        intensity=data["intensity"],
        type_id=data["type"],
        term=data["term"],
        readiness_degree=data["readiness"],
        about=data["about"]
    )
    disaster.save()
    return True


def create_audience(data):
    audience = dm.TargetAudience(
        company_id=data["company"],
        type_id=data["type"],
        size=data["size"],
        age_group=data["age_left"] + '-' + data["age_right"],
        features=data["features"]
    )
    audience.save()
    return True


def create_telegram_user(user, language):
    if dm.TelegramUser.objects.filter(user=user, language=language).exists:
        return
    user = dm.TelegramUser(user=user, language=language)
    user.save()


def read_amount_users():
    return dm.User.objects.count()


def read_amount_companies():
    return dm.Company.objects.count()


def read_amount_articles():
    return dm.Article.objects.count()


def read_amount_advices():
    return dm.Advice.objects.count()


def read_profile_by_username(username):
    return dm.Profile.objects.get(user__username=username)


def read_profile_by_email(email):
    return dm.Profile.objects.get(user__email=email)


def read_counters(username):
    return {
        "ratings": dm.AdviceRating.objects.filter(user__user__username=username).count()
                   + dm.ArticleRating.objects.filter(user__user__username=username).count(),
        "articles": dm.Article.objects.filter(author=username).count(),
        "disasters": dm.Disaster.objects.filter(user__user__username=username).count(),
    }


def read_companies_username(username):
    user = dm.Profile.objects.get(user__username=username)
    return dm.Company.objects.filter(workplace__user__user_id=user.user_id).order_by('name')[1:]


def read_companies_id(id_company):
    if dm.Company.objects.filter(pk=id_company).exists():
        return dm.Company.objects.get(pk=id_company)
    return None


def read_market_translate(id_market, language):
    if dm.MarketTranslation.objects.filter(market_id=id_market, language=language).exists():
        return dm.MarketTranslation.objects.get(market_id=id_market, language=language)
    return ''


def read_workplace_company(id_company):
    return dm.Workplace.objects.filter(company_id=id_company)


def read_workplace_username(username):
    return dm.Workplace.objects.filter(user__user__username=username)


def read_users():
    return dm.Profile.objects.all()


def read_markets():
    return dm.Market.objects.all()


def read_market_translation_language_id(language, market_id):
    if dm.MarketTranslation.objects.filter(market_id=market_id, language=language).exists():
        return dm.MarketTranslation.objects.get(market_id=market_id, language=language)
    return ''


def read_reviews():
    return dm.UserReview.objects.all()


def read_reviews_username(username):
    return dm.UserReview.objects.filter(user__user__username=username)


def read_advice_translation_language(language):
    return dm.AdviceTranslation.objects.filter(language=language)


def read_advice_translation_language_type(language, id_type):
    return dm.AdviceTranslation.objects.filter(language=language, advice__type_id=id_type)


def read_advice_rating_id(id_advice):
    return dm.AdviceRating.objects.filter(advice_id=id_advice)


def read_advice_rating_username_id(username, id_advice):
    if dm.AdviceRating.objects.filter(user__user__username=username, advice_id=id_advice).exists():
        return dm.AdviceRating.objects.get(user__user__username=username, advice_id=id_advice)
    return ''


def read_article():
    return dm.Article.objects.all()


def read_article_rating_id(id_article):
    return dm.ArticleRating.objects.filter(article_id=id_article)


def read_article_rating_username_id(username, id_article):
    if dm.ArticleRating.objects.filter(user__user__username=username, article_id=id_article).exists():
        return dm.ArticleRating.objects.get(user__user__username=username, article_id=id_article)
    return ''


def read_disaster_type_translation_language(language):
    return dm.DisasterTypeTranslation.objects.filter(language=language)


def read_disaster_type_translation_language_id(id_type, language):
    if dm.DisasterTypeTranslation.objects.filter(type_id=id_type, language=language).exists():
        return dm.DisasterTypeTranslation.objects.get(type_id=id_type, language=language)
    return ''


def read_audience_type_translation_language(language):
    return dm.TargetAudienceTypeTranslation.objects.filter(language=language)


def read_audience_type_translation_language_id(id_type, language):
    if dm.TargetAudienceTypeTranslation.objects.filter(type_id=id_type, language=language).exists():
        return dm.TargetAudienceTypeTranslation.objects.get(type_id=id_type, language=language)
    return ''


def read_article_language(language):
    return dm.Article.objects.filter(language=language)


def read_article_language_type(language, id_type):
    return dm.Article.objects.filter(language=language, type_id=id_type)


def read_telegram_user_user(user):
    return dm.TelegramUser.objects.get(user=user)


def read_disaster_user(username):
    return dm.Disaster.objects.filter(user__user__username=username)


def read_disaster_user_type(username, type_id):
    return dm.Disaster.objects.filter(user__user__username=username, type_id=type_id)


def read_disaster_id(id_disaster):
    if dm.Disaster.objects.filter(pk=id_disaster).exists():
        return dm.Disaster.objects.get(pk=id_disaster)
    return ''


def read_disasters():
    return dm.Disaster.objects.all()


def read_audiences_company(company):
    return dm.TargetAudience.objects.filter(company_id=company)


def read_audiences_id(id_audience):
    if dm.TargetAudience.objects.filter(pk=id_audience).exists():
        return dm.TargetAudience.objects.get(pk=id_audience)
    return ''


def read_audiences():
    return dm.TargetAudience.objects.all()


def update_profile_password(data):
    user = dm.User.objects.get(username=data["username"])
    user.set_password(data["password"])
    user.save()


def update_profile_subscription(data):
    user = dm.Profile.objects.get(user__username=data["username"])
    user.subscription = data["subscription"]
    user.save()


def update_profile_image(data):
    user = dm.Profile.objects.get(user__username=data["username"])
    user.img = data["img"]
    user.save()


def update_profile(data):
    if (
            data["username"] != data["username_new"]
            and User.objects.filter(username=data["username_new"]).exists()
    ):
        return False
    user = dm.User.objects.get(username=data["username"])
    user.username = data["username_new"]
    user.email = data["email"]
    user.first_name = data["first_name"]
    user.last_name = data["last_name"]
    user.save()
    return True


def update_company(data):
    if (
            data["name"] != data["name_new"]
            and dm.Company.objects.filter(name=data["name_new"]).exists()
    ):
        return False
    company = dm.Company.objects.get(name=data["name"])
    company.name = data["name_new"]
    company.website = data["website"]
    company.size = data["size"]
    company.revenue = float(data["revenue"].replace(',', '.'))
    company.location = data["location"]
    company.description = data["description"]
    company.save()
    return True


def update_company_image(data):
    company = dm.Company.objects.get(name=data["name"])
    company.img = data["img"]
    company.save()


def update_advice_rating(data):
    advice_rating = dm.AdviceRating.objects.get(user__user__username=data["username"], advice_id=data["id"])
    advice_rating.rating = data["rating"]
    advice_rating.save()


def update_article_rating(data):
    article_rating = dm.ArticleRating.objects.get(user__user__username=data["username"], article_id=data["id"])
    article_rating.rating = data["rating"]
    article_rating.save()


def update_article(data):
    if not dm.Article.objects.filter(author=data["username"], name=data["name_old"]).exists():
        return False
    article = dm.Article.objects.get(author=data["username"], name=data["name_old"])
    article.name = data["name"]
    article.language = data["language"]
    article.type_id = data["type"]
    article.img = data["img"]
    article.save()
    return True


def update_disaster(data):
    if not dm.Disaster.objects.filter(pk=data["id"]).exists():
        return False
    disaster = dm.Disaster.objects.get(pk=data["id"])
    disaster.intensity = data["intensity"]
    disaster.term = data["term"]
    disaster.readiness_degree = data["readiness"]
    disaster.type_id = data["type"]
    disaster.about = data["about"]
    disaster.about_clean = ""
    disaster.save()
    return True


def update_audience(data):
    if not dm.TargetAudience.objects.filter(pk=data["id"]).exists():
        return False
    audience = dm.TargetAudience.objects.get(pk=data["id"])
    audience.type_id = data["type"]
    audience.size = data["size"]
    audience.age_group = data["age_left"] + '-' + data["age_right"]
    audience.features = data["features"]
    audience.features_clean = ""
    audience.save()
    return True


def update_telegram_user(user, language):
    user = dm.TelegramUser.objects.get(user=user)
    user.language = language
    user.save()


def update_audience_features(id_audience, text):
    audience = dm.TargetAudience.objects.get(pk=id_audience)
    audience.features_clean = text
    audience.save()


def update_disaster_about(id_disaster, text):
    disaster = dm.Disaster.objects.get(pk=id_disaster)
    disaster.about_clean = text
    disaster.save()


def delete_companies_id(id_company):
    if dm.Company.objects.filter(pk=id_company).exists():
        dm.Company.objects.filter(pk=id_company).delete()
        return True
    return False


def delete_workplace_username_company_position(data):
    if dm.Workplace.objects.filter(user__user__username=data["username"],
                                   company__name=data["name"],
                                   position=data["position"]).exists():
        dm.Workplace.objects.filter(user__user__username=data["username"],
                                    company__name=data["name"],
                                    position=data["position"]).delete()
        return True
    return False


def delete_article_id(id_article):
    if dm.Article.objects.filter(pk=id_article).exists():
        dm.Article.objects.filter(pk=id_article).delete()
        return True
    return False


def delete_disaster_id(id_disaster):
    if dm.Disaster.objects.filter(pk=id_disaster).exists():
        dm.Disaster.objects.filter(pk=id_disaster).delete()
        return True
    return False


def delete_audience_id(id_audience):
    if dm.TargetAudience.objects.filter(pk=id_audience).exists():
        dm.TargetAudience.objects.filter(pk=id_audience).delete()
        return True
    return False
