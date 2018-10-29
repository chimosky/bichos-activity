#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Widgets.py por:
#   Flavio Danesse <fdanesse@gmail.com>
#   Uruguay

import os
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import GObject
from gi.repository import Gdk
from gi.repository import GdkPixbuf
import pygame
from pygame.sprite import Sprite
from JAMediaImagenes.ImagePlayer import ImagePlayer
from JAMediaReproductor.JAMediaReproductor import JAMediaReproductor

BASE_PATH = os.path.dirname(__file__)


def get_separador(draw=False, ancho=0, expand=False):
    separador = Gtk.SeparatorToolItem()
    separador.props.draw = draw
    separador.set_size_request(ancho, -1)
    separador.set_expand(expand)
    return separador


def describe_archivo(archivo):
    import commands
    datos = commands.getoutput('file -ik %s%s%s' % ("\"", archivo, "\""))
    retorno = ""
    for dat in datos.split(":")[1:]:
        retorno += " %s" % (dat)
    return retorno


class Widget_Leccion(Gtk.Dialog):

    def __init__(self, parent=None, lectura=""):

        Gtk.Dialog.__init__(self, parent=parent,
            buttons=("Cerrar", Gtk.RESPONSE_ACCEPT))

        self.set_decorated(False)
        self.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse("#ffffff"))
        self.set_border_width(15)

        self.panel = Panel(lectura)
        self.vbox.pack_start(self.panel, True, True, 0)
        self.vbox.show_all()

        rect = Gdk.Rectangle
        rect.width = self.ventana.get_allocated_width()
        rect.height = self.ventana.get_allocated_height()
        self.set_size_request(rect.width, rect.height)

        parent.connect("check-resize", self.__resize)

    def __resize(self, parent):
        rect = Gdk.Rectangle
        rect.width = self.ventana.get_allocated_width()
        rect.height = self.ventana.get_allocated_height()
        self.set_size_request(rect.width, rect.height)

    def stop(self):
        for visor in self.panel.players:
            visor.player.stop()


class Panel(Gtk.HPaned):

    def __init__(self, lectura):

        Gtk.HPaned.__init__(self)

        self.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse("#ffffff"))

        dirpath = False
        if lectura == "ciclo vital":
            dirpath = os.path.join(BASE_PATH, "Lecturas", "001-Ciclo-Vital")
        elif lectura == "muda de exoesqueleto":
            dirpath = os.path.join(BASE_PATH, "Lecturas", "002-Muda")
        elif lectura == "reproducción":
            dirpath = os.path.join(BASE_PATH, "Lecturas", "003-Reproducion")
        elif lectura == "plaga":
            dirpath = os.path.join(BASE_PATH, "Lecturas", "004-Plaga")
        elif lectura == "muerte":
            dirpath = os.path.join(BASE_PATH, "Lecturas", "005-Muerte")
        elif lectura == "lectura general":
            dirpath = os.path.join(BASE_PATH, "Lecturas", "General")
        elif lectura == "extinción":
            dirpath = os.path.join(BASE_PATH, "Lecturas", "Extincion")

        self.players = []
        vbox = Gtk.VBox()
        for archivo in sorted(os.listdir(dirpath)):
            tipo = describe_archivo(os.path.join(dirpath, archivo))
            if 'video' in tipo or 'application/ogg' in tipo or "image" in tipo:
                drawing = Visor(os.path.join(dirpath, archivo))
                self.players.append(drawing)
                vbox.pack_start(drawing, True, True, 0)

        self.pack1(vbox, resize=True, shrink=True)

        self.lectura = Gtk.TextView()
        self.lectura.set_editable(False)
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.POLICY_NEVER, Gtk.POLICY_AUTOMATIC)
        scroll.add(self.lectura)
        self.pack2(scroll, resize=False, shrink=False)

        path = os.path.join(dirpath, "lectura.txt")
        arch = open(path, "r")
        text = arch.read()
        arch.close()
        self.lectura.get_buffer().set_text(text)

        self.show_all()


