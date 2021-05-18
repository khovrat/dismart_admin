from rest_framework import serializers
from django.contrib.auth.models import User
from server_side.apps.data_interaction import models as dm


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['is_superuser', 'username', 'first_name', 'last_name', 'email', 'date_joined']


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)

    class Meta:
        model = dm.Profile
        fields = '__all__'


class UserReviewSerializer(serializers.ModelSerializer):
    user = ProfileSerializer(required=False)

    class Meta:
        model = dm.UserReview
        fields = '__all__'


class UserQuestionSerializer(serializers.ModelSerializer):
    user = ProfileSerializer(required=False)

    class Meta:
        model = dm.UserQuestion
        fields = '__all__'


class DisasterTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = dm.DisasterType
        fields = '__all__'


class DisasterTypeTranslationSerializer(serializers.ModelSerializer):
    type = DisasterTypeSerializer(required=False)

    class Meta:
        model = dm.DisasterTypeTranslation
        fields = '__all__'


class DisasterSerializer(serializers.ModelSerializer):
    user = ProfileSerializer(required=False)
    type = DisasterTypeSerializer(required=False)

    class Meta:
        model = dm.Disaster
        fields = '__all__'


class AdviceSerializer(serializers.ModelSerializer):
    type = DisasterTypeSerializer(required=False)

    class Meta:
        model = dm.Advice
        fields = '__all__'


class AdviceTranslationSerializer(serializers.ModelSerializer):
    advice = AdviceSerializer(required=False)

    class Meta:
        model = dm.AdviceTranslation
        fields = '__all__'


class AdviceRatingSerializer(serializers.ModelSerializer):
    advice = AdviceSerializer(required=False)
    user = ProfileSerializer(required=False)

    class Meta:
        model = dm.AdviceRating
        fields = '__all__'


class ArticleSerializer(serializers.ModelSerializer):
    type = DisasterTypeSerializer(required=False)

    class Meta:
        model = dm.Article
        fields = '__all__'


class ArticleRatingSerializer(serializers.ModelSerializer):
    article = ArticleSerializer(required=False)
    user = ProfileSerializer(required=False)

    class Meta:
        model = dm.ArticleRating
        fields = '__all__'


class MarketSerializer(serializers.ModelSerializer):
    class Meta:
        model = dm.Market
        fields = '__all__'


class MarketTranslationSerializer(serializers.ModelSerializer):
    market = MarketSerializer(required=False)

    class Meta:
        model = dm.MarketTranslation
        fields = '__all__'


class CompanySerializer(serializers.ModelSerializer):
    market = MarketSerializer(required=False)

    class Meta:
        model = dm.Company
        fields = '__all__'


class WorkplaceSerializer(serializers.ModelSerializer):
    company = CompanySerializer(required=False)
    user = ProfileSerializer(required=False)

    class Meta:
        model = dm.Workplace
        fields = '__all__'


class TargetAudienceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = dm.TargetAudienceType
        fields = '__all__'


class TargetAudienceTypeTranslationSerializer(serializers.ModelSerializer):
    type = TargetAudienceTypeSerializer(required=False)

    class Meta:
        model = dm.TargetAudienceTypeTranslation
        fields = '__all__'


class TargetAudienceSerializer(serializers.ModelSerializer):
    company = CompanySerializer(required=False)
    type = TargetAudienceTypeSerializer(required=False)

    class Meta:
        model = dm.TargetAudience
        fields = '__all__'


class MarketForecastSerializer(serializers.ModelSerializer):
    market = MarketSerializer(required=False)
    disaster = DisasterTypeSerializer(required=False)

    class Meta:
        model = dm.MarketForecast
        fields = '__all__'


class CompanyForecastSerializer(serializers.ModelSerializer):
    company = MarketSerializer(required=False)
    disaster = DisasterTypeSerializer(required=False)

    class Meta:
        model = dm.CompanyForecast
        fields = '__all__'


class CompanyStressTestSerializer(serializers.ModelSerializer):
    company = MarketSerializer(required=False)
    disaster = DisasterTypeSerializer(required=False)

    class Meta:
        model = dm.CompanyStressTest
        fields = '__all__'


class TargetAudienceBehaviourSerializer(serializers.ModelSerializer):
    audience = TargetAudienceSerializer(required=False)
    disaster = DisasterTypeSerializer(required=False)

    class Meta:
        model = dm.TargetAudienceBehaviour
        fields = '__all__'
