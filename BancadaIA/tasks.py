from __future__ import absolute_import
from celery import shared_task
from celery.utils.log import get_task_logger
from .MicropythonESP import MicropythonESP
from celery_progress.backend import ProgressRecorder

logger = get_task_logger(__name__)

@shared_task(name="enviarCodigoTask")
def enviarCodigoTask(IPAddress, IPPort, codigo):
    #progress_recorder = ProgressRecorder(self)
    #logger.info("entrei em enviar codigo")
    esp = MicropythonESP(IPAddress, IPPort)
    esp.runexperiment(codigo)
    #logger.info('em task: terminei send codigo')
