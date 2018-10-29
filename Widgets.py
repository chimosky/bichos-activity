#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import GObject
from gi.repository import Gdk

from EventTraductor.EventTraductor import MousemotionTraduce
from EventTraductor.EventTraductor import Traduce_button_press_event
from EventTraductor.EventTraductor import Traduce_button_release_event


class Escenario(Gtk.DrawingArea):

    __gsignals__ = {
    "new-size": (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT, )),
    "mouse-enter": (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_BOOLEAN, ))}

    def __init__(self):

        Gtk.DrawingArea.__init__(self)

        self.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse("#000000"))

        self.set_events(Gdk.EventType.EXPOSE |
            #Gdk.KEY_PRESS | Gdk.KEY_RELEASE |
            #Gdk.KEY_RELEASE_MASK | Gdk.KEY_PRESS_MASK |
            Gdk.EventMask.POINTER_MOTION_MASK | Gdk.EventMask.POINTER_MOTION_HINT_MASK |
            Gdk.EventMask.BUTTON_MOTION_MASK | Gdk.EventMask.BUTTON_PRESS_MASK |
            Gdk.EventMask.BUTTON_RELEASE_MASK | Gdk.EventMask.LEAVE_NOTIFY_MASK
            | Gdk.EventMask.ENTER_NOTIFY_MASK)

        self.connect("size-allocate", self.__size_request)
        self.connect('draw', self.__redraw)

        self.connect("button_press_event", self.__button_press_event)
        self.connect("button_release_event", self.__button_release_event)
        self.connect("motion-notify-event", self.__mouse_motion)
        self.connect("enter-notify-event", self.__mouse_enter)
        self.connect("leave-notify-event", self.__mouse_leave)

        self.show_all()

    def __mouse_enter(self, widget, event):
        self.emit("mouse-enter", True)

    def __mouse_leave(self, widget, event):
        self.emit("mouse-enter", False)

    def __button_press_event(self, widget, event):
        try:
            if self.get_toplevel().juego:
                rect = Gdk.Rectangle
                rect.width = self.get_allocated_width()
                rect.height = self.get_allocated_height()
                Traduce_button_press_event(event,
                    rect,
                    self.get_toplevel().juego.RESOLUCION_INICIAL)
        except:
            # Para Sugar
            if self.get_toplevel().interfaz.juego:
                rect = Gdk.Rectangle
                rect.width = self.get_allocated_width()
                rect.height = self.get_allocated_height()
                Traduce_button_press_event(event,
                    rect,
                    self.get_toplevel().interfaz.juego.RESOLUCION_INICIAL)

        return False

    def __button_release_event(self, widget, event):
        try:
            if self.get_toplevel().juego:
                rect = Gdk.Rectangle
                rect.width = self.get_allocated_width()
                rect.height = self.get_allocated_height()
                Traduce_button_release_event(event,
                    rect,
                    self.get_toplevel().juego.RESOLUCION_INICIAL)
        except:
            # Para Sugar
            if self.get_toplevel().interfaz.juego:
                rect = Gdk.Rectangle
                rect.width = self.get_allocated_width()
                rect.height = self.get_allocated_height()
                Traduce_button_release_event(event,
                    rect,
                    self.get_toplevel().interfaz.juego.RESOLUCION_INICIAL)
        return False

    def __mouse_motion(self, widget, event):
        try:
            if self.get_toplevel().juego:
                rect = Gdk.Rectangle
                rect.width = self.get_allocated_width()
                rect.height = self.get_allocated_height()
                MousemotionTraduce(event,
                    rect,
                    self.get_toplevel().juego.RESOLUCION_INICIAL)
        except:
            # Para Sugar
            if self.get_toplevel().interfaz.juego:
                rect = Gdk.Rectangle
                rect.width = self.get_allocated_width()
                rect.height = self.get_allocated_height()
                MousemotionTraduce(event,
                    rect,
                    self.get_toplevel().interfaz.juego.RESOLUCION_INICIAL)
        return False

    def __size_request(self, widget, event):
        rect = Gdk.Rectangle
        rect.width = self.get_allocated_width()
        rect.height = self.get_allocated_height()
        self.emit("new-size", (rect.width, rect.height))

    def __redraw(self, widget, event):
        rect = Gdk.Rectangle
        rect.width = self.get_allocated_width()
        rect.height = self.get_allocated_height()
        self.emit("new-size", (rect.width, rect.height))
