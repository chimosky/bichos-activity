#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   ImagePlayer.py por:
#   Flavio Danesse <fdanesse@gmail.com>
#   Uruguay

import os
import gi
from gi.repository import GObject
gi.require_version('Gst', '1.0')
from gi.repository import Gst

PR = False


class ImagePlayer(GObject.GObject):

    def __init__(self, ventana):

        GObject.GObject.__init__(self)

        self.ventana = ventana
        self.src_path = ""

        rect = self.ventana.get_allocation()
        self.width = rect.width
        self.height = rect.height

        self.xid = self.ventana.get_property('window').xid
        self.player = PlayerBin(self.xid, self.width, self.height)

        self.ventana.connect("expose-event", self.__set_size)

    def __set_size(self, widget, event):
        rect = self.ventana.get_allocation()
        self.width = rect.width
        self.height = rect.height

        rot = self.player.get_rotacion()
        if self.src_path:
            self.load(self.src_path)

        self.player.force_rotation(rot)

    def load(self, uri):
        self.src_path = uri

        if self.player:
            self.player.stop()
            del(self.player)
            self.player = False

        self.player = PlayerBin(self.xid, self.width, self.height)
        self.player.load(self.src_path)

    def rotar(self, valor):
        self.player.rotar(valor)

    def stop(self):
        self.player.stop()
        try:
            self.ventana.disconnect_by_func(self.__set_size)
        except:
            pass


class PlayerBin(GObject.GObject):

    def __init__(self, ventana_id, width, height):

        GObject.GObject.__init__(self)

        self.ventana_id = ventana_id
        self.player = None
        self.bus = None

        self.player = Gst.element_factory_make("playbin2", "player")
        self.video_bin = Video_Out(width, height)
        self.player.set_property('video-sink', self.video_bin)

        self.bus = self.player.get_bus()
        self.bus.add_signal_watch()
        self.bus.enable_sync_message_emission()
        self.bus.connect('sync-message', self.__sync_message)

    def __sync_message(self, bus, message):
        if message.type == Gst.MESSAGE_ELEMENT:
            if message.structure.get_name() == 'prepare-xwindow-id':
                message.src.set_xwindow_id(self.ventana_id)

        elif message.type == Gst.MESSAGE_ERROR:
            err, debug = message.parse_error()
            if PR:
                print "ImagePlayer ERROR:"
                print "\t%s" % err
                print "\t%s" % debug

    def __play(self):
        self.player.set_state(Gst.STATE_PLAYING)

    def rotar(self, valor):
        self.stop()
        self.video_bin.rotar(valor)
        self.__play()

    def get_rotacion(self):
        return self.video_bin.get_rotacion()

    def force_rotation(self, rot):
        self.video_bin.force_rotation(rot)

    def stop(self):
        self.player.set_state(Gst.STATE_NULL)

    def load(self, uri):
        self.stop()
        if not uri:
            return

        if os.path.exists(uri):
            direccion = "file://" + uri
            self.player.set_property("uri", direccion)
            self.__play()

        return False


class Video_Out(Gst.Pipeline):

    def __init__(self, width, height):

        Gst.Pipeline.__init__(self)

        self.set_name('video_out')

        imagefreeze = Gst.element_factory_make('imagefreeze', "imagefreeze")
        videoconvert = Gst.element_factory_make(
            'ffmpegcolorspace', 'ffmpegcolorspace')

        videoflip = Gst.element_factory_make('videoflip', "videoflip")
        caps = Gst.Caps(
            'video/x-raw-rgb,framerate=30/1,width=%s,height=%s' % (
            width, height))
        filtro = Gst.element_factory_make("capsfilter", "filtro")
        filtro.set_property("caps", caps)

        ximagesink = Gst.element_factory_make('ximagesink', "ximagesink")
        ximagesink.set_property("force-aspect-ratio", True)

        self.add(imagefreeze)
        self.add(videoconvert)
        self.add(videoflip)
        self.add(filtro)
        self.add(ximagesink)

        imagefreeze.link(videoconvert)
        videoconvert.link(videoflip)
        videoflip.link(filtro)
        filtro.link(ximagesink)

        self.ghost_pad = Gst.GhostPad(
            "sink", imagefreeze.get_static_pad("sink"))

        self.ghost_pad.set_target(imagefreeze.get_static_pad("sink"))

        self.add_pad(self.ghost_pad)

    def rotar(self, valor):
        videoflip = self.get_by_name("videoflip")
        rot = videoflip.get_property('method')
        if valor == "Derecha":
            if rot < 3:
                rot += 1

            else:
                rot = 0

        elif valor == "Izquierda":
            if rot > 0:
                rot -= 1

            else:
                rot = 3

        videoflip.set_property('method', rot)

    def force_rotation(self, rot):
        videoflip = self.get_by_name("videoflip")
        videoflip.set_property('method', rot)

    def get_rotacion(self):
        videoflip = self.get_by_name("videoflip")
        return videoflip.get_property('method')
