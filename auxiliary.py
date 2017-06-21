# Copyright (c) 2017, Albert Brox III
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
# 
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk
from threading import Thread
from main import GENERATOR


def show_object(widget, data):
    data.show_all()

def hide_object(widget, data):
    data.hide()


def dialog_run(widget, data):
    data.run()
    data.hide()


def full_quit(widget):
    gtk.main_quit()
    exit(0)


def pause(widget):
    global GENERATOR
    GENERATOR.pause()


def create_and_play(widget, data):
    carrier_box   = data[0]
    beat_box      = data[1] ## boots n cats n boots n cats
    duration_box  = data[2]
    volume_adjust = data[3]

    carrier_freq  = float(carrier_box.get_text())
    beat_freq     = float(beat_box.get_text())
    duration      = int(round(float(duration_box.get_text()), 0))
    volume        = int(volume_adjust.get_value()) / 100

    global GENERATOR
    GENERATOR.__init__(carrier=carrier_freq, duration=duration, beat_freq=beat_freq, vol=volume)

    t = Thread(target=GENERATOR.play)
    t.daemon = True
    t.start()


def update_volume(widget, data):
    volume = int(data.get_value()) / 100

    global GENERATOR
    GENERATOR.vol = volume
    GENERATOR.pause()
    GENERATOR.play()
