import os
from modelhubapi import webservice
from inference import Model

if __name__ == "__main__":
    model = Model()
    contrib_src_dir = os.path.dirname(os.path.realpath(__file__))
    webservice.start(model, contrib_src_dir)
