from django.contrib import admin
from features.models import FeaturesMetaXML, FeatureRegistry
# Register your models here.
admin.site.register(FeaturesMetaXML)
admin.site.register(FeatureRegistry)
