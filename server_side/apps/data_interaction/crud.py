from django.contrib.auth.models import User

import server_side.apps.data_interaction.models as dm


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


def create_profile(data):
    user = User(username=data['username'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                email=data['email']
                )
    user.set_password(data['password'])
    user.save()
    if 'img' in data:
        user.profile.img = data['img']
    if 'subscription' in data:
        user.profile.subscription = data['subscription']
    user.save()
    return read_profile_by_username(data['username'])
