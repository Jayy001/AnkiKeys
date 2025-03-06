from aqt.utils import tooltip
from aqt import mw

def add_shortcuts_note_type():
    """Add the 'AnkiKeys 1.0' note type if it doesn't already exist."""
    # Check if Anki is ready
    if not mw or not mw.col:
        return

    # Get the models/note types manager
    models = mw.col.models

    # Determine API version and use appropriate methods
    new_api = hasattr(models, "by_name")

    # Check if "AnkiKeys 1.0" already exists
    if new_api:
        existing_model = models.by_name("AnkiKeys 1.0")
    else:
        existing_model = models.byName("AnkiKeys 1.0")

    if existing_model:
        return

    # Create new note type
    model = models.new("AnkiKeys 1.0")

    # Add fields
    for field_name in ["Front", "Back"]:
        if new_api:
            field = models.new_field(field_name)
            models.add_field(model, field)
        else:
            field = models.newField(field_name)
            models.addField(model, field)

    # Add template
    if new_api:
        template = models.new_template("Card 1")
    else:
        template = models.newTemplate("Card 1")

    with open(f"{__file__[:-7]}/web/front.html") as front:
        template["qfmt"] = front.read()

    with open(f"{__file__[:-7]}/web/back.html") as back:
        template["afmt"] = back.read()

    if new_api:
        models.add_template(model, template)
    else:
        models.addTemplate(model, template)

    with open(f"{__file__[:-7]}/web/style.css") as style:
        model["css"] = style.read()

    # Save model - try different method names for compatibility

    try:
        models.add(model)
    except AttributeError:
        try:
            models.save(model)
        except AttributeError:
            # Older versions might use update
            models.update(model)

    tooltip("'AnkiKeys 1.0' note type has been added successfully!")
