from django import forms
from plantblog.models import Entry
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from plantblog.constants import OS_GRID_PREFIXES
from markdownx.widgets import MarkdownxWidget
from taggit.forms import TagWidget


class TextInput(forms.TextInput):
    def __init__(self, attrs=None):
        default_attrs = {"class": "input input-bordered input-lg w-full max-w-xs"}

        if attrs:
            default_attrs.update(attrs)  # Merge with any custom attrs
        super().__init__(attrs=default_attrs)


class DateInput(forms.DateInput):
    input_type = "date"

    def __init__(self, attrs=None):
        default_attrs = {"class": "input input-bordered input-lg w-full max-w-xs"}
        if attrs:
            default_attrs.update(attrs)  # Merge with any custom attrs
        super().__init__(attrs=default_attrs)


def validate_grid_ref(grid_ref: str) -> None:
    if not isinstance(grid_ref, str):
        raise ValidationError(
            _("Grid reference must be a string, but got %(type)s"),
            params={"type": type(grid_ref).__name__},
        )

    prefix = grid_ref[0:2].upper()
    digits = grid_ref[2:9]

    if prefix not in OS_GRID_PREFIXES:
        raise ValidationError(
            _("%(prefix)s is not a valid prefix"), params={"prefix": prefix}
        )

    for digit in digits:
        if not digit.isdigit():
            raise ValidationError(
                _("%(digit)s is not a valid digit"), params={"digit": digit}
            )


class EntryForm(forms.ModelForm):
    grid_ref = forms.CharField(
        max_length=8,
        validators=[validate_grid_ref],
        widget=TextInput(attrs={"placeholder": "Enter grid ref"}),
    )
    field_order = ["grid_ref", "publish_date", "species", "body", "tags"]

    class Meta:
        model = Entry
        fields = ["species", "body", "tags", "publish_date"]
        widgets = {
            "tags": TagWidget(attrs={"class": "input input-bordered input-lg w-full max-w-md"}),
            "publish_date": DateInput(),
            "body": MarkdownxWidget(
                attrs={
                    "class": "textarea textarea-bordered textarea-lg w-full",
                    "placeholder": "Enter markdown",
                }
            ),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)

        grid_ref = self.cleaned_data["grid_ref"]
        instance.set_or_create_grid_ref(grid_ref)

        if commit:
            instance.save()

        return instance
