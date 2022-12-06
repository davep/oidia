"""Provides a widget to show the streak status for some days."""

##############################################################################
# Python imports.
from datetime import date

##############################################################################
# Textual imports.
from textual.app      import RenderResult
from textual.reactive import reactive
from textual.binding  import Binding

##############################################################################
# Local imports.
from .timeline import TimelineDay, Timeline

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
        Binding( "minus",       "done( -1 )", "Less Done", key_display="-" ),
        Binding( "equals_sign", "done(  1 )", "More Done", key_display="=" )
    ]
    """list[ Binding ]: The bindings for a streak day."""

    done = reactive( 0 )
    """int: The done count for the day."""

    def render( self ) -> RenderResult:
        """Render the content of the streak day.

        Returns:
            RenderResult: The content to render for the day.
        """
        return str( self.done ) if self.done else ""

    def action_done( self, this_many: int ) -> None:
        """Handle the done count being changed.

        Args:
            this_many (int): The amount to change the done count by.
        """
        self.done = max( 0, self.done + this_many )
        self.set_class( bool( self.done ), "done" )

##############################################################################
class StreakLine( Timeline ):
   """Widget to display a horizontal timeline of streak results."""

   def make_my_day( self, day: date ) -> StreakDay:
        """Make a day widget for the given day.

        Args:
            day (date): The date to make the day widget for.

        Returns:
            StreakDay: The day widget for the timeline.
        """
        return StreakDay( day )

### streakline.py ends here
