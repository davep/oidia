"""The main screen of the application."""

##############################################################################
# Textual imports.
from textual.app     import ComposeResult
from textual.screen  import Screen
from textual.widgets import Header, Footer

##############################################################################
# Local imports.
from ..widgets import Timeline

##############################################################################
class Main( Screen ):
    """The main screen of the application."""

    DEFAULT_CSS = """
    TimelineTitle {
        background: $primary-background;
        border-right: vkey $secondary;
    }

    #header TimelineDay {
        background: $primary-background;
        border-right: vkey $secondary;
    }
    """
    """str: The styles for the main screen."""

    BINDINGS = [
        ( "left",  "move(-1)", "-1 day" ),
        ( "right", "move(1)",  "+1 day" ),
        ( "up",    "zoom(-1)", "In" ),
        ( "down",  "zoom(1)",  "Out" ),
    ]

    def compose( self ) -> ComposeResult:
        """Compose the content of the main screen.

        Args:
            ComposeResult: The result of composing the screen.
        """
        yield Header( show_clock=True )
        yield Timeline( id="header" )
        yield Footer()

    def action_move( self, days: int ) -> None:
        """Move the timeline.

        Args:
            days (int): The number of times to move the timeline by.
        """
        self.query_one( Timeline ).move_days( days )

    def action_zoom( self, days: int ) -> None:
        """Zoom the timeline.

        Args:
            days (int): The number of times to zoom the timeline by.
        """
        self.query_one( Timeline ).zoom_days( days )

### main.py ends here
