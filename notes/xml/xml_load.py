from xml.etree import ElementTree as ET
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from notes.models import NotesTemplateXML, NotesMetaXML, NoteRegistry
from datetime import datetime
from boto.dynamodb.condition import NULL

#TODO put these in the the settings directory
NOTE_TEMPLATE_XML = r"D:\dev\MemAppDjango\notes\xml\note_templates.xml"
NOTE_META_XML = r"D:\dev\MemAppDjango\notes\xml\note_meta.xml"

def user_prompt_replace(xml_file_name, note_id, note_property, old_value, new_value):
    print "XML File, " + xml_file_name + ", has a new value of " +\
            note_property + " for a note with id " + str(note_id) +\
            "Old Value was : " + str(old_value) + "\nNew Value is : " + str(new_value)
    while True:
        reply = raw_input("Choose 'y' to proceed with this modification and 'n' to decline it: ")
        if reply == 'y':
            return True
        elif reply == 'n':
            return False
        
def user_prompt_delete(note_id, note_key_name):
    print "Note with id", note_id, "and key name", note_key_name, "was not found in the meta xml file.\
    \nDo you want to delete it?"
    while True:
        reply = raw_input("Choose 'y' to delete it or 'n' to keep it: ")
        if reply == 'y':
            return True
        elif reply == 'n':
            return False

#checks for changes in xml
#loads new xml and modifies NotesRegistry Table accordingly
def load_note_meta_xml():
    #load new xml from file
    try:
        with open(NOTE_META_XML, 'r') as nmx:
            nmx_content = nmx.read()
    except:
        print "Error reading note meta xml from file path :", NOTE_META_XML
        return "No Change"
    
    #load latest xml in db
    try:
        xml_old = NotesMetaXML.objects.latest('timestamp')
    except ObjectDoesNotExist:
        xml_old = None
        
    #terminate if xml is not updated
    if xml_old and nmx_content == xml_old.xml:
        #print nmx_content
        #print xml_old.xml
        return "No Change"
    
    #Use this time stamp to detect which models have been updated
    update_timestamp = datetime.now()
    
    #Parse the xml and update the databases
    note_list_xml = ET.fromstring(nmx_content)
    for note_xml in note_list_xml:
        
        _id = int(note_xml.attrib['id'])
        try:
            nreg_entry = NoteRegistry.objects.get(nid=_id)
            new_entry = False
        except ObjectDoesNotExist:
            new_entry = True
            nreg_entry = NoteRegistry(nid=_id)            
        
        #Update Key Name
        need_to_update = True
        if not new_entry:
            old_name = nreg_entry.key_name
            new_name = note_xml.attrib['key_name']
            if old_name != new_name:
                need_to_update = user_prompt_replace(NOTE_META_XML, _id, "key_name", old_name, new_name)
        
        if need_to_update:
            nreg_entry.key_name = note_xml.attrib['key_name']
            
        #Update Parent
        need_to_update = True
        if not new_entry:
            if nreg_entry.parent == None:
                old_value = "none"
            else:
                old_value = nreg_entry.parent.key_name
            new_value = note_xml.attrib['parent']
            if old_value != new_value:
                need_to_update = user_prompt_replace(NOTE_META_XML, _id, "parent", old_value, new_value)
        
        if need_to_update:
            new_value = note_xml.attrib['parent']
            #print "BUG-DE :", new_value
            if new_value=="none":
                nreg_entry.parent = None
            else:
                nreg_entry.parent = NoteRegistry.objects.get(key_name=new_value)
        
        #Update the last updated timestamp
        nreg_entry.last_updated = update_timestamp
        
        #Save the changes made
        try:
            nreg_entry.save()
        except Exception as e: #TODO DB Constraint exception
            print  "XML LOAD ERROR: Failure in saving note meta record for note with note id",\
            _id, "\nThe table constraints might have been violated. Check the error message for\
            more details.\n" + str(e)
            
    unfetched_notes = NoteRegistry.objects.filter(~Q(last_updated=update_timestamp))
    print "unfetched: ", len(unfetched_notes)
    for note in unfetched_notes:
        del_ = user_prompt_delete(note.nid, note.key_name)
        if del_:
            note.delete()
    
           
    #store the new xml in the db
    xml_new = NotesMetaXML(xml=nmx_content)
    xml_new.save()
    
    return "Changed"


def load_note_template_xml():
    #load new xml from file
    try:
        with open(NOTE_TEMPLATE_XML, 'r') as ntx: 
            ntx_content = ntx.read()
    except:
        print "Error reading note template xml from file path :", NOTE_TEMPLATE_XML
        return "No Change"
        
    #load latest xml in db
    try:
        xml_old = NotesTemplateXML.objects.latest('timestamp')
    except ObjectDoesNotExist:
        xml_old = None
        
    #terminate if xml is not updated
    if xml_old and ntx_content == xml_old.xml:
        return "No Change"
    
    #Parse the xml and update the databases
    note_list_xml = ET.fromstring(ntx_content)
    for note_xml in note_list_xml:
        try:
            key_name = note_xml.attrib['key_name']
            nreg_entry = NoteRegistry.objects.get(key_name=key_name)
        except ObjectDoesNotExist:
            print "XML LOAD ERROR: Could not find note with keyname", key_name, "in the database\
            while loading template xml. This element will be skipped."
            continue
        nreg_entry.attrib_dict = dict_from_xml_element(note_xml)
        nreg_entry.save()
        
    #store the new xml in the db
    xml_new = NotesTemplateXML(xml=ntx_content)
    xml_new.save()
    
    return "Changed"

#TODO Test this shizz
def dict_from_xml_element(element, dict_ = None):
    if dict_ == None:
        dict_ = {}
    dict_.update(element.attrib)
    for subel in element:
        if len(element.findall(subel.tag)) == 1:
            if subel.text and subel.text.strip():
                dict_[subel.tag] = subel.text.strip()
                continue
            dict_[subel.tag] = {}
            child_dict = dict_[subel.tag]
        else:
            try:
                dict_[subel.tag].append({})
            except KeyError:
                dict_[subel.tag] = [{}]
            child_dict = dict_[subel.tag][-1]
        child_dict = dict_from_xml_element(subel, child_dict)
    return dict_
        

