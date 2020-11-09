from django.conf import settings
from django.db import models
from django.utils import timezone


class ExperimentoGangorra(models.Model):
    experimento_id = models.AutoField(primary_key=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)

    csvArquivo = models.FileField(upload_to='gangorra/csv/', null=True, verbose_name="")
    videoArquivo = models.FileField(upload_to='gangorra/videos/', null=True, verbose_name="")

    modelo_kp = models.CharField(max_length=20, default='0')
    modelo_ki = models.CharField(max_length=20, default='0')
    modelo_kd = models.CharField(max_length=20, default='0')
    modelo_referencia = models.CharField(max_length=20, default='0')
    modelo_repeticoes = models.CharField(max_length=20, default='0')

    def publish(self):
        self.save()

    def __str__(self):
        return self.title

