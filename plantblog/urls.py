from django.urls import path
from plantblog.views import home_view, add_entry, entry_detail_view, entries_by_tag, search_species

urlpatterns = [
    path('posts', home_view, name='home'),
    path('posts/<int:pk>', entry_detail_view, name='entry_detail'),
    path('create-entry', add_entry, name='create_entry'),
    path('tags/<slug:tag_slug>/', entries_by_tag, name='entries_by_tag'),
    path('search-species', search_species, name='search_species')
]

