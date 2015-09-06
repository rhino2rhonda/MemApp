
from django.shortcuts import render
from django.views.generic import View
from django.views.generic.base import TemplateView
from notes.models import Note
from notes.forms import CompositeNoteForm

# Create your views here.
class HomeView(TemplateView):
    template_name = 'common/index.html'

# Create your views here.
class TodoView(View):
    template_name = 'common/todo2.html'
    form_type = "todo"
    initial = {}
    
    def get(self, request, *args, **kwrgs):
        
        todo = CompositeNoteForm(self.form_type)
        return render(request, self.template_name, {'feature_forms' : todo.forms,\
                                                    'note_properties' : todo.note_properties,\
                                                    'note_name' : todo.note_name},)
    
    def post(self, request, *args, **kwrgs):
        return render(request, "<html><body><h1>yet todo ;)</h1></body></html>", {})
