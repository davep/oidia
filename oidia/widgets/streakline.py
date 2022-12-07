"""Provides a widget to show the streak status for some days."""

##############################################################################
# Python imports.
from typing      import Any, cast
from datetime    import date, timedelta
from collections import defaultdict

##############################################################################
# Textual imports.
from textual.app       import RenderResult
from textual.reactive  import reactive
from textual.binding   import Binding
from textual.message   import Message
from textual.events    import Click
from textual.css.query import NoMatches

##############################################################################
# Local imports.
from .timeline    import TimelineDay, Timeline
from .title_input import TitleInput

##############################################################################
class StreakDay( TimelineDay, can_focus=True ):
    """Widget for tracking if a day is done or not."""

    DEFAULT_CSS = """
    StreakDay {
        content-align: center middle;
    }
    """
    """str: The default styling for a streak day."""

    BINDINGS = [
        Binding( "minus,backspace",   "done( -1 )", "Less Done", key_display="-" ),
        Binding( "equals_sign,space", "done(  1 )", "More Done", key_display="=" )
    ]
    """list[ Binding ]: The bindings for a streak day."""

    done = reactive( 0 )
    """int: The done count for the day."""

    def __init__( self, day: date, done: int, *args: Any, **kwargs: Any ) -> None:
        """Initialise the streak day."""
        super().__init__( day, *args, **kwargs )
        self.done = done

    def render( self ) -> RenderResult:
        """Render the content of the streak day.

        Returns:
            RenderResult: The content to render for the day.
        """
        return str( self.done ) if self.done else ""

    class Updated( Message ):
        """Message sent when the streak day is updated.

        Attributes:
            day (date): The day on the timeline.
            done (int): The done count for the day.
        """

        def __init__( self, sender: "StreakDay", updated_to: int ) -> None:
            """Initialise the message.

            Args:
                sender (StreakDay): The streak day widget sending the message.
                updated_to (int): The number the done count is being updated to.
            """
            super().__init__( sender )
            self.day  = sender.day
            self.done = updated_to

    def on_mount( self ) -> None:
        """Force an initial refresh on mount."""
        self.action_done( 0 )

    def watch_done( self, new_done: int ) -> None:
        """React to changes in the done count.

        Args:
            new_done (int): The new value for `done`.
        """
        self.set_class( bool( new_done ), "done" )
        self.emit_no_wait( self.Updated( self, new_done ) )

    def action_done( self, this_many: int ) -> None:
        """Handle the done count being changed.

        Args:
            this_many (int): The amount to change the done count by.
        """
        self.done = max( 0, self.done + this_many )

    def on_click( self, event: Click ) -> None:
        """Handle a mouse click event.

        Args:
            event (Click): The click event.

        Note:
            Implements the ability to increase or decrease the done count
            for a day using the mouse. A non-modified mouse click is left
            alone. Ctrl+Click or Meta+Click increases the done count.
            Shift+Click decreases it.
        """
        if event.ctrl or event.meta:
            self.action_done( 1 )
        elif event.shift:
            self.action_done( -1 )

##############################################################################
class StreakLine( Timeline ):
    """Widget to display a horizontal timeline of streak results."""

    DEFAULT_CSS = """
    StreakLine.editing TimelineTitle {
        display: none;
    }
    """

    BINDINGS = [
        Binding( "enter", "edit", "Edit" )
    ]
    """list[ Binding ]: The bindings for the widget."""

    def __init__( self, *args: Any, **kwargs: Any ) -> None:
        """Initialise the streak line."""
        super().__init__( *args, **kwargs )
        self._streaks: defaultdict[ date, int ] = defaultdict( int )

    def make_my_day( self, day: date ) -> StreakDay:
        """Make a day widget for the given day.

        Args:
            day (date): The date to make the day widget for.

        Returns:
            StreakDay: The day widget for the timeline.
        """
        return StreakDay( day, self._streaks[ day ] )

    def on_streak_day_updated( self, event: StreakDay.Updated ) -> None:
        """React to the done count of a day being changed.

        Args:
            event (StreakDay.Updated): The event.
        """
        self._streaks[ event.day ] = event.done
        if self._streaks[ event.day ] == 0:
            del self._streaks[ event.day ]

    def adjust_day( self, day: TimelineDay, delta: timedelta ) -> None:
        """Adjust the date of a given timeline day.

        Args:
            day (TimelineDay): The day widget to adjust.
            delta (timedelta): The period of time to adjust by.
        """
        super().adjust_day( day, delta )
        cast( StreakDay, day ).done = self._streaks[ day.day ]

    async def action_edit( self ) -> None:

        # Place the streak in editing mode.
        self.add_class( "editing" )

        # Mount an input, set it to edit the title and focus it. Note that
        # we place it at the start of the streak widget -- the CSS will hide
        # the title itself while this is all happening (see the application
        # of the "editing" class just above).
        await self.mount( input := TitleInput( value=self.title, placeholder="New title" ), before=0 )
        input.focus()

        # Finally, mark the actual focused widget as the one that was
        # focused, so we can return to it post-edit.
        if self.screen.focused is not None:
            self.screen.focused.add_class( "back-here-please" )

    async def on_input_submitted( self, event: TitleInput.Submitted ) -> None:
        """Handle the user submitting input.

        Args:
            event (TitleInput.Submitted): The submit event.
        """

        # We don't want this event bubbling up the DOM. If we got this it's
        # an edit event. That's on us.
        event.prevent_default()

        # Let's make sure focus is back to where it should be.
        try:
            return_to = self.query_one( ".back-here-please" )
            return_to.focus()
            return_to.remove_class( "back-here-please" )
        except NoMatches:
            pass

        # We're going to remove the input, so let's get its content before
        # we do that.
        title = event.input.value.strip()

        # Now let's remove the input box.
        await event.input.remove()

        # If the user entered a title...
        if title:
            # ...go with it.
            self.title = title

        # Ensure any editing state is cleared.
        self.remove_class( "editing" )

### streakline.py ends here
