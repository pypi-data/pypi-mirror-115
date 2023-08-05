"""Base class for Git Fix states."""


class State:
    """Defines an individual state within the state machine."""

    def __init__(self, parent=None, options=None):
        """Initializes the State."""
        self.parent = parent
        self.options = options

    def parse_choice(self, event):
        """Parses the choice made by the user."""
        test = event.name
        if test == "KEY_LEFT":
            return "Parent"
        try:
            code = int(event)
        except ValueError:
            return None
        if not self.options or code >= len(self.options):
            return None
        else:
            return self.options[code]

    def on_event(self, event):
        """Handle events that are delegated to this State."""
        pass

    def __repr__(self):
        """Leverages the __str__ method to describe the State."""
        return self.__str__()

    def __str__(self):
        """Returns the name of the State."""
        return self.__class__.__name__
