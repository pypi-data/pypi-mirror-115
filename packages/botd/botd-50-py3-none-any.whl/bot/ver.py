# This file is placed in the Public Domain

from ob import kernel

k = kernel()

def ver(event):
    event.reply("%s %s" % (k.cfg.name.upper(), k.cfg.version))
