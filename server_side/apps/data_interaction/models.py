from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from decouple import config

from server_side.apps.shared_logic.loggers import class_status_logger
from server_side.settings import LANGUAGE_CODE, LANGUAGES
from server_side.apps.data_interaction.constants import SUBSCRIPTION_TYPE, QUESTION_TYPE


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_("user"))
    subscription = models.CharField(
        max_length=100,
        choices=SUBSCRIPTION_TYPE,
        default="DEFAULT",
        verbose_name=_("subscription"),
        help_text=_("subscription_help"),
    )
    img = models.URLField(
        default=config("BASE_URL"),
        null=False,
        verbose_name=_("img_user"),
        help_text=_("help_img_user"),
    )

    @class_status_logger
    def img_tag(self):
        return mark_safe('<img src="%s" width="150" height="150" />' % self.img)

    @class_status_logger
    def __str__(self):
        return _("user") + ": " + str(self.user.id) + "; "

    class Meta:
        verbose_name = _("profile")
        verbose_name_plural = _("profiles")


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, **kwargs):
    if kwargs["created"]:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class UserReview(models.Model):
    user = models.ForeignKey(
        Profile, on_delete=models.CASCADE, null=False, verbose_name=_("profile")
    )
    review = models.TextField(verbose_name=_("review"))
    time = models.DateTimeField(auto_now_add=True, blank=True, verbose_name=_("time"))

    class Meta:
        verbose_name = _("user_review")
        verbose_name_plural = _("user_reviews")


class UserQuestion(models.Model):
    user = models.ForeignKey(
        Profile, on_delete=models.CASCADE, null=False, verbose_name=_("profile")
    )
    question = models.TextField(verbose_name=_("question"))
    time = models.DateTimeField(auto_now_add=True, blank=True, verbose_name=_("time"))
    type = models.CharField(
        max_length=100,
        choices=QUESTION_TYPE,
        default="DEFAULT",
        verbose_name=_("question_type"),
        help_text=_("question_type_help"),
    )

    class Meta:
        verbose_name = _("user_question")
        verbose_name_plural = _("user_questions")


class DisasterType(models.Model):
    img = models.URLField(
        default=config("BASE_URL"),
        null=False,
        verbose_name=_("img"),
        help_text=_("help_img"),
    )

    @class_status_logger
    def img_tag(self):
        return mark_safe('<img src="%s" width="150" height="150" />' % self.img)

    img_tag.short_description = _("img")

    @class_status_logger
    def __str__(self):
        return _("disaster_type") + ": " + str(self.id) + "; "

    class Meta:
        verbose_name = _("disaster_type")
        verbose_name_plural = _("disaster_types")


class DisasterTypeTranslation(models.Model):
    type = models.ForeignKey(
        DisasterType,
        on_delete=models.CASCADE,
        null=False,
        verbose_name=_("disaster_type"),
    )
    language = models.CharField(
        max_length=20,
        choices=LANGUAGES,
        default=LANGUAGE_CODE,
        null=False,
        verbose_name=_("language"),
    )
    name = models.CharField(max_length=200, null=False, verbose_name=_("name"))
    content = models.TextField(verbose_name=_("content"), help_text=_("content_help"))

    @class_status_logger
    def __str__(self):
        result = _("disaster_type") + ": " + str(self.type.id) + "; "
        return result

    class Meta:
        verbose_name = _("disaster_type_translation")
        verbose_name_plural = _("disaster_types_translation")
        unique_together = ("type", "language")


class Disaster(models.Model):
    type = models.ForeignKey(
        DisasterType,
        on_delete=models.CASCADE,
        null=False,
        verbose_name=_("disaster_type"),
    )
    user = models.ForeignKey(
        Profile, on_delete=models.CASCADE, null=False, verbose_name=_("profile")
    )
    term = models.IntegerField(
        default=1, null=False, verbose_name=_("term"), help_text=_("term_help")
    )
    intensity = models.IntegerField(
        default=1,
        null=False,
        verbose_name=_("intensity"),
        help_text=_("intensity_help"),
    )
    readiness_degree = models.IntegerField(
        default=1,
        null=False,
        verbose_name=_("readiness_degree"),
        help_text=_("readiness_degree_help"),
    )
    about = models.TextField(verbose_name=_("about"), help_text=_("about_help"))

    @class_status_logger
    def __str__(self):
        result = _("disaster") + ": " + str(self.type.id) + "; "
        return result

    class Meta:
        verbose_name = _("disaster")
        verbose_name_plural = _("disasters")


