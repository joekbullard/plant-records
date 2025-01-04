from django.contrib.gis.db import models
from taggit.managers import TaggableManager
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify

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
    geom = models.PolygonField(srid=27700)

    def __str__(self):
        return self.name


class Entry(models.Model):

    day_number = models.PositiveIntegerField(editable=False)
    body = MarkdownxField()
    species = models.ForeignKey(Species, related_name="species", on_delete=models.CASCADE)
    grid_square = models.ForeignKey(GridSquare, related_name="entries", on_delete=models.CASCADE)
    publish_date = models.DateField()
    edit_date = models.DateTimeField(auto_now=True)
    tags = TaggableManager()

    @property
    def formatted_markdown(self):
        return markdownify(self.body)

    def save(self, *args, **kwargs):
        if not self.day_number:
            last_day = Entry.objects.aggregate(models.Max('day_number'))['day_number__max'] or 0
            self.day_number = last_day + 1
        super().save(*args, **kwargs)

    def generate_name(self):
        return f"Day {self.day_number} - {self.species.taxon_name}"

    def __str__(self):
        return self.generate_name()

    class Meta:
        verbose_name_plural = "entries"


class Comment(models.Model):

    entry = models.ForeignKey(Entry, related_name="comments", on_delete=models.CASCADE)
    body = MarkdownxField(max_length=500)
    publish_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["entry", "-publish_date"]