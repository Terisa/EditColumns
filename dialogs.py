#!/usr/bin/env python
# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai
from __future__ import (unicode_literals, division, absolute_import,
                        print_function)
import six

__license__   = 'GPL v3'
__copyright__ = '2011, Grant Drake <grant.drake@gmail.com>'
__docformat__ = 'restructuredtext en'

import os, traceback
from collections import OrderedDict
try:
    from PyQt5.Qt import Qt, QVBoxLayout, QDialogButtonBox, QGroupBox, QGridLayout, QCheckBox
except ImportError:
    from PyQt4.Qt import Qt, QVBoxLayout, QDialogButtonBox, QGroupBox, QGridLayout, QCheckBox

from calibre.gui2 import warning_dialog

from calibre_plugins.edit_columns.common_utils import (SizePersistedDialog, ImageTitleLayout, debug_print)

DIALOG_NAME = 'Edit Columns'


class UpdateCustomColsDialog(SizePersistedDialog):

    def __init__(self, parent, plugin_action):
        SizePersistedDialog.__init__(self, parent, 'edit columns plugin:update custom columns dialog')
        self.plugin_action = plugin_action
        self.help_anchor   = "UpdateCustomCols"

        self.custom_cols = self.get_custom_columns ()
        self.db = self.plugin_action.gui.library_view.model().db
        
        self.initialize_controls()
        self.restart = False
        
        
    def initialize_controls(self):
        self.setWindowTitle(DIALOG_NAME)
        layout = QVBoxLayout(self)
        self.setLayout(layout)
        title_layout = ImageTitleLayout(self, 'images/icon.png', 'Update custom columns in Library')
        layout.addLayout(title_layout)

        column_group = QGroupBox(_("Columns to update"), self)
        layout.addWidget(column_group)
        column_layout = QGridLayout()
        column_group.setLayout(column_layout)

        pos = 0
        self.checkbox = {}
        for key in sorted (self.custom_cols):
            value = self.custom_cols[key]
            self.checkbox[key] = self.createCheckbox (value)
            column_layout.addWidget(self.checkbox[key], int ((pos / 2)), int ((pos % 2)* 2 + 1), 1, 1)
            pos = pos + 1
            
        layout.addStretch(1)

        # Dialog buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.ok_clicked)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def ok_clicked(self):
    
        #debug_print ("Columns: ", self.custom_cols)

        for key, checkbox in six.iteritems(self.checkbox):
            col = self.custom_cols[key]
            #aux = checkbox.checkState == Qt.Checked
            aux = checkbox.isChecked ()
            
            debug_print (key, "[", col['datatype'], "]: ", checkbox.isChecked())
            
            if (aux != col['is_editable']):
                debug_print ("Modificando ", col['name'])
                self.db.set_custom_column_metadata (col['colnum'], is_editable=aux)
                self.restart = True
            else:
                debug_print (col['name'], ": ", aux)
            
        self.accept()

    def get_custom_columns(self):
        column_types = ['composite', '*composite']
        custom_columns = self.plugin_action.gui.library_view.model().custom_columns
        available_columns = {}
        for key, column in six.iteritems(custom_columns):
            typ = column['datatype']
            if typ not in column_types:
                available_columns[key] = column
                
            # Include type, name (header, long name), is_multiple, display, is_editable
            #'label':record[0],
            #        'name':record[1],
            #        'datatype':record[2],
            #        'editable':bool(record[3]),
            #        'display':json.loads(record[4]),
            #        'normalized':bool(record[5]),
            #        'colnum':record[6],
            #        'is_multiple':bool(record[7]),
            
            # Modificar: set_custom_column_data
        return available_columns

    def createCheckbox (self, column):
        checkbox = QCheckBox(column['name'], self)
        checkbox.setChecked(column['is_editable'])

        return checkbox