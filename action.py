#!/usr/bin/env python
# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai
from __future__ import (unicode_literals, division, absolute_import,
                        print_function)
from datetime import datetime


__copyright__ = '2015, Terisa de Morgan <terisam@gmail.com>'
__docformat__ = 'restructuredtext en'

from functools import partial
try:
    from PyQt5.Qt import (Qt, QWidget, QGridLayout, QLabel, QPushButton, QUrl,
                          QGroupBox, QComboBox, QVBoxLayout, QCheckBox,
                          QLineEdit, QToolButton, QModelIndex)
except ImportError:
    from PyQt4.Qt import (Qt, QWidget, QGridLayout, QLabel, QPushButton, QUrl,
                          QGroupBox, QComboBox, QVBoxLayout, QCheckBox,
                          QLineEdit, QToolButton)

from calibre.ebooks.metadata.book.base import Metadata
from calibre.gui2 import (question_dialog, Dispatcher, error_dialog, show_restart_warning)
from calibre.gui2.actions import InterfaceAction
from calibre.gui2.dialogs.message_box import ErrorNotification
from calibre.gui2 import question_dialog
from calibre.gui2.dialogs.progress import ProgressDialog
from contextlib import closing
from calibre.utils.date import now, UNDEFINED_DATE, DEFAULT_DATE, EPOCH
from calibre.utils.config import prefs, tweaks
from calibre.customize.ui import plugin_for_input_format
from calibre.db.legacy import LibraryDatabase

from calibre_plugins.edit_columns.common_utils import (set_plugin_icon_resources, get_icon, debug_print)
from calibre_plugins.edit_columns.dialogs import (UpdateCustomColsDialog)

from calibre.ebooks.metadata.book.base import Metadata
from calibre.library import current_library_name

import os
import time
import sys

PLUGIN_ICONS = ['images/icon.png']

try:
    debug_print("EditColumns::action.py - loading translations")
    load_translations()
except NameError:
    debug_print("EditColumns::action.py - exception when loading translations")
    pass # load_translations() added in calibre 1.9
    
class EditColumnsAction(InterfaceAction):

    name = 'Edit Columns'
    # Create our top-level menu/toolbar action (text, icon_path, tooltip, keyboard shortcut)
    action_spec = ('Edit Columns', None, _('Make custom columns editable / not editable'), 'Alt+Shift+E')
    dont_add_to = frozenset(['context-menu-device'])
    

    def genesis(self):
        icon_resources = self.load_resources(PLUGIN_ICONS)
        set_plugin_icon_resources(self.name, icon_resources)

        # Assign our menu to this action and an icon
        self.qaction.setIcon(get_icon(PLUGIN_ICONS[0]))
        self.qaction.triggered.connect(self.show_custom_cols)

    def show_custom_cols (self):
    
        dlg = UpdateCustomColsDialog(self.gui, self)
        dlg.exec_()
        if dlg.restart:
            do_restart = show_restart_warning (_('Restart calibre for the changes to the custom columns to be applied.'))
            if do_restart:
                self.gui.quit (restart=True)
        else:
            return
