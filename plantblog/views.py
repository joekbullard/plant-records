from django.shortcuts import render
from django.views.generic import TemplateView
from plantblog.models import Entry, Species
from plantblog.forms import EntryForm
from django.shortcuts import redirect, get_object_or_404
from taggit.models import Tag
from django.db.models import Q # new


class AboutView(TemplateView):
    template_name = "about.html"


def home_view(request):
    entries = Entry.objects.all()
    tags = Tag.objects.all()
    ctx = {"entries": entries, "tags": tags }
    return render(request, "home.html", ctx)


def add_entry(request):
    if request.method == "GET":
        form = EntryForm()

    else:
        form = EntryForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("home")

    return render(request, "create-entry.html", {"form": form})


def entry_detail_view(request, pk):
    entry = get_object_or_404(Entry, pk=pk)
    tags = entry.tags.all()
    return render(request, "post-detail.html", {"entry": entry, "tags": tags })


def entries_by_tag(request, tag_slug):
    tags = Tag.objects.all()
    tag = get_object_or_404(Tag, slug=tag_slug)
    entries = Entry.objects.filter(tags=tag)
    return render(request, 'home.html', {"entries": entries, "tags": tags })


def search_species(request):

    search_name = request.GET.get("q").strip()

    if not search_name:
        return render(request, 'partials/search-results.html', {"results": []})
    
    results = Species.objects.filter(
        Q(taxon_name__icontains=search_name) |
        Q(common_name__icontains=search_name)
    )
    return render(request, 'partials/search-results.html', {"results": results})

