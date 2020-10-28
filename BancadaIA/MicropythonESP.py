import os
import time
from celery_progress.backend import ProgressRecorder

class MicropythonESP:
    def __init__(self, ip, port):
        self.IPAddress = ip
        self.IPPort = port

    def runexperiment(self, codigo):
        codigo.replace('\r\r', '')
        filename = "teste.py"  # datetime.now().strftime("%d-%m-%Y-%H-%M-%S") + ".py"
        f = open("temp\\" + filename, "w", newline="\n")  # newline="\n" evita o problema de fim de linha errado no arquivo
        f.write(codigo)
        f.close()

        time.sleep(1)

        # faz upload do experimento
        comandoUpload = "python upload.py -p senha temp/teste.py 10.0.0.100:/experimentos/"  # trocar para python3 no linux
        os.system(comandoUpload)
        print("terminei o upload")

        time.sleep(1)

        # executa experimento remotamente
        comandoExecutar = "python executar.py"  # trocar para python3 no linux
        os.system(comandoExecutar)
        os.remove('temp/teste.py')

        time.sleep(1)

        return True
