from datetime import datetime
import os
import time
from celery_progress.backend import ProgressRecorder


class MicropythonESP:
    def __init__(self, ip, p_recorder):
        self.IPAddress = ip
        self.progress_recorder = p_recorder

    def runexperiment(self, codigo):
        self.progress_recorder.set_progress(0, 3)

        print("micropythonESP")

        codigo.replace('\r\r', '')
        filename = "exp"+datetime.now().strftime("%d%m%Y%H%M%S")
        f = open("temp\\" + filename + ".py", "w", newline="\n")  # newline="\n" evita o problema de fim de linha errado no arquivo
        f.write(codigo)
        f.close()
        self.progress_recorder.set_progress(1, 4)

        # faz upload do experimento
        comandoUpload = "python upload.py -p senha temp/" + filename + ".py " + self.IPAddress + ":/experimentos/"  # trocar para python3 no linux
        os.system(comandoUpload)
        print("terminei o upload")
        self.progress_recorder.set_progress(2, 4)

        # executa experimento remotamente
        comandoExecutar = "python executar.py " + filename + " " + self.IPAddress # trocar para python3 no linux
        os.system(comandoExecutar)
        os.remove('temp/' + filename + ".py")
        self.progress_recorder.set_progress(3, 4)
        time.sleep(2)
        # faz download dos dados
        comandoUpload = "python upload.py -p senha " + self.IPAddress + ":/dados.txt temp"  # trocar para python3 no linux
        os.system(comandoUpload)
        print("terminei o download dos dados")
        self.progress_recorder.set_progress(4, 4)

        return True
