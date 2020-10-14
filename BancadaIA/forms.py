from django import forms
from .models import ExperimentoSpotNano


class PostForm(forms.ModelForm):

    class Meta:
        model = ExperimentoSpotNano
        fields = ('title', 'codigo',)

