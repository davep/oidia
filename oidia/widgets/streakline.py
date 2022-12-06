"""Provides a widget to show the streak status for some days."""

##############################################################################
# Python imports.
from datetime import date

##############################################################################
# Textual imports.
from textual.app import RenderResult

##############################################################################
# Local imports.
from .timeline import TimelineDay, Timeline

##############################################################################
class StreakDay( TimelineDay ):
    """Widget for tracking if a day is done or not."""

    def render( self ) -> RenderResult:
        """Render the content of the streak day.

        Returns:
            RenderResult: The content to render for the day.
        """
        return ""

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
