import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk
from beat_gen import BeatGenerator


def create_and_play(widget, data):
    carrier_box  = data[0]
    beat_box     = data[1] ## boots n cats n boots n cats
    duration_box = data[2]

    carrier_freq = float(carrier_box.get_text())
    beat_freq    = float(beat_box.get_text())
    duration     = float(duration_box.get_text())

    generator = BeatGenerator(carrier=carrier_freq, beat_freq=beat_freq, duration=duration)    
    generator.play()


def main():
    builder = gtk.Builder()
    builder.add_from_file('main.ui')  

    main_window     = builder.get_object('main_window')
    main_play       = builder.get_object('main_play')
    carrier_freq    = builder.get_object('carrier_freq')
    beat_freq       = builder.get_object('beat_freq')
    duration        = builder.get_object('duration')

    main_window.connect('destroy', gtk.main_quit)
    main_play.connect('clicked', create_and_play,
        (carrier_freq, beat_freq, duration))

    gtk.main()


if __name__ == '__main__':
    main()
