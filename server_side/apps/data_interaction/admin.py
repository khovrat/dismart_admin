from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _
from server_side.apps.data_interaction import models as dm
from server_side.apps.data_interaction import admin_models as adm


admin.site.site_header = 'DISMART'
admin.site.index_title = _("Dismart_Admin_Panel")
admin.site.site_title = _("Dismart_Management")

admin.site.unregister(Group)
admin.site.register(dm.Profile, adm.ProfileAdmin)
admin.site.register(dm.UserReview, adm.UserReviewAdmin)
admin.site.register(dm.UserQuestion, adm.UserQuestionAdmin)

admin.site.register(dm.Advice, adm.AdviceAdmin)
admin.site.register(dm.AdviceTranslation, adm.AdviceTranslationAdmin)
admin.site.register(dm.AdviceRating, adm.AdviceRatingAdmin)

admin.site.register(dm.Article, adm.ArticleAdmin)
admin.site.register(dm.ArticleRating, adm.ArticleRatingAdmin)

admin.site.register(dm.Market, adm.MarketAdmin)
admin.site.register(dm.MarketTranslation, adm.MarketTranslationAdmin)

admin.site.register(dm.TargetAudience, adm.TargetAudienceAdmin)
admin.site.register(dm.TargetAudienceType, adm.TargetAudienceTypeAdmin)
admin.site.register(dm.TargetAudienceTypeTranslation, adm.TargetAudienceTypeTranslationAdmin)

admin.site.register(dm.Company, adm.CompanyAdmin)
admin.site.register(dm.Workplace, adm.WorkplaceAdmin)

admin.site.register(dm.Disaster, adm.DisasterAdmin)
admin.site.register(dm.DisasterType, adm.DisasterTypeAdmin)
admin.site.register(dm.DisasterTypeTranslation, adm.DisasterTypeTranslationAdmin)

admin.site.register(dm.MarketForecast, adm.MarketForecastAdmin)
admin.site.register(dm.CompanyForecast, adm.CompanyForecastAdmin)
admin.site.register(dm.CompanyStressTest, adm.CompanyStressTestAdmin)
admin.site.register(dm.TargetAudienceBehaviour, adm.TargetAudienceBehaviourAdmin)
