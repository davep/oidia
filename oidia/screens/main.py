"""The main screen of the application."""

##############################################################################
# Textual imports.
from textual.app     import ComposeResult
from textual.screen  import Screen
from textual.widgets import Header, Footer

##############################################################################
class Main( Screen ):
    """The main screen of the application."""

    def compose( self ) -> ComposeResult:
        """Compose the content of the main screen.

        Args:
            ComposeResult: The result of composing the screen.
        """
        yield Header()
        yield Footer()

### main.py ends here
