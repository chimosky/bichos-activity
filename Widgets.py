#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gtk
from gi.repository import GObject
from gi.repository import gdk

from EventTraductor.EventTraductor import MousemotionTraduce
from EventTraductor.EventTraductor import Traduce_button_press_event
from EventTraductor.EventTraductor import Traduce_button_release_event


class Escenario(gtk.DrawingArea):

    __gsignals__ = {
    "new-size": (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT, )),
    "mouse-enter": (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_BOOLEAN, ))}

    def __init__(self):

        gtk.DrawingArea.__init__(self)

        self.modify_bg(gtk.StateType.NORMAL, gdk.color_parse("#000000"))

        self.set_events(gdk.EventType.EXPOSE |
            #gdk.KEY_PRESS | gtk.gdk.KEY_RELEASE |
            #gdk.KEY_RELEASE_MASK | gdk.KEY_PRESS_MASK |
            gdk.EventMask.POINTER_MOTION_MASK | gdk.EventMask.POINTER_MOTION_HINT_MASK |
            gdk.EventMask.BUTTON_MOTION_MASK | gdk.EventMask.BUTTON_PRESS_MASK |
            gdk.EventMask.BUTTON_RELEASE_MASK | gdk.EventMask.LEAVE_NOTIFY_MASK
            | gdk.EventMask.ENTER_NOTIFY_MASK)

        self.connect("size-allocate", self.__size_request)
        self.connect("expose-event", self.__redraw)

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
                Traduce_button_press_event(event,
                    self.get_allocation(),
                    self.get_toplevel().juego.RESOLUCION_INICIAL)
        except:
            # Para Sugar
            if self.get_toplevel().interfaz.juego:
                Traduce_button_press_event(event,
                    self.get_allocation(),
                    self.get_toplevel().interfaz.juego.RESOLUCION_INICIAL)

        return False

    def __button_release_event(self, widget, event):
        try:
            if self.get_toplevel().juego:
                Traduce_button_release_event(event,
                    self.get_allocation(),
                    self.get_toplevel().juego.RESOLUCION_INICIAL)
        except:
            # Para Sugar
            if self.get_toplevel().interfaz.juego:
                Traduce_button_release_event(event,
                    self.get_allocation(),
                    self.get_toplevel().interfaz.juego.RESOLUCION_INICIAL)
        return False

    def __mouse_motion(self, widget, event):
        try:
            if self.get_toplevel().juego:
                MousemotionTraduce(event,
                    self.get_allocation(),
                    self.get_toplevel().juego.RESOLUCION_INICIAL)
        except:
            # Para Sugar
            if self.get_toplevel().interfaz.juego:
                MousemotionTraduce(event,
                    self.get_allocation(),
                    self.get_toplevel().interfaz.juego.RESOLUCION_INICIAL)
        return False

    def __size_request(self, widget, event):
        rect = self.get_allocation()
        self.emit("new-size", (rect.width, rect.height))

    def __redraw(self, widget, event):
        rect = self.get_allocation()
        self.emit("new-size", (rect.width, rect.height))
