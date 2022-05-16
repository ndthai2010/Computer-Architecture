from goto import *
import time
import var
import pio
import resource
import Ports

def peripheral_setup():
    pio.terminal=Ports.SerialTerminal (9600)
def variables_setup():
    var.Name = " "
def peripheral_loop () :
    pass

    