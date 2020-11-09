from __future__ import absolute_import
from celery import shared_task
from celery.utils.log import get_task_logger
from celery_progress.backend import ProgressRecorder
from django.contrib.auth.models import User
from gangorra.models import ExperimentoGangorra
from .MicropythonESP import MicropythonESP

logger = get_task_logger(__name__)


@shared_task(bind=True)
def enviarCodigoTask(self, IPAddress, codigo):

    progress_recorder = ProgressRecorder(self)
    progress_recorder.set_progress(0, 3)
    esp = MicropythonESP(IPAddress, progress_recorder)
    esp.runexperiment(codigo)

    user = User.objects.get(username='lange')
    r = ExperimentoGangorra(author=user, csvArquivo='dados12.txt', videoArquivo='dados12.mp4')
    r.publish()


