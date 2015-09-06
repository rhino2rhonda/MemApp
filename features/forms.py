from features.models import FeatureRegistry
from django.core.exceptions import ObjectDoesNotExist
from django import forms
from django.apps import apps

class FeatureFormFactory:
    
    def __init__(self, key_name, customization_class=None):
        self.key_name = key_name
        self.customization_class = customization_class
        self.feature_form = {}
        self.create_feature_form()
        
    def create_feature_form(self):
        
        feature = FeatureRegistry.objects.get(key_name=self.key_name)
        self.feature_form['name'] = feature.key_name
        self.feature_form['default_ui_rank'] = feature.default_ui_rank
        if self.customization_class:
            feature_form = eval(self.customization_class)().form
        else:
            feature_form = forms.modelform_factory(apps.get_model('features', feature.model_class), fields="__all__")
        self.feature_form['form'] = feature_form