from aqt import gui_hooks
from anki.hooks import wrap, addHook

from .utils import *
from .shortcuts import *
from .note import *

keys = []

def hook(handled, message, context):
    global keys

    if f"ShortcutAddon:" not in message:
        return handled

    elif "Health" in message:
        return (True, "OK")

    elif "DisableKeyboard" in message:
        disable_shortcuts()

    elif "AddKey" in message:
        if mw.reviewer.state == "answer":
            return (True, "-1")

        keys.append(message.split("ShortcutAddon: AddKey ")[-1])

        return (True, str(len(keys)))

    elif "RemoveKey" in message:
        if mw.reviewer.state == "answer":
            return (True, "-1")

        try:
            keys.pop()
        except:
            pass

        return (True, str(len(keys)))

    elif "Reset" in message:
        keys = []
        return (True, None)

    elif "AnswerCard" in message:
        mw.reviewer._showAnswer()

    elif "EnableKeyboard" in message:
        enable_shortcuts()

    elif "LoadKeys" in message:
        return (True, " ".join(keys))

    elif "CheckAnswer" in message:
        return (True, is_correct(keys))

    return (True, None)


def on_state_change(state, oldstate):
    if state != "review":
        enable_shortcuts()


gui_hooks.webview_did_receive_js_message.append(hook)
addHook("profileLoaded", add_shortcuts_note_type)
addHook("beforeStateChange", on_state_change)