class Visor(Gtk.DrawingArea):

    def __init__(self, archivo):

        Gtk.DrawingArea.__init__(self)

        self.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse("#ffffff"))

        self.archivo = archivo
        self.player = False

        self.connect("realize", self.__realize)

        self.show_all()

    def __realize(self, widget):
        tipo = describe_archivo(self.archivo)
        if "image" in tipo:
            self.player = ImagePlayer(self)
        elif 'video' in tipo or 'application/ogg':
            self.player = JAMediaReproductor(self.get_property('window').get_xid)
        GObject.idle_add(self.player.load, self.archivo)


class Cursor(Sprite):

    def __init__(self, tipo):

        Sprite.__init__(self)

        self.tipo = tipo

        path = ""
        if self.tipo == "agua":
            path = os.path.join(BASE_PATH, "Imagenes", "jarra.png")
        elif self.tipo == "alimento":
            path = os.path.join(BASE_PATH, "Imagenes", "pan.png")

        self.image = pygame.image.load(path)
        self.rect = self.image.get_bounding_rect()

    def pos(self, pos):
        self.rect.centerx = pos[0]
        self.rect.centery = pos[1]


class Alimento(Sprite):

    def __init__(self, tipo, pos):

        Sprite.__init__(self)

        self.tipo = tipo
        self.cantidad = 1500.0

        path = ""
        if self.tipo == "agua":
            path = os.path.join(BASE_PATH, "Imagenes", "jarra.png")
        elif self.tipo == "alimento":
            path = os.path.join(BASE_PATH, "Imagenes", "pan.png")

        self.image = pygame.image.load(path)
        self.rect = self.image.get_bounding_rect()
        self.rect.centerx = pos[0]
        self.rect.centery = pos[1]

    def update(self):
        if self.cantidad <= 0.0:
            self.kill()


