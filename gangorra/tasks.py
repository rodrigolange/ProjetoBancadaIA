from __future__ import absolute_import
from celery import shared_task
from celery.utils.log import get_task_logger
from celery_progress.backend import ProgressRecorder
from django.contrib.auth.models import User
from gangorra.models import ExperimentoGangorra
from .MicropythonESP import MicropythonESP
import os
import pandas as pd

#import threading


logger = get_task_logger(__name__)


@shared_task(bind=True)
def enviarCodigoTask(self, IPAddress, codigo, filename, autor, kp, ki, kd, ref, rep):

    progress_recorder = ProgressRecorder(self)
    progress_recorder.set_progress(0, 3)

    esp = MicropythonESP(IPAddress, progress_recorder)
    esp.runexperiment(codigo, filename)

    dfilename = filename + ".csv"
    vfilename = filename + ".mp4"
    gfilename = filename + ".png"

    os.rename("temp/"+filename+".csv", "media/gangorra/csv/"+filename+".csv")

    dados = pd.read_csv("media/gangorra/csv/" + filename + ".csv")
    grafico = dados.plot.line()
    grafico.figure.savefig("media/gangorra/graficos/" + filename + ".png")

    user = User.objects.get(username=autor)
    r = ExperimentoGangorra(title=filename,
                            author=user,
                            modelo_kp=kp,
                            modelo_ki=ki,
                            modelo_kd=kd,
                            modelo_referencia=ref,
                            modelo_repeticoes=rep,
                            csvArquivo=dfilename,
                            videoArquivo=vfilename,
                            graficoArquivo=gfilename)
    r.publish()


