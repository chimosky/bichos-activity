#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   OjosCompuestos.py por:
#   Flavio Danesse <fdanesse@gmail.com>
#   Uruguay

import os
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import GObject
from gi.repository import Gdk
from PlayerList import PlayerList
from JAMediaImagenes.ImagePlayer import ImagePlayer

BASE_PATH = os.path.dirname(__file__)


class OjosCompuestos(Gtk.HPaned):

    def __init__(self, pantalla):

        Gtk.HPaned.__init__(self)

        print "Corriendo Ojos Compuestos . . ."

        self.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse("#ffffff"))

        self.player = False
        self.pantalla = pantalla
        self.playerlist = PlayerList()

        self.pack1(self.pantalla, resize=True, shrink=True)
        self.pack2(self.playerlist, resize=False, shrink=False)

        self.playerlist.connect("nueva-seleccion", self.__play_item)

        self.connect("realize", self.__load_imagenes)
        self.show_all()

    def __load_imagenes(self, widget):
        GObject.idle_add(self.__run)

    def __run(self):
        self.player = ImagePlayer(self.pantalla)
        dirpath = os.path.join(BASE_PATH, "Imagenes")
        elementos = []
        for path in sorted(os.listdir(dirpath)):
            elementos.append([path, os.path.join(dirpath, path)])
        self.playerlist.lista.agregar_items(elementos)
        dialog = Dialog(parent=self.get_toplevel(),
            text="Presiona Escape Cuando Desees Salir")
        dialog.run()
        return False

    def __play_item(self, widget, path):
        if path:
            self.player.load(path)

    def salir(self):
        self.player.stop()


class Dialog(Gtk.Dialog):

    def __init__(self, parent=None, text=""):

        Gtk.Dialog.__init__(self, parent=parent)

        self.set_decorated(False)
        self.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse("#ffffff"))
        self.set_border_width(15)

        label = Gtk.Label(text)

        self.vbox.pack_start(label, True, True, 0)
        self.vbox.show_all()

        GObject.timeout_add(3000, self.destroy)
