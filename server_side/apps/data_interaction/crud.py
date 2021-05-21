from django.contrib.auth.models import User

import server_side.apps.data_interaction.models as dm


def create_profile(data):
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


def create_review(data):
    profile = read_profile_by_username(data["username"])
    review = dm.UserReview(user_id=profile.id, review=data["review"])
    review.save()


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
    return dm.Company.objects.filter(workplace__user__user_id=user.user_id)


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
    company.revenue = data["revenue"]
    company.location = data["location"]
    company.description = data["description"]
    company.save()
    return True


def update_company_image(data):
    company = dm.Company.objects.get(name=data["name"])
    company.img = data["img"]
    company.save()


def delete_companies_id(id_company):
    if dm.Company.objects.filter(pk=id_company).exists():
        dm.Company.objects.filter(pk=id_company).delete()
        return True
    return False
