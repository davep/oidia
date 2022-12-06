"""The main screen of the application."""

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
from ..widgets import Timeline, TimelineTitle, StreakLine, StreakDay

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
        Binding( "escape", "cancel", "Cancel" )
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

    StreakLine:focus-within TimelineTitle {
        text-style: bold;
        border-left: wide $secondary;
        padding-left: 1;
    }

    StreakLine:focus-within StreakDay {
        text-style: bold;
    }

    StreakLine.editing TimelineTitle {
        display: none;
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
        Binding( "enter",                "edit",     "Edit" ),
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

    async def action_edit( self ) -> None:
        """Edit the title of a timeline on the display."""
        streak = self.query_one( "StreakLine:focus-within", StreakLine )
        streak.add_class( "editing" )
        await streak.mount( input := TitleInput( value=streak.title, placeholder="Title", id="streak-edit" ), before=0 )
        if self.focused is not None:
            self.focused.add_class( "back-here-please" )
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
            # If it's to add a new timeline...
            if ( event.input.id or "" ) == "streak-add":
                # ...add a new timeline associated with it.
                await self.query_one( "#streaks", Vertical ).mount( line := StreakLine() )
                line.title = title
                line.query( StreakDay ).last().focus()
            else:
                # ...it's an edit. Set the new title.
                self.query_one( "StreakLine.editing", StreakLine ).title = title

        # Ensure any editing state is cleared.
        self.query( ".editing" ).remove_class( "editing" )

        # Finally, let's see if we're supposed to settle focus back
        # anywhere.
        try:
            return_to = self.query_one( ".back-here-please" )
            return_to.focus()
            return_to.remove_class( "back-here-please" )
        except NoMatches:
            pass

### main.py ends here
