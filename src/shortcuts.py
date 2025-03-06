from PyQt6.QtCore import Qt, QObject, QEvent
from PyQt6.QtGui import QKeyEvent

from aqt import mw
from aqt.qt import *
from aqt.reviewer import Reviewer

original_reviewer_shortcut_keys = Reviewer._shortcutKeys
original_shortcuts = {}
original_reviewer_scuts = None


def disable_shortcuts():
    Reviewer._shortcutKeys = lambda self: []

    for shortcut in mw.findChildren(QShortcut):
        original_shortcuts[shortcut] = shortcut.key()
        shortcut.setKey(QKeySequence(""))

    # Save and disable QAction shortcuts
    for action in mw.findChildren(QAction):
        if action.shortcuts():
            original_shortcuts[action] = action.shortcuts()
            action.setShortcuts([])


def enable_shortcuts():
    """Re-enable all shortcuts in Anki"""
    global original_shortcuts, original_reviewer_shortcut_keys
    Reviewer._shortcutKeys = lambda self: original_reviewer_shortcut_keys(self)

    # Restore QShortcuts and QActions
    for obj, key_data in original_shortcuts.items():
        if not sip.isdeleted(obj):  # Check if object still exists
            if isinstance(obj, QShortcut):
                obj.setKey(key_data)
            else:
                obj.setShortcuts(key_data)

    # Restore reviewer shortcuts
    if original_reviewer_scuts:
        Reviewer._shortcutKeys = original_reviewer_scuts

    original_shortcuts = {}
