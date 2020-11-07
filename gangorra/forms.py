from django import forms
from .models import ExperimentoGangorra


class VideoForm(forms.ModelForm):
    class Meta:
        model = ExperimentoGangorra
        fields = ["title", "csvArquivo", "videoArquivo"]
