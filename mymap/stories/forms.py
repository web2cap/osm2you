from django import forms
from django.conf import settings

from .models import Story

STORY_MIN_LEN = getattr(settings, "STORY_MIN_LEN", None)
STORY_PER_PAGE = getattr(settings, "STORY_PER_PAGE", None)


class StoryForm(forms.ModelForm):
    """Add story form."""

    class Meta:
        model = Story
        fields = ["text"]

    def clean_text(self):
        data = self.cleaned_data["text"]

        if len(data) < STORY_MIN_LEN:
            raise forms.ValidationError(
                f"Minimum test len is {STORY_MIN_LEN} sumbols!"
            )

        return data


class StoryDropForm(forms.Form):
    confirm = forms.ChoiceField(
        widget=forms.CheckboxInput, label="Confirm delete story", required=True
    )
