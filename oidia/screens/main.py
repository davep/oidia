"""The main screen of the application."""

##############################################################################
# Textual imports.
from textual.app        import ComposeResult
from textual.screen     import Screen
from textual.widgets    import Header, Footer
from textual.containers import Vertical
from textual.binding    import Binding

##############################################################################
# Local imports.
from ..widgets import Timeline, StreakLine

##############################################################################
class Main( Screen ):
    """The main screen of the application."""

    DEFAULT_CSS = """
    Timeline {
        height: 3;
    }

    Timeline TimelineTitle, TimelineDay {
        background: $primary-background;
        border-right: vkey $secondary;
    }

    StreakLine TimelineTitle, StreakDay {
        background: $primary-background-darken-1;
    }
    """
    """str: The styles for the main screen."""

    BINDINGS = [
        Binding( "left",                 "move(-1)", "< day" ),
        Binding( "right",                "move(1)",  "> day" ),
        Binding( "left_square_bracket",  "zoom(-1)", "Zoom In" ),
        Binding( "right_square_bracket", "zoom(1)",  "Zoom Out" ),
        Binding( "a",                    "add",      "Add Streak" ),
        Binding( "escape",               "app.quit", "Quit" )
    ]
    """list[ Binding ]: The bindings for the main screen."""

    def compose( self ) -> ComposeResult:
        """Compose the content of the main screen.

        Args:
            ComposeResult: The result of composing the screen.
        """
        yield Header( show_clock=True )
        yield Vertical( Timeline( id="header" ), id="streaks" )
        yield Footer()

    def action_move( self, days: int ) -> None:
        """Move the timeline.

        Args:
            days (int): The number of times to move the timeline by.
        """
        for timeline in self.query( Timeline ):
            timeline.move_days( days )

    def action_zoom( self, days: int ) -> None:
        """Zoom the timeline.

        Args:
            days (int): The number of times to zoom the timeline by.
        """
        for timeline in self.query( Timeline ):
            timeline.zoom_days( days )

    def action_add( self ) -> None:
        """Add a new timeline to the display."""
        # TODO: For now this just adds one and does nothing else special
        # with it. We're just testing what happens.
        self.query_one( "#streaks", Vertical ).mount( StreakLine() )

### main.py ends here
