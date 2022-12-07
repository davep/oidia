"""The main screen of the application."""

##############################################################################
# Textual imports.
from textual.app        import ComposeResult
from textual.css.query  import NoMatches
from textual.screen     import Screen
from textual.widgets    import Header, Footer, Input
from textual.containers import Vertical
from textual.binding    import Binding
from textual.events     import Click

##############################################################################
# Local imports.
from ..widgets import TimelineTitle, Timeline, StreakLine, StreakDay, TitleInput

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

    TimelineTitle {
        padding-left: 2;
        content-align: left middle;
    }

    StreakLine:focus-within TimelineTitle {
        text-style: bold;
        border-left: wide $secondary;
        padding-left: 1;
    }

    StreakLine:focus-within StreakDay {
        text-style: bold;
    }

    StreakDay.done {
        background: green;
    }

    StreakDay:focus {
        background: $primary-background-lighten-1;
    }

    StreakDay.done:focus {
        color: darkgreen;
        background: lightgreen;
    }
    """
    """str: The styles for the main screen."""

    BINDINGS = [
        Binding( "left",                 "focus_previous", "", show=False ),
        Binding( "right",                "focus_next", "", show=False ),
        Binding( "comma",                "move(-1)", "< day" ),
        Binding( "full_stop",            "move(1)",  "> day" ),
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

    def action_focus_previous( self ) -> None:
        """Action wrapper for moving focus to the previous widget."""
        self.focus_previous()

    def action_focus_next( self ) -> None:
        """Action wrapper for moving focus to the next widget."""
        self.focus_next()

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

    async def action_add( self ) -> None:
        """Add a new timeline to the display."""
        await self.query_one( "#streaks", Vertical ).mount( input := TitleInput( placeholder="Title", id="streak-add" ) )
        input.focus()

    async def on_input_submitted( self, event: Input.Submitted ) -> None:
        """Handle the user submitting input.

        Args:
            event (TitleInput.Submitted): The submit event.
        """

        # We're going to remove the input, so let's get its content before
        # we do that.
        title = event.input.value.strip()

        # Now let's remove the input box.
        await event.input.remove()

        # If the user entered a title...
        if title:
            # ...add a new timeline associated with it.
            await self.query_one( "#streaks", Vertical ).mount( line := StreakLine() )
            line.title = title
            line.query( StreakDay ).last().focus()

### main.py ends here