class Toolbar(Gtk.EventBox):

    def __init__(self):

        Gtk.EventBox.__init__(self)

        toolbar = Gtk.Toolbar()

        self.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse("#ffffff"))
        toolbar.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse("#ffffff"))

        toolbar.insert(get_separador(draw=False, ancho=3, expand=False), -1)

        imagen = Gtk.Image()
        icono = os.path.join(BASE_PATH, "Imagenes", "cucaracha2.png")
        pixbuf = GdkPixbuf.Pixbuf.pixbuf_new_from_file_at_size(icono,
            -1, 24)
        imagen.set_from_pixbuf(pixbuf)
        imagen.show()
        item = Gtk.ToolItem()
        item.add(imagen)
        toolbar.insert(item, -1)

        item = Gtk.ToolItem()
        self.labelcucas = Gtk.Label(" 0H + 0M = 0")
        self.labelcucas.modify_fg(Gtk.StateType.NORMAL,
            Gdk.color_parse("#000000"))
        self.labelcucas.show()
        item.add(self.labelcucas)
        toolbar.insert(item, -1)

        toolbar.insert(get_separador(draw=False, ancho=3, expand=False), -1)

        imagen = Gtk.Image()
        icono = os.path.join(BASE_PATH, "Imagenes", "huevos.png")
        pixbuf = GdkPixbuf.Pixbuf.pixbuf_new_from_file_at_size(icono,
            -1, 24)
        imagen.set_from_pixbuf(pixbuf)
        imagen.show()
        item = Gtk.ToolItem()
        item.add(imagen)
        toolbar.insert(item, -1)

        item = Gtk.ToolItem()
        self.labelootecas = Gtk.Label(" = 0")
        self.labelootecas.modify_fg(Gtk.StateType.NORMAL,
            Gdk.color_parse("#000000"))
        self.labelootecas.show()
        item.add(self.labelootecas)
        toolbar.insert(item, -1)

        imagen = Gtk.Image()
        icono = os.path.join(BASE_PATH, "Imagenes", "jarra.png")
        pixbuf = GdkPixbuf.Pixbuf.pixbuf_new_from_file_at_size(icono, -1, 24)
        imagen.set_from_pixbuf(pixbuf)
        imagen.show()
        item = Gtk.ToolItem()
        item.add(imagen)
        toolbar.insert(item, -1)

        item = Gtk.ToolItem()
        self.labelagua = Gtk.Label(" = 0")
        self.labelagua.modify_fg(Gtk.StateType.NORMAL,
            Gdk.color_parse("#000000"))
        self.labelagua.show()
        item.add(self.labelagua)
        toolbar.insert(item, -1)

        toolbar.insert(get_separador(draw=False, ancho=3, expand=False), -1)

        imagen = Gtk.Image()
        icono = os.path.join(BASE_PATH, "Imagenes", "pan.png")
        pixbuf = GdkPixbuf.Pixbuf.pixbuf_new_from_file_at_size(icono, -1, 24)
        imagen.set_from_pixbuf(pixbuf)
        imagen.show()
        item = Gtk.ToolItem()
        item.add(imagen)
        toolbar.insert(item, -1)

        item = Gtk.ToolItem()
        self.labelalimento = Gtk.Label(" = 0")
        self.labelalimento.modify_fg(Gtk.StateType.NORMAL,
            Gdk.color_parse("#000000"))
        self.labelalimento.show()
        item.add(self.labelalimento)
        toolbar.insert(item, -1)

        toolbar.insert(get_separador(draw=False, ancho=3, expand=False), -1)

        item = Gtk.ToolItem()
        self.labeltiempo = Gtk.Label(" Años: 0 Dias: 0 Horas: 0")
        self.labeltiempo.modify_fg(Gtk.StateType.NORMAL,
            Gdk.color_parse("#000000"))
        self.labeltiempo.show()
        item.add(self.labeltiempo)
        toolbar.insert(item, -1)

        toolbar.insert(get_separador(draw=False, ancho=0, expand=True), -1)

        self.add(toolbar)
        self.show_all()

    def set_info(self, infocucas, infoootecas, infoagua, infoalimento, tiempo):
        self.labelcucas.set_text(infocucas)
        self.labelootecas.set_text(infoootecas)
        self.labelagua.set_text(infoagua)
        self.labelalimento.set_text(infoalimento)
        self.labeltiempo.set_text(tiempo)


class ToolbarEstado(Gtk.EventBox):

    __gsignals__ = {
    "volumen": (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_FLOAT, ))}

    def __init__(self):

        Gtk.EventBox.__init__(self)

        toolbar = Gtk.Toolbar()

        self.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse("#ffffff"))
        toolbar.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse("#ffffff"))

        toolbar.insert(get_separador(draw=False, ancho=3, expand=False), -1)

        item = Gtk.ToolItem()
        self.label = Gtk.Label()
        self.label.modify_fg(Gtk.StateType.NORMAL,
            Gdk.color_parse("#000000"))
        self.label.show()
        item.add(self.label)
        toolbar.insert(item, -1)

        toolbar.insert(get_separador(draw=False, ancho=0, expand=True), -1)

        item = Gtk.ToolItem()
        self.volumen = ControlVolumen()
        self.volumen.connect("value-changed", self.__value_changed)
        self.volumen.show()
        item.add(self.volumen)
        toolbar.insert(item, -1)

        toolbar.insert(get_separador(draw=False, ancho=3, expand=False), -1)

        self.add(toolbar)
        self.show_all()

    def __value_changed(self, widget, valor):
        self.emit('volumen', valor)

    def set_info(self, info):
        self.label.set_text(info)


class ControlVolumen(Gtk.VolumeButton):

    __gsignals__ = {
    "volumen": (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_FLOAT, ))}

    def __init__(self):

        Gtk.VolumeButton.__init__(self)

        self.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse("#ffffff"))

        self.connect("value-changed", self.__value_changed)
        self.show_all()

        self.set_value(0.1)

    def __value_changed(self, widget, valor):
        valor = int(valor * 10)
        self.emit('volumen', valor)
