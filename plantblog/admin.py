from django.contrib.gis import admin
from markdownx.admin import MarkdownxModelAdmin
from plantblog.models import Entry, GridSquare, Comment, Species
# Register your models here.

class MardownxAdmin(MarkdownxModelAdmin):
    autocomplete_fields = ["species"]
    view_on_site = True

class SpeciesAdmin(admin.ModelAdmin):
    search_fields = ['taxon_name']

admin.site.register(Entry, MardownxAdmin)
admin.site.register(GridSquare)
admin.site.register(Comment)
admin.site.register(Species, SpeciesAdmin)