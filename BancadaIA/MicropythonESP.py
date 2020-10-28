import os
from celery_progress.backend import ProgressRecorder


class MicropythonESP:
    def __init__(self, ip, p_recorder):
        self.IPAddress = ip
        self.progress_recorder = p_recorder

    def runexperiment(self, codigo):
        self.progress_recorder.set_progress(0, 3)

        codigo.replace('\r\r', '')
        filename = "teste.py"  # datetime.now().strftime("%d-%m-%Y-%H-%M-%S") + ".py"
        f = open("temp\\" + filename, "w", newline="\n")  # newline="\n" evita o problema de fim de linha errado no arquivo
        f.write(codigo)
        f.close()
        self.progress_recorder.set_progress(1, 3)

        # faz upload do experimento
        comandoUpload = "python upload.py -p senha temp/teste.py " + self.IPAddress + ":/experimentos/"  # trocar para python3 no linux
        os.system(comandoUpload)
        print("terminei o upload")
        self.progress_recorder.set_progress(2, 3)

        # executa experimento remotamente
        comandoExecutar = "python executar.py"  # trocar para python3 no linux
        os.system(comandoExecutar)
        os.remove('temp/teste.py')
        self.progress_recorder.set_progress(3, 3)

        return True