class Advice(models.Model):
    img = models.URLField(
        default=config("BASE_URL"),
        null=False,
        verbose_name=_("img"),
        help_text=_("help_img"),
    )
    type = models.ForeignKey(
        DisasterType,
        on_delete=models.CASCADE,
        null=False,
        verbose_name=_("advice_type"),
        help_text=_("advice_type_help"),
    )

    @class_status_logger
    def img_tag(self):
        return mark_safe('<img src="%s" width="150" height="150" />' % self.img)

    img_tag.short_description = _("img")

    @class_status_logger
    def __str__(self):
        return _("advice") + ": " + str(self.id) + "; "

    class Meta:
        verbose_name = _("advice")
        verbose_name_plural = _("advices")


class AdviceTranslation(models.Model):
    advice = models.ForeignKey(
        Advice, on_delete=models.CASCADE, null=False, verbose_name=_("advice")
    )
    language = models.CharField(
        max_length=20,
        choices=LANGUAGES,
        default=LANGUAGE_CODE,
        null=False,
        verbose_name=_("language"),
    )
    name = models.CharField(max_length=200, null=False, verbose_name=_("name"))
    content = models.TextField(verbose_name=_("content"), help_text=_("content_help"))

    @class_status_logger
    def __str__(self):
        result = _("advice") + ": " + str(self.advice.id) + "; "
        return result

    class Meta:
        verbose_name = _("advice_translation")
        verbose_name_plural = _("advices_translation")
        unique_together = ("advice", "language")


class AdviceRating(models.Model):
    advice = models.ForeignKey(
        Advice, on_delete=models.CASCADE, null=False, verbose_name=_("advice")
    )
    user = models.ForeignKey(
        Profile, on_delete=models.CASCADE, null=False, verbose_name=_("profile")
    )
    rating = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        null=False,
        verbose_name=_("rating"),
        help_text=_("rating"),
    )
    time = models.DateTimeField(auto_now_add=True, blank=True, verbose_name=_("time"))

    @class_status_logger
    def __str__(self):
        return _("advice") + ": " + str(self.advice.id) + "; "

    class Meta:
        verbose_name = _("advice_rating")
        verbose_name_plural = _("advices_rating")
        unique_together = ("advice", "user")


class Article(models.Model):
    img = models.URLField(
        default=config("BASE_URL"),
        null=False,
        verbose_name=_("img"),
        help_text=_("help_img"),
    )
    type = models.ForeignKey(
        DisasterType,
        on_delete=models.CASCADE,
        null=False,
        verbose_name=_("article_type"),
        help_text=_("article_type_help"),
    )
    language = models.CharField(
        max_length=20,
        choices=LANGUAGES,
        default=LANGUAGE_CODE,
        null=False,
        verbose_name=_("language"),
    )
    name = models.CharField(max_length=200, null=False, verbose_name=_("name"))
    author = models.CharField(max_length=200, null=False, verbose_name=_("author"))
    date = models.DateField(auto_now_add=True, blank=True, verbose_name=_("date"))
    text = models.BinaryField(verbose_name=_("article_text"))

    @class_status_logger
    def img_tag(self):
        return mark_safe('<img src="%s" width="150" height="150" />' % self.img)

    img_tag.short_description = _("img")

    @class_status_logger
    def __str__(self):
        return _("advice") + ": " + str(self.id) + "; "

    class Meta:
        verbose_name = _("advice")
        verbose_name_plural = _("advices")


class ArticleRating(models.Model):
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, null=False, verbose_name=_("article")
    )
    user = models.ForeignKey(
        Profile, on_delete=models.CASCADE, null=False, verbose_name=_("profile")
    )
    rating = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        null=False,
        verbose_name=_("rating"),
        help_text=_("rating"),
    )
    time = models.DateTimeField(auto_now_add=True, blank=True, verbose_name=_("time"))

    @class_status_logger
    def __str__(self):
        return _("article") + ": " + str(self.article.id) + "; "

    class Meta:
        verbose_name = _("article_rating")
        verbose_name_plural = _("article_rating")
        unique_together = ("article", "user")


