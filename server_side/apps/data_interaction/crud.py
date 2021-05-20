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
