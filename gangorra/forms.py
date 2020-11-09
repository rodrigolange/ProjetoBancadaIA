from django import forms
from .models import ExperimentoGangorra


class FormExperimento(forms.ModelForm):
    class Meta:
        model = ExperimentoGangorra
        fields = ["modelo_kp", "modelo_ki", "modelo_kd", "modelo_referencia", "modelo_repeticoes"]


class FormVideo(forms.ModelForm):
    class Meta:
        model = ExperimentoGangorra
        fields = ["csvArquivo", "videoArquivo"]

