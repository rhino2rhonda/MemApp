#from django import forms
#from features.models import TodoNote, Feature
#from django.core.exceptions import ObjectDoesNotExist
from notes.models import NoteRegistry
from django.core.exceptions import ObjectDoesNotExist
from features.forms import FeatureFormFactory

class CompositeNoteForm():
    
    def __init__(self, key_name):
        self.key_name = key_name
        self.error_message_prefix = "Composite FormGen Error : "
        self.generate_composite_form()
        
        
        
    def generate_composite_form(self):
        try:
            note = NoteRegistry.objects.get(key_name=self.key_name)
        except ObjectDoesNotExist:
            print self.error_message_prefix + "key_name", self.key_name, "does not exist in the database"
            return None
        self.forms = []
        self.note_properties = {}
        self.note_name = note.attrib_dict['note_name']
        print note.attrib_dict
        while note:
            if not note.attrib_dict:
                break
            for key in note.attrib_dict.keys():
                print key, note.attrib_dict[key]
                if key == 'note_name':
                    continue
                elif key == 'ordered_features':
                    for feature in note.attrib_dict['ordered_features']['feature_template']:
                        print "DEEBUB : ", type(feature), feature
                        key_name = feature['key_name']
                        try:
                            feature_form = FeatureFormFactory(key_name).feature_form
                        except Exception as e:
                            print self.error_message_prefix + "Could not generate feature form for form with keyname "\
                            + key_name + ". Skipping this feature."
                            print e
                            continue
                        self.forms.append(feature_form)
                        self.forms.sort(key=lambda x: x['default_ui_rank'])
                else:
                    try:
                        self.note_properties[key]
                    except KeyError:
                        self.note_properties[key] = note.attrib_dict[key]
            note = note.parent
            
        
'''
class Feature_Customization_Base():
    
    def getForm(self):
        return None

class FeatureFormFactory:
    
    customized_features = {"some_feature": "some_class"}
    
    def getForm(self, feature_key_name, xmlstuff=None):
        customization_class = None
        
        try:#Getting Model from feature key name
            feature_model = Feature.objects.get(feature_key_name=feature_key_name)
        except ObjectDoesNotExist as odne:
            print "Error:ObjectDoesNotExist. Returning None\n", odne
            return None
        
        try:#Checking if Customiztion Class exists for this model
            customization_class = self.customized_features[feature_key_name]
        except KeyError:
            pass
        
        if customization_class == None:
            return forms.modelform_factory(feature_model, fields="__all__")
        
        formgen = customization_class()
        return formgen.getForm()
        

    
        
    

class TodoForm(forms.ModelForm):
    title = forms.CharField(max_length=30)
    content = forms.CharField(max_length=30)
    category = forms.CharField(max_length=30)
    class Meta:
        model = TodoNote
        fields = []
        
'''