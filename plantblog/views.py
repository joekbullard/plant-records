from django.shortcuts import render
from django.views.generic import TemplateView
from plantblog.models import Entry


class AboutView(TemplateView):
    template_name = 'about.html'
    

def home_view(request):

    entries = Entry.objects.all()
    ctx = { "entries": entries}

    return render(request, "home.html", ctx)
