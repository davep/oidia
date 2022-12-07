"""The main screen of the application."""

##############################################################################
# Python imports.
from typing import cast

##############################################################################
# Textual imports.
from textual.app        import ComposeResult
from textual.css.query  import NoMatches
from textual.screen     import Screen
from textual.widgets    import Header, Footer, Input
from textual.containers import Vertical
from textual.binding    import Binding

##############################################################################
# Local imports.
from ..widgets import Timeline, StreakLine, StreakDay, TitleInput

##############################################################################
class Streaks( Vertical ):
    """Container widget for the streaks."""

    @property
    def focused_streak( self ) -> StreakLine | None:
        """StreakLine | None: The streak that contains focus, if there is one."""
        try:
            return self.query_one( "StreakLine:focus-within", StreakLine )
        except NoMatches:
            return None

    def __getitem__( self, index: int ) -> StreakLine:
        """Get a streak based on its index.

        Args:
            index (int): The index of the streak to get.
        """
        return cast( StreakLine, self.children[ index ] )

    def index( self, streak: StreakLine ) -> int:
        """Find the index of the given streak.

        Args:
            streak (StreakLine): The streak to look for.

        Returns:
            int: The position of the streak.

        Raises:
            ValueError: If the streak could not be found.
        """
        return self.children.index( streak )

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
        Binding( "left",                 "focus_left",  "", show=False ),
        Binding( "right",                "focus_right", "", show=False ),
        Binding( "up",                   "focus_up",    "", show=False ),
        Binding( "down",                 "focus_down",  "", show=False ),
        Binding( "comma",                "move(-1)",    "< day" ),
        Binding( "full_stop",            "move(1)",     "> day" ),
        Binding( "left_square_bracket",  "zoom(-1)",    "Zoom In" ),
        Binding( "right_square_bracket", "zoom(1)",     "Zoom Out" ),
        Binding( "a",                    "add",         "Add Streak" ),
        Binding( "escape",               "app.quit",    "Quit" )
    ]
    """list[ Binding ]: The bindings for the main screen."""

    def compose( self ) -> ComposeResult:
        """Compose the content of the main screen.

        Args:
            ComposeResult: The result of composing the screen.
        """
        yield Header( show_clock=True )
        self.streaks = Streaks( Timeline( id="header" ) )
        yield self.streaks
        yield Footer()

    def action_focus_left( self ) -> None:
        """Action wrapper for moving focus to the left."""
        self.focus_previous()

    def action_focus_right( self ) -> None:
        """Action wrapper for moving focus to the right."""
        self.focus_next()

    def action_focus_up( self ) -> None:
        """Action that moves focus up a streak."""
        if ( current := self.streaks.focused_streak ) is not None:
            self.streaks[
                -1 if current.is_first
                else self.streaks.index( current ) - 1
            ].steal_focus( current )

    def action_focus_down( self ) -> None:
        """Action that moves focus down a streak."""
        if ( current := self.streaks.focused_streak ) is not None:
            self.streaks[
                # TODO: Note hard-coded value of 1. This needs to change
                # when I move the header out of the streak list.
                1 if current.is_last
                else self.streaks.index( current ) + 1
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
        await self.query_one( Streaks ).mount( input := TitleInput( placeholder="Title", id="streak-add" ) )
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
            await self.query_one( Streaks ).mount( line := StreakLine() )
            line.title = title
            line.query( StreakDay ).last().focus()

### main.py ends here
