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
from beat_gen import BeatGenerator
from auxiliary import *

GENERATOR = BeatGenerator()

def main():
    builder = gtk.Builder()
    builder.add_from_file('main.ui')  

    main_window     = builder.get_object('main_window')
    main_play       = builder.get_object('main_play')
    main_stop       = builder.get_object('main_stop')

    carrier_freq    = builder.get_object('carrier_freq')
    beat_freq       = builder.get_object('beat_freq')
    duration        = builder.get_object('duration')
    volume_adjust   = builder.get_object('volume_adjust')

    file_quit       = builder.get_object('file_quit')
    help_about      = builder.get_object('help_about')

    about_window    = builder.get_object('about_window')

    main_window.connect('destroy', full_quit)
    file_quit.connect('activate', full_quit)
    help_about.connect('activate', dialog_run, about_window)
    main_play.connect('clicked', create_and_play,
        (carrier_freq, beat_freq, duration, volume_adjust))
    main_stop.connect('clicked', pause)

    gtk.main()


if __name__ == '__main__':
    main()
