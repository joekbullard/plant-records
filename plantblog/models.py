from django.contrib.gis.db import models
from taggit.managers import TaggableManager
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify
from plantblog.constants import OS_GRID_PREFIXES
from django.contrib.gis.geos import Polygon
from django.urls import reverse
import json

class Species(models.Model):
    ddb_id = models.CharField(max_length=20, unique=True)
    taxon_name = models.TextField()
    common_name = models.TextField()
    tyk = models.CharField(max_length=16)
    rank = models.CharField(max_length=30)

    def __str__(self):
        if self.common_name:
            return f"{self.taxon_name} {self.common_name}"
        return self.taxon_name

    def bsbi_url(self):
        return f"https://bsbi.org/taxon?taxonid={self.ddb_id}"

    def nbn_url(self):
        return f"https://species.nbnatlas.org/species/{self.tyk}"

    class Meta:
        ordering = ["taxon_name"]
        verbose_name_plural = "species"


class GridSquare(models.Model):
    name = models.CharField(max_length=8, unique=True)
    geom = models.PolygonField(srid=4326, geography=True, blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.pk is not None:  # Only check if it's an update, not a new object
            original = GridSquare.objects.get(pk=self.pk)
            if original.name != self.name:  # If the name has changed
                self.geom = self.generate_geom()

        if not self.geom:
            self.geom = self.generate_geom()
    
        super().save(*args, **kwargs)

    def generate_geom(self):
        prefix = self.name[0:2]
        x_digits = self.name[2:5].ljust(5, "0")
        y_digits = self.name[5:8].ljust(5, "0")

        x_grid, y_grid = OS_GRID_PREFIXES[prefix]

        easting = int(x_grid + x_digits)
        northing = int(y_grid + y_digits)

        south_west = (easting, northing)
        north_west = (easting, northing + 100)
        north_east = (easting + 100, northing + 100)
        south_east = (easting + 100, northing)

        grid_polygon = Polygon(
            (south_west, north_west, north_east, south_east, south_west), srid=27700
        )

        grid_polygon.transform(4326)

        return grid_polygon
    
    def to_geojson(self):


        related_links = [
        reverse('entry_detail', args=[related.pk])  # Replace with your actual URL name
        for related in self.entries.all()
        ]
 
        geojson = {
            "type": "Feature",
            "id": self.pk,
            "geometry": json.loads(self.geom.geojson),
            "properties": {
                "name": self.name,
                "related_links": related_links
            }
        }

        return geojson

    @classmethod
    def to_geojson_collection(cls, queryset):
        """Serialize a queryset to a GeoJSON FeatureCollection."""
        features = [obj.to_geojson() for obj in queryset]  # Use the instance method
        return {
            "type": "FeatureCollection",
            "features": features,
        }


class Entry(models.Model):
    day_number = models.PositiveIntegerField(editable=False)
    body = MarkdownxField()
    species = models.ForeignKey(
        Species, related_name="entries", on_delete=models.CASCADE
    )
    grid_square = models.ForeignKey(
        GridSquare, related_name="entries", on_delete=models.CASCADE
    )
    publish_date = models.DateField()
    edit_date = models.DateTimeField(auto_now=True)
    tags = TaggableManager()

    @property
    def formatted_markdown(self):
        return markdownify(self.body)
    
    @property
    def preview_markdown(self):
        return markdownify(self.body[:300])

    def save(self, *args, **kwargs):
        if not self.day_number:
            last_day = (
                Entry.objects.aggregate(models.Max("day_number"))["day_number__max"]
                or 0
            )
            self.day_number = last_day + 1
        super().save(*args, **kwargs)

    def generate_name(self):
        return f"Day {self.day_number} - {self.species.taxon_name}"

    def set_or_create_grid_ref(self, grid_ref):
        related_grid_ref, created = GridSquare.objects.get_or_create(name=grid_ref)
        self.grid_square = related_grid_ref
        return created

    def __str__(self):
        return self.generate_name()

    class Meta:
        verbose_name_plural = "entries"
        ordering = ["-day_number"]


class Comment(models.Model):
    entry = models.ForeignKey(Entry, related_name="comments", on_delete=models.CASCADE)
    body = MarkdownxField(max_length=500)
    publish_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["entry", "-publish_date"]
