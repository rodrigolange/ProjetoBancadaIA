import os


class MicropythonESP:
    def __init__(self, ip):
        self.IPAddress = ip

    def runexperiment(self, codigo):
        codigo.replace('\r\r', '')
        filename = "teste.py"  # datetime.now().strftime("%d-%m-%Y-%H-%M-%S") + ".py"
        f = open("temp\\" + filename, "w", newline="\n")  # newline="\n" evita o problema de fim de linha errado no arquivo
        f.write(codigo)
        f.close()

        # faz upload do experimento
        comandoUpload = "python upload.py -p senha temp/teste.py " + self.IPAddress + ":/experimentos/"  # trocar para python3 no linux
        os.system(comandoUpload)
        print("terminei o upload")


        # executa experimento remotamente
        comandoExecutar = "python executar.py"  # trocar para python3 no linux
        os.system(comandoExecutar)
        os.remove('temp/teste.py')


        return True
