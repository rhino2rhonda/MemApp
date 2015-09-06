from features.models import FeaturesMetaXML, FeatureRegistry
from xml.etree import ElementTree as ET
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from datetime import datetime

#TODO put these in the the settings directory
FEATURE_META_XML = r"D:\dev\MemAppDjango\features\xml\feature_meta.xml"

def user_prompt_replace(xml_file_name, feature_id, feature_property, old_value, new_value):
    print "XML File, " + xml_file_name + ", has a new value of " +\
            feature_property + " for a feature with id " + str(feature_id) +\
            "\nOld Value was : " + str(old_value) + "\nNew Value is : " + str(new_value)
    while True:
        reply = raw_input("Choose 'y' to proceed with this modification and 'n' to decline it: ")
        if reply == 'y':
            return True
        elif reply == 'n':
            return False

def user_prompt_delete(feature_id, feature_key_name):
    print "Feature with id", feature_id, "and key name", feature_key_name, "was not found in the meta xml \
    file. Do you want to delete it?"
    while True:
        reply = raw_input("Choose 'y' to delete it or 'n' to keep it: ")
        if reply == 'y':
            return True
        elif reply == 'n':
            return False

#checks for changes in xml
#loads new xml and modifies FeaturesRegistry Table accordingly 
def load_feature_meta_xml():
    #load new xml from file
    try:
        with open(FEATURE_META_XML, 'r') as fmx:
            fmx_content = fmx.read()
    except:
        print "Error reading feature meta xml from file path :", FEATURE_META_XML
        return "No Change"
    
    #load latest xml in db
    try:
        xml_old = FeaturesMetaXML.objects.latest('timestamp')
    except ObjectDoesNotExist:
        xml_old = None
        
    #terminate if xml is not updated
    if xml_old and fmx_content == xml_old.xml:
        return "No Change"
    
    #Use this time stamp to detect which models have been updated
    update_timestamp = datetime.now()
    
    #Parse the xml and update the databases
    feature_list_xml = ET.fromstring(fmx_content)
    for feature_xml in feature_list_xml:
        
        _id = int(feature_xml.attrib['id'])
        try:
            freg_entry = FeatureRegistry.objects.get(fid=_id)
            new_entry = False
        except ObjectDoesNotExist:
            freg_entry = FeatureRegistry(fid=_id)
            new_entry = True
        
        #Update Key Name
        need_to_update = True
        if not new_entry:
            old_name = freg_entry.key_name
            new_name = feature_xml.attrib['key_name']
            if old_name != new_name:
                need_to_update = user_prompt_replace(FEATURE_META_XML, _id, "key_name", old_name, new_name)
        
        if need_to_update:
            freg_entry.key_name = feature_xml.attrib['key_name']
            
        #Update Default UI Rank
        need_to_update = True
        if not new_entry:
            old_value = freg_entry.default_ui_rank
            new_value = int(feature_xml.attrib['default_ui_rank'])
            if old_value != new_value:
                need_to_update = user_prompt_replace(FEATURE_META_XML, _id, "default_ui_rank", old_value, new_value)
        
        if need_to_update:
            freg_entry.default_ui_rank = feature_xml.attrib['default_ui_rank']
            
        #Update Default UI Rank
        need_to_update = True
        if not new_entry:
            old_value = freg_entry.model_class
            new_value = feature_xml.attrib['model_class']
            if old_value != new_value:
                need_to_update = user_prompt_replace(FEATURE_META_XML, _id, "model_class", old_value, new_value)
        
        if need_to_update:
            freg_entry.model_class = feature_xml.attrib['model_class']
        
        #Update the last updated timestamp
        freg_entry.last_updated = update_timestamp
        
        #Save the changes made
        try:
            freg_entry.save()
        except Exception as e: #TODO DB Constraint exception
            print  "XML LOAD ERROR: Failure in saving feature meta record for feature with feature id",\
            _id, "\nThe table constraints might have been violated. Check the error message for\
            more details.\n" + str(e)
            
    unfetched_features = FeatureRegistry.objects.filter(~Q(last_updated=update_timestamp))
    for feature in unfetched_features:
        del_ = user_prompt_delete(feature.fid, feature.key_name)
        if del_:
            feature.delete()
           
    #store the new xml in the db
    xml_new = FeaturesMetaXML(xml=fmx_content)
    xml_new.save()
    
    return "Changed"

