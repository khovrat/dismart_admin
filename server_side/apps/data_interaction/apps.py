from django.apps import AppConfig
from suit.apps import DjangoSuitConfig
from suit.menu import ParentItem, ChildItem
from django.utils.translation import ugettext_lazy as _


class DataInteractionConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "server_side.apps.data_interaction"
    verbose_name = _("Tables")
