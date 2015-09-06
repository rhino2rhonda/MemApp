from django.contrib import admin
from notes.models import NotesTemplateXML, NotesMetaXML, NoteRegistry
# Register your models here.
admin.site.register(NotesMetaXML)
admin.site.register(NotesTemplateXML)
admin.site.register(NoteRegistry)