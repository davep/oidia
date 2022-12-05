"""Provides the timeline header widget."""

##############################################################################
# Python imports.
from typing   import Type, Any
from datetime import date, timedelta

##############################################################################
# Textual imports.
from textual.app        import ComposeResult, RenderResult
from textual.containers import Horizontal
from textual.reactive   import reactive
from textual.widgets    import Static

##############################################################################
class TimelineDay( Static ):
    """A widget for displaying information on a timeline date."""

    DEFAULT_CSS = """
    TimelineDay {
        width: 1fr;
        text-align: center;
    }
    """

    day = reactive( date.today() )
    """date: The date of this day."""

    def __init__( self, day: date ) -> None:
        """Initialise the day widget.

        Args:
            day (date): The day to represent.
        """
        super().__init__()
        self.day = day

    def render( self ) -> RenderResult:
        """Render this day.

        Returns:
            RederResult: The rendering of this day.
        """
        return self.day.strftime( "%b %d\n%a" )

##############################################################################
class Timeline( Horizontal ):
    """Widget to display a horizontal timeline."""

    time_span = reactive( timedelta( weeks=1 ), init=False )
    """timedelta: The span of time the timeline will show in one go."""

    end_date = reactive( date.today() )
    """date: The last date shown in the timeline."""

    def __init__( self, day_type: Type[ TimelineDay ]=TimelineDay, **kwargs: Any ) -> None:
        """Initialise the timeline display.

        Args:
            day_type (Type[ TimelineDay ]): The type of widget to use to show a day.
        """
        super().__init__( **kwargs )
        self._day_type = day_type

    @property
    def start_date( self ) -> date:
        """date: The first date shown in the timeline."""
        return self.end_date - self.time_span

    @property
    def dates( self ) -> list[ date ]:
        """list[ date ]: The list of dates currently in the window of interest."""
        return [ self.start_date + timedelta( days=day ) for day in range( 1, self.time_span.days + 1 ) ]

    def compose( self ) -> ComposeResult:
        """Compose the widget.

        Returns:
            ComposeResult: The result of composing the widget.
        """
        for day in self.dates:
            yield self._day_type( day )

    def watch_time_span( self, new_span: timedelta ) -> None:
        """React to changes to the time span of the timeline.

        Args:
            new_span (timedelta): The new timespan for the timeline.
        """
        self.query( TimelineDay ).remove()
        self.mount( *[
            self._day_type( self.end_date - timedelta( days=day ) )
            for day in reversed( range( new_span.days ) )
        ] )

    def watch_end_date( self, old_date: date, new_date: date ) -> None:
        """React to changes to the end date for the display.

        Args:
            old_date (date): The old value for the end date.
            new_date (date): The new value for the end date.
        """
        diff = new_date - old_date
        for day in self.query( TimelineDay ):
            day.day += diff

    def move_days( self, days: int ) -> None:
        """Move the timeline by a given number of days.

        Args:
            days (int): The number of days to move by.
        """
        self.end_date += timedelta( days=days )

    def zoom_days( self, days: int ) -> None:
        """Zoom the timeline in/out by a given number of days.

        Args:
            days (int): The number of days to zoom by.

        Note:
            A negative number of days zooms out.
        """
        # Ensure the zoom only ever results in a single day at most.
        if self.time_span.days > 1 or days > 0:
            self.time_span += timedelta( days=days )

### timeline.py ends here
