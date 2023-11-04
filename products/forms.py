from django import forms
from .models import ReviewandRating


class ReviewForms(forms.ModelForm):
    class Meta:
        model = ReviewandRating
        fields = ["subject", "review", "rating"]