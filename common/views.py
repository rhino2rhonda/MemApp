from django.shortcuts import render
from django.views.generic import View
from django.views.generic.base import TemplateView
from features.note_models import Note


# Create your views here.
class HomeView(TemplateView):
    template_name = 'common/index.html'
    
# Create your views here.
class TodoView(View):
    template_name = 'common/todo2.html'
    form_type = "todo"
    initial = {}
    
    def get(self, request, *args, **kwrgs):
        print "debug 12123has"
        #for field_name in TodoNote._meta.get_fields():
        #   print type(field_name), field_name
        todonote = Note.objects.get(note_key_name=self.form_type)
        todoform = todonote.getCompositeForm()
        return render(request, self.template_name, {'forms' : todoform})
    
    def post(self, request, *args, **kwrgs):
        return render(request, "<html><body><h1>yet todo ;)</h1></body></html>", {})
    
    