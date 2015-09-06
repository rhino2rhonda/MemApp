from django.apps.config import AppConfig
from features.xml.xml_load import load_feature_meta_xml
from notes.xml.xml_load import load_note_meta_xml, load_note_template_xml

#Use this to toggle the startup activities
DISABLE = False

#Put startup code in teh ready function
#This app is to be loaded at the end so that other apps are ready to be configured
class CommonConfig(AppConfig):
    name = "common"
    def ready(self):
        if DISABLE:
            return None
        
        print "Running the startup shizznit!"
        
        #list of startup tasks
        startup_tasks = [
        #(TaskName, TaskFunction)
        ('Feature Meta XML Load', load_feature_meta_xml),
         ('Note Meta XML Load', load_note_meta_xml),
         ('Note Template XML Load', load_note_template_xml),
        ]
        
        for task_name, task_function in startup_tasks:
            print "STARTUP TASKS : Task " + task_name + " has started."         
            result = task_function()
            if result == "No Change":
                print "STARTUP TASKS : Task " + task_name + " was terminated. No changes were made to the database."
            elif result == "Changed":
                print "STARTUP TASKS : Task " + task_name + " successfully completed. The databases have been updated."
            else:
                print "XML LOAD : Invalid Result Returned : ", result