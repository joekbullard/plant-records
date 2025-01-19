from django.contrib.gis.db import models
from plantblog.constants import OS_GRID_PREFIXES
from django.contrib.gis.geos import Polygon
from django.urls import reverse
import datetime
import json

class Species(models.Model):
    ddb_id = models.CharField(max_length=20, unique=True)
    taxon_name = models.TextField()
    common_name = models.TextField(null=True)
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
    geom = models.PolygonField(srid=27700, blank=True, null=True)

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

        bottom_left = (easting, northing)
        top_left = (easting, northing + 100)
        top_right = (easting + 100, northing + 100)
        bottom_right = (easting + 100, northing)

        grid_polygon = Polygon(
            (bottom_left, top_left, top_right, bottom_right, bottom_left), srid=27700
        )

        return grid_polygon
    
    def to_geojson(self):

        related_links = [
        reverse('entry_detail', args=[related.pk])  # Replace with your actual URL name
        for related in self.records.all()
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

class Photo(models.Model):
    image = models.ImageField(upload_to='photos/% Y/% m/% d/')
    caption = models.TextField(null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)


class Abundance(models.IntegerChoices):
    INDIVIDUAL = 1, "Individual"
    FEW = 2, "Few"
    MANY = 3, "Many"


class Record(models.Model):
    species = models.ForeignKey(Species, related_name="records", on_delete=models.CASCADE)
    record_data = models.DateField(default=datetime.date.today())
    sensitive = models.BooleanField(default=False)
    osgrid = models.ForeignKey(GridSquare, related_name="records", on_delete=models.CASCADE)
    abundance = models.SmallIntegerField(choices=Abundance.choices, default=Abundance.INDIVIDUAL)
    location = models.TextField(null=True, blank=True)
    comments = models.TextField(null=True, blank=True)
    photos = models.ForeignKey(Photo, related_name="records", on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

