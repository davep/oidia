"""Provides the timeline header widget."""

##############################################################################
# Python imports.
from typing   import Any
from datetime import date, timedelta

##############################################################################
# Textual imports.
from textual.app        import ComposeResult, RenderResult
from textual.containers import Horizontal, Grid
from textual.css.query  import NoMatches
from textual.reactive   import reactive
from textual.widgets    import Static, Label

##############################################################################
class TimelineDay( Static ):
    """A widget for displaying information on a timeline date."""

    DEFAULT_CSS = """
    TimelineDay {
        width: 100%;
        height: 100%;
        text-align: center;
    }
    """
    """str: The default styling for a `TimelineDay`."""

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
class TimelineTitle( Label ):
    """A widget that displays the title of a timeline."""

    DEFAULT_CSS = """
    TimelineTitle {
        width: 25;
        height: 100%;
    }
    """
    """str: The default styling for a `TimelineTitle`."""

##############################################################################
class TimelineDays( Grid ):
    """Widget that shows the actual days on the timeline."""

    DEFAULT_CSS = """
    TimelineDays {
        width: 1fr;
        grid-size: 1;
    }
    """
    """str: The default styling for a `TimelineDays`."""

    def __init__( self, span: timedelta, *args: Any, **kwargs: Any ) -> None:
        """initialise the days widget.

        Args:
            span (timedelta): The span of time to cover.
        """
        super().__init__( *args, **kwargs )
        self.spanning( span )

    def spanning( self, span: timedelta ) -> None:
        """Set the span for the days display.

        Args:
            span (timedelta): The span.
        """
        self.styles.grid_size_columns = span.days

##############################################################################
class Timeline( Horizontal ):
    """Widget to display a horizontal timeline."""

    title = reactive( "", init=False )
    """str: The title to five the timeline."""

    time_span = reactive( timedelta( weeks=1 ), init=False )
    """timedelta: The span of time the timeline will show in one go."""

    end_date = reactive( date.today() )
    """date: The last date shown in the timeline."""

    @property
    def start_date( self ) -> date:
        """date: The first date shown in the timeline."""
        return self.end_date - self.time_span

    @property
    def dates( self ) -> list[ date ]:
        """list[ date ]: The list of dates currently in the window of interest."""
        return [ self.start_date + timedelta( days=day ) for day in range( 1, self.time_span.days + 1 ) ]

    def make_my_day( self, day: date ) -> TimelineDay:
        """Make a day widget for the given day.

        Args:
            day (date): The date to make the day widget for.

        Returns:
            TimelineDay: The day widget for the timeline.
        """
        return TimelineDay( day )

    def compose( self ) -> ComposeResult:
        """Compose the widget.

        Returns:
            ComposeResult: The result of composing the widget.
        """
        yield TimelineTitle( self.title )
        self.days = TimelineDays( self.time_span, *[
            self.make_my_day( day ) for day in self.dates
        ] )
        yield self.days

    def on_mount( self ) -> None:
        """Set up the display after it has been mounted."""
        self.days.spanning( self.time_span )

    def watch_title( self, new_title: str ) -> None:
        """Update the title when a new one is set.

        Args:
            new_title (str): The new title.
        """
        try:
            self.query_one( TimelineTitle ).update( new_title )
        except NoMatches:
            pass

    def watch_time_span( self, new_span: timedelta ) -> None:
        """React to changes to the time span of the timeline.

        Args:
            new_span (timedelta): The new timespan for the timeline.
        """
        self.query( TimelineDay ).remove()
        self.days.mount( *[
            self.make_my_day( self.end_date - timedelta( days=day ) )
            for day in reversed( range( new_span.days ) )
        ] )
        self.days.spanning( self.time_span )

    def adjust_day( self, day: TimelineDay, delta: timedelta ) -> None:
        """Adjust the date of a given timeline day.

        Args:
            day (TimelineDay): The day widget to adjust.
            delta (timedelta): The period of time to adjust by.
        """
        day.day += delta

    def watch_end_date( self, old_date: date, new_date: date ) -> None:
        """React to changes to the end date for the display.

        Args:
            old_date (date): The old value for the end date.
            new_date (date): The new value for the end date.
        """
        diff = new_date - old_date
        for day in self.query( TimelineDay ):
            self.adjust_day( day, diff )

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
