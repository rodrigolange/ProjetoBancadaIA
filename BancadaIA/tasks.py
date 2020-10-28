from __future__ import absolute_import
from celery import shared_task
from celery.utils.log import get_task_logger
import os
from .MicropythonESP import MicropythonESP
from celery_progress.backend import ProgressRecorder


logger = get_task_logger(__name__)


@shared_task(bind=True)
def enviarCodigoTask(self, IPAddress, codigo):

    progress_recorder = ProgressRecorder(self)
    progress_recorder.set_progress(0, 3)

    logger.info("entrei em enviar codigo")
    esp = MicropythonESP(IPAddress)
    progress_recorder.set_progress(1, 3)

    esp.runexperiment(codigo)
    logger.info('em task: terminei send codigo')
    progress_recorder.set_progress(3, 3)

