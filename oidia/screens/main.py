"""The main screen of the application."""

##############################################################################
# Textual imports.
from textual.app        import ComposeResult
from textual.screen     import Screen
from textual.widgets    import Header, Footer, Input
from textual.containers import Vertical
from textual.binding    import Binding

##############################################################################
# Local imports.
from ..widgets import Timeline, StreakLine

##############################################################################
class TitleInput( Input ):
    """Widget for inputting a title."""

    DEFAULT_CSS = """
    TitleInput:focus {
        border-left: none;
        border-right: none;
        width: 25;
    }
    """
    """str: The styles for the title input widget."""

    BINDINGS = [
        # In 0.5.0 at least there's no reasonable method inheriting bindings
        # and adding to them. So for now we do a sneaky splice... Annoyingly
        # though this is throwing up type warnings, but I'll run with it for
        # now. I'm told that `main` (what will be 0.6.0) addresses this.
        *Input.BINDINGS,
        Binding( "escape", "cancel", "Cancel add" )
    ]
    """list[ Binding ]: The bindings for the title input widget."""

    async def action_cancel( self ) -> None:
        """Provide a cancel action.

        Note:
            This empties the input and then performs the normal submit. It
            is expected that the user of the class will check the input and
            take an empty value to mean the input was cancelled.
        """
        self.value = ""
        await self.action_submit()

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

    async def action_add( self ) -> None:
        """Add a new timeline to the display."""
        await self.query_one( "#streaks", Vertical ).mount( input := TitleInput( placeholder="Title" ) )
        input.focus()

    def on_input_submitted( self, event: Input.Submitted ) -> None:
        """Handle the user submitting input.

        Args:
            event (TitleInput.Submitted): The submit event.
        """

        # We're going to remove the input, so let's get its content before
        # we do that.
        title = event.input.value.strip()

        # Now let's remove the input box.
        event.input.remove()

        # If the user entered a title...
        if title:
            # ...add a new timeline associated with it.
            self.query_one( "#streaks", Vertical ).mount( line := StreakLine() )
            line.title = title

### main.py ends here
