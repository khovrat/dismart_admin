from django.contrib import admin

from server_side.apps.shared_logic.loggers import class_status_logger


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'subscription', 'img_tag')
    change_list_template = 'smuggler/change_list.html'
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'user__email')


class UserReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'review', 'time')
    list_filter = ('user', )
    change_list_template = 'smuggler/change_list.html'
    search_fields = ('user__user__username', 'review')
    date_hierarchy = 'time'

    @class_status_logger
    def has_add_permission(self, request):
        return False

    @class_status_logger
    def has_change_permission(self, request, obj=None):
        return False


class UserQuestionAdmin(admin.ModelAdmin):
    list_display = ('user', 'type', 'question', 'time')
    list_filter = ('type', 'user')
    change_list_template = 'smuggler/change_list.html'
    search_fields = ('user__user__username', 'question')
    date_hierarchy = 'time'

    @class_status_logger
    def has_add_permission(self, request):
        return False

    @class_status_logger
    def has_change_permission(self, request, obj=None):
        return False


class DisasterTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'img_tag')
    change_list_template = 'smuggler/change_list.html'


class DisasterTypeTranslationAdmin(admin.ModelAdmin):
    list_display = ('type', 'language', 'name', 'content')
    list_filter = ('type', 'language')
    change_list_template = 'smuggler/change_list.html'
    search_fields = ('name', 'content')


class DisasterAdmin(admin.ModelAdmin):
    list_display = ('type', 'user', 'term', 'intensity', 'readiness_degree', 'about')
    list_filter = ('type', 'user', 'term', 'intensity', 'readiness_degree')
    change_list_template = 'smuggler/change_list.html'
    search_fields = ('about', )


class AdviceAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'img_tag')
    list_filter = ('type', )
    change_list_template = 'smuggler/change_list.html'


class AdviceTranslationAdmin(admin.ModelAdmin):
    list_display = ('advice', 'language', 'name', 'content')
    list_filter = ('advice', 'language')
    change_list_template = 'smuggler/change_list.html'
    search_fields = ('name', 'content')


class AdviceRatingAdmin(admin.ModelAdmin):
    list_display = ('advice', 'user', 'rating')
    list_filter = ('advice', 'user', 'rating')
    change_list_template = 'smuggler/change_list.html'


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'date', 'img_tag')
    list_filter = ('author', 'date')
    change_list_template = 'smuggler/change_list.html'
    search_fields = ('name', 'author')


class ArticleRatingAdmin(admin.ModelAdmin):
    list_display = ('article', 'user', 'rating')
    list_filter = ('article', 'user', 'rating')
    change_list_template = 'smuggler/change_list.html'


class MarketAdmin(admin.ModelAdmin):
    list_display = ('id', 'ticker', 'img_tag')
    change_list_template = 'smuggler/change_list.html'
    search_fields = ('ticker',)


class MarketTranslationAdmin(admin.ModelAdmin):
    list_display = ('market', 'language', 'name', 'description')
    list_filter = ('market', 'language')
    change_list_template = 'smuggler/change_list.html'
    search_fields = ('name', 'content')


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'market', 'location', 'size', 'revenue', 'website', 'description', 'img_tag')
    list_filter = ('market', 'size', 'revenue')
    change_list_template = 'smuggler/change_list.html'
    search_fields = ('name', 'location', 'website', 'description')


class WorkplaceAdmin(admin.ModelAdmin):
    list_display = ('user', 'company', 'position')
    list_filter = ('company', 'user__user__username', 'position')
    change_list_template = 'smuggler/change_list.html'


class TargetAudienceTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'img_tag')
    change_list_template = 'smuggler/change_list.html'


class TargetAudienceTypeTranslationAdmin(admin.ModelAdmin):
    list_display = ('type', 'language', 'name', 'content')
    list_filter = ('type', 'language')
    change_list_template = 'smuggler/change_list.html'
    search_fields = ('name', 'content')


class TargetAudienceAdmin(admin.ModelAdmin):
    list_display = ('type', 'company', 'age_group', 'size', 'features')
    list_filter = ('type', 'company', 'size')
    change_list_template = 'smuggler/change_list.html'
    search_fields = ('age_group', 'features')


class MarketForecastAdmin(admin.ModelAdmin):
    list_display = ('market', 'disaster', 'date', 'last_update')
    list_filter = ('market', 'disaster', 'date', 'last_update')
    change_list_template = 'smuggler/change_list.html'
    date_hierarchy = 'date'

    @class_status_logger
    def has_add_permission(self, request):
        return False

    @class_status_logger
    def has_change_permission(self, request, obj=None):
        return False


class CompanyForecastAdmin(admin.ModelAdmin):
    list_display = ('company', 'disaster', 'date', 'last_update')
    list_filter = ('company', 'disaster', 'date', 'last_update')
    change_list_template = 'smuggler/change_list.html'
    date_hierarchy = 'date'

    @class_status_logger
    def has_add_permission(self, request):
        return False

    @class_status_logger
    def has_change_permission(self, request, obj=None):
        return False


class CompanyStressTestAdmin(admin.ModelAdmin):
    list_display = ('company', 'disaster', 'date', 'last_update')
    list_filter = ('company', 'disaster', 'date', 'last_update')
    change_list_template = 'smuggler/change_list.html'
    date_hierarchy = 'date'

    @class_status_logger
    def has_add_permission(self, request):
        return False

    @class_status_logger
    def has_change_permission(self, request, obj=None):
        return False


class TargetAudienceBehaviourAdmin(admin.ModelAdmin):
    list_display = ('audience', 'disaster', 'date', 'last_update')
    list_filter = ('audience', 'disaster', 'date', 'last_update')
    change_list_template = 'smuggler/change_list.html'
    date_hierarchy = 'date'

    @class_status_logger
    def has_add_permission(self, request):
        return False

    @class_status_logger
    def has_change_permission(self, request, obj=None):
        return False
