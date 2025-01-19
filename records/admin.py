from django.contrib.gis import admin
from records.models import GridSquare, Species, Record, Photo

# Register your models here.
class RecordAdmin(admin.ModelAdmin):
    autocomplete_fields = ["species"]
    view_on_site = True

class SpeciesAdmin(admin.ModelAdmin):
    search_fields = ['taxon_name']

admin.site.register(Record, RecordAdmin)
admin.site.register(GridSquare, admin.GISModelAdmin)
admin.site.register(Photo)
admin.site.register(Species, SpeciesAdmin)
