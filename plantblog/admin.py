from django.contrib.gis import admin
from markdownx.admin import MarkdownxModelAdmin
from plantblog.models import Entry, GridSquare, Comment, Species
# Register your models here.

class MardownxAdmin(MarkdownxModelAdmin):
    view_on_site = True

admin.site.register(Entry, MardownxAdmin)
admin.site.register(GridSquare)
admin.site.register(Comment, MardownxAdmin)
admin.site.register(Species)