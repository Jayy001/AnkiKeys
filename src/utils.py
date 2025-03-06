from aqt import mw

def is_correct(keys):
    try:
        answer = mw.reviewer.card.note()["Back"]
    except:
        return "0"

    given = " ".join(keys)

    # Normalize and compare the two formats
    return str(int(parse_human_format(answer) == parse_js_format(given)))


def parse_human_format(text):
    """Parse human-readable keyboard shortcut into normalized form."""

    keys = text.strip().split()
    normalized_combination = []

    for key in keys:
        normalized_key = normalize_human_key(key)

        if normalized_key:
            normalized_combination.append(normalized_key)

    return " ".join(normalized_combination)


def normalize_human_key(key):
    # Modifier keys
    if key.lower() == "ctrl":
        return "Control"
    elif key.lower() == "alt":
        return "Alt"
    elif key.lower() == "shift":
        return "Shift"
    elif key.lower() in ("win", "super", "cmd"):
        return "Meta"

    # Single alphanumeric characters
    elif len(key) == 1 and key.isalpha():
        return f"Key{key.upper()}"
    elif len(key) == 1 and key.isdigit():
        return f"Digit{key}"

    # Special characters mapping
    special_char_map = {
        "[": "BracketLeft",
        "]": "BracketRight",
        "{": "BraceLeft",
        "}": "BraceRight",
        "(": "ParenthesisLeft",
        ")": "ParenthesisRight",
        "<": "LessThan",
        ">": "GreaterThan",
        "-": "Minus",
        "+": "Plus",
        "=": "Equal",
        ".": "Period",
        ",": "Comma",
        "/": "Slash",
        "\\": "Backslash",
        ";": "Semicolon",
        "'": "Quote",
        '"': "DoubleQuote",
        ":": "Colon",
        "?": "QuestionMark",
        "!": "ExclamationMark",
        "@": "At",
        "#": "Hash",
        "$": "Dollar",
        "%": "Percent",
        "^": "Caret",
        "&": "Ampersand",
        "*": "Asterisk",
        "_": "Underscore",
        "~": "Tilde",
        "`": "Backquote",
        "|": "Pipe",
        " ": "Space",
    }

    if key in special_char_map:
        return special_char_map[key]

    # Function keys
    if key.upper().startswith("F") and key[1:].isdigit():
        return f"F{key[1:]}"

    # Other standard keys
    key_map = {
        "esc": "Escape",
        "escape": "Escape",
        "tab": "Tab",
        "caps": "CapsLock",
        "capslock": "CapsLock",
        "enter": "Enter",
        "return": "Enter",
        "backspace": "Backspace",
        "space": "Space",
        "spacebar": "Space",
        "ins": "Insert",
        "insert": "Insert",
        "del": "Delete",
        "delete": "Delete",
        "home": "Home",
        "end": "End",
        "pageup": "PageUp",
        "pgup": "PageUp",
        "pagedown": "PageDown",
        "pgdn": "PageDown",
        "up": "ArrowUp",
        "down": "ArrowDown",
        "left": "ArrowLeft",
        "right": "ArrowRight",
        "prtsc": "PrintScreen",
        "print": "PrintScreen",
        "printscreen": "PrintScreen",
        "scroll": "ScrollLock",
        "scrolllock": "ScrollLock",
        "pause": "Pause",
        "break": "Pause",
        "num": "NumLock",
        "numlock": "NumLock",
    }

    return key_map.get(key.lower(), key)


def parse_js_format(text):
    # Split the text into individual keys
    js_keys = text.strip().split()

    # Normalize each key (removing Left/Right from modifiers)
    normalized_keys = []
    for key in js_keys:
        # Strip direction indicators (Left/Right) from modifiers
        if key.startswith("Control"):
            normalized_keys.append("Control")
        elif key.startswith("Alt"):
            normalized_keys.append("Alt")
        elif key.startswith("Shift"):
            normalized_keys.append("Shift")
        elif key.startswith("Meta"):
            normalized_keys.append("Meta")
        else:
            normalized_keys.append(key)

    return " ".join(normalized_keys)
