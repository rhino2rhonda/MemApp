from django.db import models

# Create your models here.

#Feature Models
class Feature(models.Model):
    feature_name = models.CharField(max_length=30, )
    
    def __str__(self):
        return self.feature_name
    
class BaseFeature(models.Model):
    value = models.CharField(max_length=30)
    
    def __str__(self):
        return self.value
    
class Feature_Title(BaseFeature):
    pass
    
class Feature_Category(BaseFeature):
    pass
    
class Feature_Content(BaseFeature):
    value = models.Field(max_length=500)
    
    def __str__(self):
        return self.value[:20] + " ..."
    
class Feature_Tags(BaseFeature):
    pass

class Feature_Target_Completion_Date_Initial(BaseFeature):
    value = models.DateField()
    
class Feature_Target_Completion_Date_Current(BaseFeature):
    value = models.DateField()
    
class Feature_Deadline_Initial(BaseFeature):
    value = models.DateField()
    
class Feature_Deadline_Current(BaseFeature):
    value = models.DateField()

class Feature_Notification():
    pass

class Feature_Creation_Time():
    value = models.DateTimeField()
    
class Feature_Last_Modification_Time():
    value = models.DateTimeField()
    
    
#Notes

class BaseNote(models.Model):
    
    title = models.OneToOneField(Feature_Title)
    creation_time = models.OneToOneField(Feature_Creation_Time)
    last_modification_time = models.OneToOneField(Feature_Last_Modification_Time)
    category = models.ForeignKey(Feature_Category)
    tags = models.ManyToManyField(Feature_Tags)
    
class TodoNote(models):
    
    content = models.OneToOneField(Feature_Content)
    target_completion_date_initial = models.OneToOneField(Feature_Target_Completion_Date_Initial)
    target_completion_date_current = models.OneToOneField(Feature_Target_Completion_Date_Current)
    deadline_initial = models.OneToOneField(Feature_Deadline_Initial)
    deadline_current = models.OneToOneField(Feature_Deadline_Current)
    notification = models.ForeignKey(Feature_Notification)

