#!/usr/bin/python
# -*- coding: utf-8 -*-

from atop_parser import atopStore

import gtk

import time

class MyWindow(gtk.Window):

  def __init__(self):
    gtk.Window.__init__(self)

    self.set_border_width(10)
    self.set_title("atop-plot")

    self.grid = gtk.Table()
    self.grid.set_col_spacings(5)
    self.grid.set_row_spacings(5)
    self.add(self.grid)

    self.file_label = gtk.Label("File")
    self.grid.attach(self.file_label, 0, 1, 0, 1, gtk.FILL, gtk.FILL)

    self.load_button = gtk.FileChooserButton("Select A File", None)
    self.load_button.connect("file-set", self.file_selected)
    self.grid.attach(self.load_button, 1, 2, 0, 1, gtk.FILL, gtk.FILL)

    self.label_label = gtk.Label("Label")
    self.grid.attach(self.label_label, 2, 3, 0, 1, gtk.FILL, gtk.FILL)

    self.label_combo = gtk.combo_box_new_text()
    self.label_combo.set_sensitive(False)
    self.label_combo.connect("changed", self.on_label_combo_changed)
    self.grid.attach(self.label_combo, 3, 4, 0, 1, gtk.FILL, gtk.FILL)

    self.pid_label = gtk.Label("PID")
    self.grid.attach(self.pid_label, 4, 5, 0, 1, gtk.FILL, gtk.FILL)

    self.pid_combo = gtk.combo_box_new_text()
    self.pid_combo.set_sensitive(False)
    self.pid_combo.connect("changed", self.on_pid_combo_changed)
    self.grid.attach(self.pid_combo, 5, 6, 0, 1, gtk.FILL, gtk.FILL)

  def file_selected(self, widget):
    self.store = atopStore(widget.get_filename())
    self.label_combo.append_text("PRC")
    self.label_combo.set_sensitive(True)

  def on_label_combo_changed(self, combo):
    key = self.label_combo.get_active_text()
    self.store = getattr(self.store, "series_" + key)

    sensitive = key.startswith("PR")
    if sensitive:
      for pid in self.store.keys():
        self.pid_combo.append_text(pid)
    self.pid_combo.set_sensitive(sensitive)

  def on_pid_combo_changed(self, combo):
    key = self.pid_combo.get_active_text()
    print self.store[key]

win = MyWindow()
win.connect("delete-event", gtk.main_quit)
win.show_all()
gtk.main()

