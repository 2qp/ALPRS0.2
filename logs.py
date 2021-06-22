import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk as gtk
import os
import sqlite3
import numpy

conn = sqlite3.connect('stu3.db')
c = conn.cursor()



class WB_Window(gtk.Window):
    def __init__(self):
        gtk.Window.__init__(self, title="Logs")
        self.set_border_width(10)
        self.set_position(gtk.WindowPosition.CENTER)
        self.set_default_size(300, 450)

        #self.outter_box = gtk.Box(gtk.Orientation.HORIZONTAL, spacing=10)
        self.outter_box = gtk.VBox(False,spacing=10)
        self.add(self.outter_box)
        
        c.execute("select * from Logs")
        software_list = c.fetchall()
        self.software_liststore = gtk.ListStore(str, str, int)
        for software_ref in software_list:
            self.software_liststore.append(list(software_ref))
		
        self.tree = gtk.TreeView(self.software_liststore)
        self.tree_selection = self.tree.get_selection()
        self.tree_selection.connect("changed", self.onSelectionChanged)
        
        for i, column_title in enumerate(["Plate", "Entry Time", "Inside"]):
            renderer = gtk.CellRendererText()
            column = gtk.TreeViewColumn(column_title, renderer, text=i)
            self.tree.append_column(column)

        self.scrollable_treelist = gtk.ScrolledWindow()
        self.scrollable_treelist.set_vexpand(True)
        self.scrollable_treelist.set_hexpand(True)
        self.outter_box.pack_start(self.scrollable_treelist, False, True, 0)
        self.scrollable_treelist.add(self.tree)
        
        
        hbox2 = gtk.Box(gtk.Orientation.HORIZONTAL)
        self.outter_box.pack_start(hbox2, False, False, 0)
        #hbox2.set_layout(gtk.CENTER)
        self.entryid = gtk.Entry()
        self.entry = gtk.Entry()
        self.entry2 = gtk.Entry()
        hbox2.add(self.entry)
        hbox2.add(self.entry2)

        hbox = gtk.ButtonBox.new(gtk.Orientation.HORIZONTAL)
        hbox.set_layout(gtk.ButtonBoxStyle.CENTER) 
        self.outter_box.pack_start(hbox, False, True, 0)
        

        # Add CSS "linked" class
        hbox.get_style_context().add_class("linked")
        
        button_add = gtk.Button(label="Add")
        hbox.add(button_add)
        button_add.connect("clicked", self.add_btn_clicked)
        
        button_update = gtk.Button(label="Update")
        hbox.add(button_update)
        button_update.connect("clicked", self.update_btn_clicked)
        
        button_remove = gtk.Button(label="Remove")
        hbox.add(button_remove)
        button_remove.connect("clicked", self.remove_btn_clicked)
        
        button_quit = gtk.Button(label="Quit",stock=gtk.STOCK_QUIT)
        button_quit.show()
        hbox.add(button_quit)
        button_quit.connect("clicked", self.on_close_clicked)
        
        button_refresh = gtk.Button(label="Refresh")
        hbox.add(button_refresh)
        button_refresh.connect("clicked", self.refresh_btn_clicked)
        

    def onSelectionChanged(self, tree_selection) :
        (model, pathlist) = self.tree_selection.get_selected_rows()
        for path in pathlist:
           tree_iter = model.get_iter(path)
           self.ids = model.get_value(tree_iter,0)
           value = model.get_value(tree_iter,1)
           value2 = model.get_value(tree_iter,2)
           self.entry.set_text(value)
           self.entry2.set_text(value2)
        #return self.ids
		

        
        
    def add_btn_clicked(self, button_add):
        get_user = self.entry.get_text()
        get_plate = self.entry2.get_text()
        data_input = '''INSERT INTO NP(user,plate) VALUES(?,?);'''

        data_tuple = (get_user, get_plate)
        c.execute(data_input, data_tuple)
        conn.commit()
        
    def remove_btn_clicked(self, button_remove):
		
		get_ids = self.ids
		
		query = '''DELETE from NP where id = ?'''
		c.execute(query, (get_ids,))
		conn.commit()
		print(get_ids)
		
    def update_btn_clicked(self, button_update):
        get_ids = self.ids
        get_user = self.entry.get_text()
        get_plate = self.entry2.get_text()
        query = ''' UPDATE NP SET user = ? , plate = ? WHERE id = ?'''
        data_tuple = (get_user, get_plate, get_ids)
        c.execute(query, data_tuple)
        conn.commit()
        
    def on_close_clicked(self, button_quit):
        print("Closing Logs")
        gtk.main_quit()
        
    def refresh_btn_clicked(self, button_quit):
		
        #self.software_liststore.clear()
        c.execute("select * from logs")
        software_list = c.fetchall()
        self.software_liststore = gtk.ListStore(str, str, int)
        for software_ref in software_list:
            self.software_liststore.append(list(software_ref))
        
        self.tree.set_model(self.software_liststore)

win = WB_Window()
win.connect("delete-event",gtk.main_quit)
win.show_all()
gtk.main() 
