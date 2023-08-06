# -*- coding: latin1 -*-
from time import *
from pygame import *
from pythonBgt import *
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"]="hide"
mixer.init()
def fala(text):
    speak(text)
    waitKey(K_RETURN)
