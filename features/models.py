from django.db import models
from notes.models import Note

# Create your models here.

#Table FeaturesMetaXML stores the raw xml from an xml file.
#Stores History of previous (valid) versions of the xml file
#Update it when the xml file is modified.
class FeaturesMetaXML(models.Model):
    xml = models.TextField()
    timestamp = models.DateField(auto_now_add=True)
    
class FeatureRegistry(models.Model):
    fid = models.IntegerField(primary_key=True) 
    key_name = models.CharField(max_length=200)
    default_ui_rank = models.IntegerField(unique=True)
    #verbose_name, description
    last_updated = models.DateTimeField()
    model_class = models.CharField(max_length=30)
    
    class Meta:
        verbose_name_plural = "feature registry"
        
    def  __str__(self):
        return "_".join(["Feature", self.key_name, str(self.fid)])


'''
#Hold Name of all features used and related metadata
class FeatureTemp(models.Model):
    feature_name = models.CharField(max_length=30)
    feature_key_name = models.CharField(max_length=30, unique=True)
    feature_description = models.CharField(max_length=100)
    feature_render_permission = models.BooleanField()
    feature_class = models.CharField(max_length=30, unique=True)
    xml_params = models.CharField(max_length=30)
    
    def __init__(self, *args, **kwargs):
        super(self.__class__, self, args, kwargs)
        #UPDATE XML
        self.xml_params = "read_some_file"
        "save instance"
        "add attributes to class"
        
    def get_form(self, xmlstuff=None):
        customization_class = "self.customization_class"
        
        if customization_class == None:
            return forms.modelform_factory(self.__class__, fields="__all__")
        
        formgen = customization_class()
        return formgen.getForm()
    
    def __str__(self):
        return self.feature_name

#Note1: that feature tables are of the following types:
#1. Ones that hold OneToOne Records, eg, Feature_Title
#2. Ones that hold Foreign Keys, eg, Feature_Category
#Note2: Some features, like Feature_Category, are exceptions, but for all features
#including these ones, the only relevant info is the way they are rendered
'''

class FeatureBase(models.Model):
    note = models.ForeignKey(Note)
    
    def __str__(self):
        print self.__class__.__name__
    
class FeatureTitle(FeatureBase):
    value = models.CharField(max_length=200)
    
class FeatureContent(FeatureBase):
    value = models.CharField(max_length=500, verbose_name='content')

class FeatureTargetCompletionTime(FeatureBase):
    value = models.DateTimeField(verbose_name='target completion time')

'''
class Feature_Category(Feature_Base):
    value = models.CharField(max_length=30, verbose_name='category')
    child_categories = models.ManyToManyField("self", symmetrical=False)

class Feature_Tag(Feature_Base):
    value = models.CharField(max_length=30, verbose_name='tag')

class Feature_Target_Completion_Date_Initial(Feature_Base):
    value = models.DateField(verbose_name='target completion date', editable=False)
    
class Feature_Target_Completion_Date_Current(Feature_Base):
    value = models.DateField(verbose_name='target completion date')
    
class Feature_Deadline_Initial(Feature_Base):
    value = models.DateField(verbose_name='deadline', editable=False)
    
class Feature_Deadline_Current(Feature_Base):
    value = models.DateField(verbose_name='deadline')

class Feature_Notification(Feature_Base):
    NOTIFICATION_CHOICES = (
        ('SMS', 'SMS Notification'),
        ('EM', 'Email Notification'),
    )
    value = models.CharField(max_length=30, choices=NOTIFICATION_CHOICES
                             , verbose_name='notification method')

class Feature_Creation_Time(Feature_Base):
    value = models.DateTimeField(auto_now_add=True, editable=False)
    
class Feature_Last_Modification_Time(Feature_Base):
    value = models.DateTimeField(auto_now=True)
    
'''  

