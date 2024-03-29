"""The main screen of the application."""

##############################################################################
# Textual imports.
from textual.app        import ComposeResult
from textual.screen     import Screen
from textual.widgets    import Header, Footer, Input
from textual.containers import Container
from textual.binding    import Binding

##############################################################################
# Local imports.
from ..widgets import Streaks, Timeline, StreakLine, StreakDay, TitleInput

##############################################################################
class Main( Screen ):
    """The main screen of the application."""

    DEFAULT_CSS = """
    Main {
        background: $primary-background-darken-1;
    }

    Timeline {
        height: 3;
    }

    Timeline#header {
        dock: top;
        padding-right: 2;
        background: $primary-background;
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
        Binding( "left_square_bracket",  "zoom(-1)",    "Zoom In" ),
        Binding( "right_square_bracket", "zoom(1)",     "Zoom Out" ),
        Binding( "a",                    "add",         "Add Streak", key_display="a" ),
        Binding( "escape",               "app.quit",    "Quit" )
    ]
    """list[ Binding ]: The bindings for the main screen."""

    def compose( self ) -> ComposeResult:
        """Compose the content of the main screen.

        Args:
            ComposeResult: The result of composing the screen.
        """
        yield Header( show_clock=True )
        self.streaks = Streaks()
        yield Container( Timeline( id="header" ), self.streaks )
        yield Footer()

    async def on_mount( self ) -> None:
        """Set up the screen on mount."""
        await self.streaks.load()
        if len( self.streaks.children ) > 0:
            self.streaks[ 0 ].query( StreakDay ).last().focus()

    def action_focus_left( self ) -> None:
        """Action wrapper for moving focus to the left."""
        if isinstance( self.screen.focused, StreakDay ) and self.screen.focused.is_first:
            self.action_move( -1 )
        else:
            self.focus_previous()

    def action_focus_right( self ) -> None:
        """Action wrapper for moving focus to the right."""
        if isinstance( self.screen.focused, StreakDay ) and self.screen.focused.is_last:
            self.action_move( 1 )
        else:
            self.focus_next()

    def action_focus_up( self ) -> None:
        """Action that moves focus up a streak."""
        if ( current := self.streaks.focused_streak ) is not None:
            self.streaks[
                -1 if current.is_first else self.streaks.index( current ) - 1
            ].steal_focus( current )

    def action_focus_down( self ) -> None:
        """Action that moves focus down a streak."""
        if ( current := self.streaks.focused_streak ) is not None:
            self.streaks[
                0 if current.is_last else self.streaks.index( current ) + 1
            ].steal_focus( current )

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
        await self.streaks.mount( title_input := TitleInput( placeholder="Title", id="streak-add" ) )
        title_input.focus()

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
            await self.streaks.mount( line := StreakLine() )
            line.title     = title
            line.time_span = self.query_one( "#header", Timeline ).time_span
            line.query( StreakDay ).last().focus()
            self.streaks.save()

### main.py ends here
