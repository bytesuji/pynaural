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