class Market(models.Model):
    img = models.URLField(
        default=config("BASE_URL"),
        null=False,
        verbose_name=_("img"),
        help_text=_("help_img"),
    )

    @class_status_logger
    def img_tag(self):
        return mark_safe('<img src="%s" width="150" height="150" />' % self.img)

    img_tag.short_description = _("img")

    @class_status_logger
    def __str__(self):
        return _("market") + ": " + str(self.id) + "; "

    class Meta:
        verbose_name = _("market")
        verbose_name_plural = _("markets")


class MarketTranslation(models.Model):
    market = models.ForeignKey(
        Market, on_delete=models.CASCADE, null=False, verbose_name=_("market")
    )
    language = models.CharField(
        max_length=20,
        choices=LANGUAGES,
        default=LANGUAGE_CODE,
        null=False,
        verbose_name=_("language"),
    )
    name = models.CharField(max_length=200, null=False, verbose_name=_("name"))
    description = models.TextField(
        verbose_name=_("description"), help_text=_("description_help")
    )

    @class_status_logger
    def __str__(self):
        result = _("advice") + ": " + str(self.market.id) + "; "
        return result

    class Meta:
        verbose_name = _("market_translation")
        verbose_name_plural = _("markets_translation")
        unique_together = ("market", "language")


class Company(models.Model):
    market = models.ForeignKey(
        Market, on_delete=models.CASCADE, null=False, verbose_name=_("market")
    )
    name = models.CharField(max_length=200, null=False, verbose_name=_("name"))
    location = models.CharField(max_length=200, null=False, verbose_name=_("location"))
    size = models.IntegerField(default=1, null=False, verbose_name=_("size"))
    revenue = models.FloatField(default=1.0, null=True, verbose_name=_("size"))
    website = models.URLField(
        null=True, verbose_name=_("website"), help_text=_("help_website")
    )
    img = models.URLField(
        default=config("BASE_URL"),
        null=False,
        verbose_name=_("img_user"),
        help_text=_("help_img_user"),
    )
    description = models.TextField(
        verbose_name=_("description"), help_text=_("description_help")
    )

    @class_status_logger
    def img_tag(self):
        return mark_safe('<img src="%s" width="150" height="150" />' % self.img)

    img_tag.short_description = _("img")

    @class_status_logger
    def __str__(self):
        result = _("market") + ": " + str(self.market.id) + "; "
        return result

    class Meta:
        verbose_name = _("company")
        verbose_name_plural = _("companies")


class Workplace(models.Model):
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, null=False, verbose_name=_("company")
    )
    user = models.ForeignKey(
        Profile, on_delete=models.CASCADE, null=False, verbose_name=_("profile")
    )
    position = models.CharField(max_length=200, null=False, verbose_name=_("position"))

    @class_status_logger
    def __str__(self):
        result = (
            _("company")
            + ": "
            + str(self.company.id)
            + "; "
            + _("user")
            + ": "
            + self.user.user.username
            + "; "
        )
        return result

    class Meta:
        verbose_name = _("workplace")
        verbose_name_plural = _("workplaces")


class TargetAudienceType(models.Model):
    img = models.URLField(
        default=config("BASE_URL"),
        null=False,
        verbose_name=_("img"),
        help_text=_("help_img"),
    )

    @class_status_logger
    def img_tag(self):
        return mark_safe('<img src="%s" width="150" height="150" />' % self.img)

    img_tag.short_description = _("img")

    @class_status_logger
    def __str__(self):
        return _("target_audience_type") + ": " + str(self.id) + "; "

    class Meta:
        verbose_name = _("target_audience_type")
        verbose_name_plural = _("target_audience_types")


class TargetAudienceTypeTranslation(models.Model):
    type = models.ForeignKey(
        TargetAudienceType,
        on_delete=models.CASCADE,
        null=False,
        verbose_name=_("target_audience_type"),
    )
    language = models.CharField(
        max_length=20,
        choices=LANGUAGES,
        default=LANGUAGE_CODE,
        null=False,
        verbose_name=_("language"),
    )
    name = models.CharField(max_length=200, null=False, verbose_name=_("name"))
    content = models.TextField(verbose_name=_("content"), help_text=_("content_help"))

    @class_status_logger
    def __str__(self):
        result = _("target_audience") + ": " + str(self.type.id) + "; "
        return result

    class Meta:
        verbose_name = _("target_audience_type_translation")
        verbose_name_plural = _("target_audience_types_translation")
        unique_together = ("type", "language")


