import sys
from pyreadline import Readline as readline # mudar quando usar servidor linux
#import readline
import getpass
import websocket

try:
    import thread
except ImportError:
    import _thread as thread
from time import sleep

try:                   # from https://stackoverflow.com/a/7321970
    input = raw_input  # Fix Python 2.x.
except NameError:
    pass

filename = sys.argv[1]
ipaddress = sys.argv[2]

inp = ""
raw_mode = False
normal_mode = True
paste_mode = False
prompt = "Password: "
prompt_seen = False
passwd = 'senha'
debug = False
redirect = False

def on_message(ws, message):
    global inp
    global raw_mode
    global normal_mode
    global paste_mode
    global prompt
    global prompt_seen
    if len(inp) == 1 and ord(inp[0]) <= 5:
        inp = "\r\n" if inp != '\x04' else "\x04"
    while inp != "" and message != "" and inp[0] == message[0]:
        inp = inp[1:]
        message = message[1:]
    if message != "":
        if not(raw_mode) or inp != "\x04":
            inp = ""
    if raw_mode:
        if message == "OK":
            inp = "\x04\x04"
        elif message == "OK\x04":
            message = "OK"
            inp = "\x04"
        elif message == "OK\x04\x04":
            message = "OK"
            inp = ""
        elif message == "OK\x04\x04>":
            message = "OK>"
            inp = ""
    if debug:
        print("[%s,%d,%s]" % (message, ord(message[0]), inp))
    if inp == '' and prompt != '':
        if message.endswith(prompt):
            prompt_seen = True
        elif normal_mode:
            if message.endswith("... "):
                prompt = ""
            elif message.endswith(">>> "):
                prompt = ">>> "
                prompt_seen = True
    if prompt_seen:
        sys.stdout.write(message[:-len(prompt)])
    else:
        sys.stdout.write(message)
    sys.stdout.flush()
    if paste_mode and message == "=== ":
        inp = "\n"


def on_error(ws, error):
    sys.stdout.write("### error("+error+") ###\n")
    sys.stdout.flush()


def on_close(ws):
    sys.stdout.write("### closed ###\n")
    sys.stdout.flush()
    ws.close()
    sys.exit(1)


def on_open(ws):
    def run(*args):
        global input
        global inp
        global raw_mode
        global normal_mode
        global paste_mode
        global prompt
        global prompt_seen

        teste = False

        running = True
        injected = False
        do_input = getpass.getpass
        print(filename)
        comandos = ["import os",
                    "os.remove('" + filename + ".csv')",
                    "\x04"]
        contadorComandos = 0

        while running:
            while ws.sock and ws.sock.connected:
                while prompt and not(prompt_seen):
                    sleep(0.2)

                prompt_seen = False

                if prompt == "Password: ":
                    inp = passwd
                    #sys.stdout.write("Pediu Password: ")
                    #sys.stdout.flush()
                else:
                    if contadorComandos > 3:
                        inp = "exit"
                    else:
                        sleep(0.1)
                        inp = comandos[contadorComandos] #do_input(prompt)
                        contadorComandos += 1
                    #if redirect:
                    #    sys.stdout.write(inp+"\n")
                    #    sys.stdout.flush()


                if len(inp) != 1 or inp[0] < 'A' or inp[0] > 'E':
                    inp += "\r\n"
                else:
                    inp = chr(ord(inp[0])-64)
                    if raw_mode:
                        if inp[0] == '\x02':
                            normal_mode = True
                            raw_mode = False
                    elif normal_mode:
                        if inp[0] == '\x01':
                            raw_mode = True
                            normal_mode = False
                        elif inp[0] == '\x05':
                            paste_mode = True
                            normal_mode = False
                    else:
                        if inp[0] == '\x03' or inp[0] == '\x04':
                            normal_mode = True
                            paste_mode = False

                do_input = getpass.getpass if raw_mode else input

                if prompt == "Password: ":  # initial "CTRL-C CTRL-B" injection
                    prompt = ""
                else:
                    prompt = "=== " if paste_mode else ">>> "[4*int(raw_mode):]

                if "exit" in inp:
                    running = False
                    break
                else:
                    if ws.sock and ws.sock.connected:
                        #if not "senha" in inp:
                        #    print(comandos[contadorComandos])
                        #    ws.send(comandos[contadorComandos])
                        #    contadorComandos += 1
                        #else:

                        ws.send(inp)
                             
                        if prompt == "" and not(raw_mode) and not(injected):
                            inp += '\x03\x02'
                            injected = True
                            ws.send('\x03\x02')
                    else:
                        running = False
            running = False
        ws.sock.close()
        sys.exit(1)
    thread.start_new_thread(run, ())


if __name__ == "__main__":
    websocket.enableTrace(False)
    ws = websocket.WebSocketApp("ws://" + ipaddress + ":8266",
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()

