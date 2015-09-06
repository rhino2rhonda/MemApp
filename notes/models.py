from django.db import models
from DjangoThirdParty.picklefield.fields import PickledObjectField
#from features import models as fmodels
#from django.db.models.loading import get_model
#from notes.forms import FeatureFormFactory
#from features.models import Feature

#import xml.etree.ElementTree as ET
# Create your models here.

#Table NotesMetaXML stores the raw xml from an xml file.
#Stores History of previous (valid) versions of the xml file
#Update it when the xml file is modified.
class NotesMetaXML(models.Model):
    xml = models.TextField()
    timestamp = models.DateField(auto_now_add=True)
    
class NotesTemplateXML(models.Model):
    xml = models.TextField()
    timestamp = models.DateField(auto_now_add=True)

#Table NoteRegistry - stores noteid,notekeyname,metadata mapping.
#It is polulated/updated from an xml file.
#Update it every time you modify the corresponding xml file.
class NoteRegistry(models.Model):
    nid = models.IntegerField(primary_key=True) 
    key_name = models.CharField(max_length=200)
    parent = models.ForeignKey("self", null=True)
    #other meta data specific to a note comes here
    attrib_dict = PickledObjectField()
    last_updated = models.DateTimeField()

    def  __str__(self):
        return "_".join(["Note", self.key_name, str(self.nid)])
#Table Note - holds the individual note instances created along with the note type
#While retrieving a note, find out the associated features and poll their values
class Note(models.Model):
    type = models.ForeignKey(NoteRegistry)
    
'''
class Note:    
    
    def __init__(self, note_short_key_name):
        try:
            #test val and type of args
            self.short_key_name = note_short_key_name
            
            tree = ET.parse('features/todo.xml')
            template_list = tree.getroot()
            note_template = template_list.find('note_template[@short_key_name="' + self.short_key_name + '"]')
            if not note_template:
                5/0
                
            #NOTE_NAME
            try:
                self.note_name = note_template.find('note_name').text
            except:
                self.note_name = None
                
            #NOTE_DESCRIPTION
            try:
                self.note_description = note_template.find('note_description').text
            except:
                self.note_description = None
                
            #NOTE_CLASS
            try:
                self.note_class = note_template.find('note_class').text
            except:
                self.note_class = None
             
            #FEATURE_CATEGORY
            try:
                self.note_category = note_template.find('note_category').Text
            except:
                self.note_category = None
                
            #FEATURE_LIST
            self.feature_list = []
            flist_xml = note_template.find('ordered_features')
            for feature_xml in flist_xml:
                self.feature_list.append(feature_xml.text)
            
        except:
            raise(Exception("XML Missing or Improperly Configured (xml file name)"))
    
    def getOrderedFeatuers(self):
        pass #handle xml shizz
    
    
    def getCompositeForm(self):
        self.form_model = get_model(self.note_class)
        self.features = self.getOrderedFeatuers()
        xmlstuff=None
        form_list =[]
        for feature in self.features:
            feature_form = Feature.objects.get(feature_key_name=feature).getForm(xmlstuff)
            form_list.append(feature_form)
        return form_list
    
    def __str__(self):
        return self.feature_name

class BaseNote(models.Model):
       
    creation_time = models.OneToOneField(fmodels.Feature_Creation_Time)
    last_modification_time = models.OneToOneField(fmodels.Feature_Last_Modification_Time)
    category = models.ForeignKey(fmodels.Feature_Category)
    tags = models.ManyToManyField(fmodels.Feature_Tag)    
    
class TodoNote(BaseNote):
    
    title = models.OneToOneField(fmodels.Feature_Title)
    content = models.OneToOneField(fmodels.Feature_Content)
    target_completion_date_initial = models.OneToOneField(fmodels.Feature_Target_Completion_Date_Initial, null=True)
    target_completion_date_current = models.OneToOneField(fmodels.Feature_Target_Completion_Date_Current, null=True)
    deadline_initial = models.OneToOneField(fmodels.Feature_Deadline_Initial, null=True)
    deadline_current = models.OneToOneField(fmodels.Feature_Deadline_Current, null=True)
    notification = models.ForeignKey(fmodels.Feature_Notification, null=True)
'''