class TargetAudience(models.Model):
    type = models.ForeignKey(
        TargetAudienceType,
        on_delete=models.CASCADE,
        null=False,
        verbose_name=_("target_audience_type"),
    )
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, null=False, verbose_name=_("company")
    )
    age_group = models.CharField(
        max_length=200, null=False, verbose_name=_("age_group")
    )
    size = models.IntegerField(default=1, null=False, verbose_name=_("size"))
    features = models.TextField(
        verbose_name=_("features"), help_text=_("features_help")
    )

    @class_status_logger
    def __str__(self):
        return (
            _("company")
            + ": "
            + str(self.company.id)
            + "; "
            + _("target_audience_type")
            + ": "
            + str(self.type.id)
            + "; "
        )

    class Meta:
        verbose_name = _("target_audience")
        verbose_name_plural = _("target_audiences")


class MarketForecast(models.Model):
    market = models.ForeignKey(
        Market, on_delete=models.CASCADE, null=False, verbose_name=_("market")
    )
    disaster = models.ForeignKey(
        Disaster, on_delete=models.CASCADE, null=False, verbose_name=_("disaster")
    )
    forecast = models.BinaryField(verbose_name=_("forecast"))
    date = models.DateField(auto_now_add=True, blank=True, verbose_name=_("date"))
    last_update = models.DateTimeField(
        auto_now_add=True, blank=True, verbose_name=_("last_update")
    )

    @class_status_logger
    def __str__(self):
        return (
            _("market")
            + ": "
            + str(self.market.id)
            + "; "
            + _("disaster")
            + ": "
            + str(self.disaster.id)
            + "; "
        )

    class Meta:
        verbose_name = _("market_forecast")
        verbose_name_plural = _("market_forecasts")


class CompanyForecast(models.Model):
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, null=False, verbose_name=_("company")
    )
    disaster = models.ForeignKey(
        Disaster, on_delete=models.CASCADE, null=False, verbose_name=_("disaster")
    )
    forecast = models.BinaryField(verbose_name=_("forecast"))
    date = models.DateField(auto_now_add=True, blank=True, verbose_name=_("date"))
    last_update = models.DateTimeField(
        auto_now_add=True, blank=True, verbose_name=_("last_update")
    )

    @class_status_logger
    def __str__(self):
        return (
            _("company")
            + ": "
            + str(self.company.id)
            + "; "
            + _("disaster")
            + ": "
            + str(self.disaster.id)
            + "; "
        )

    class Meta:
        verbose_name = _("company_forecast")
        verbose_name_plural = _("company_forecasts")


class CompanyStressTest(models.Model):
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, null=False, verbose_name=_("company")
    )
    disaster = models.ForeignKey(
        Disaster, on_delete=models.CASCADE, null=False, verbose_name=_("disaster")
    )
    test_result = models.BinaryField(verbose_name=_("test_result"))
    date = models.DateField(auto_now_add=True, blank=True, verbose_name=_("date"))
    last_update = models.DateTimeField(
        auto_now_add=True, blank=True, verbose_name=_("last_update")
    )

    @class_status_logger
    def __str__(self):
        return (
            _("company")
            + ": "
            + str(self.company.id)
            + "; "
            + _("disaster")
            + ": "
            + str(self.disaster.id)
            + "; "
        )

    class Meta:
        verbose_name = _("company_stress_test")
        verbose_name_plural = _("company_stress_tests")


class TargetAudienceBehaviour(models.Model):
    audience = models.ForeignKey(
        TargetAudience,
        on_delete=models.CASCADE,
        null=False,
        verbose_name=_("target_audience"),
    )
    disaster = models.ForeignKey(
        Disaster, on_delete=models.CASCADE, null=False, verbose_name=_("disaster")
    )
    forecast = models.BinaryField(verbose_name=_("forecast"))
    date = models.DateField(auto_now_add=True, blank=True, verbose_name=_("date"))
    last_update = models.DateTimeField(
        auto_now_add=True, blank=True, verbose_name=_("last_update")
    )

    @class_status_logger
    def __str__(self):
        return (
            _("target_audience")
            + ": "
            + str(self.audience.id)
            + "; "
            + _("disaster")
            + ": "
            + str(self.disaster.id)
            + "; "
        )

    class Meta:
        verbose_name = _("target_audience_behaviour")
        verbose_name_plural = _("target_audiences_behaviours")
