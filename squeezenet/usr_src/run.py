import webservice
import netron
import sys
import time
from multiprocessing import Process


def startNetron():
    netron.serve_file("/usr_src/model/model.onnx", port=81, host="0.0.0.0")


if __name__ == "__main__":
#    netronProcess = Process(target=startNetron)
#    netronProcess.start()
    webservice.start()
#    netronProcess.terminate()
