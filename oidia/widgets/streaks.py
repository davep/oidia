"""Provides a widget that holds a collection of streaks."""

##############################################################################
# Python imports.
from typing  import Final, Any, cast
from pathlib import Path
from json    import dumps, loads, JSONEncoder

##############################################################################
# XDG imports.
from xdg import xdg_data_home

##############################################################################
# Textual imports.
from textual.css.query  import NoMatches
from textual.containers import Vertical

##############################################################################
# Local imports.
from . import StreakLine

##############################################################################
class Streaks( Vertical ):
    """Container widget for the streaks."""

    DEFAULT_CSS = """
    Streaks {
        overflow-y: scroll;
        scrollbar-background: $primary-background-darken-1;
    }
    """

    STREAKS_FILE: Final = Path( "streaks.json" )
    """Path: The name of the file that the list it saved to."""

    @property
    def data_file( self ) -> Path:
        """Path: The full path to the file for saving the data.

        Note:
            As a side effect of access the directory will be crated if it
            doesn't exist.
        """
        ( save_to := xdg_data_home() / "oidia" ).mkdir( parents=True, exist_ok=True )
        return save_to / self.STREAKS_FILE

    class Encoder( JSONEncoder ):
        """Encoder for the streak data data."""

        def default( self, o: object ) -> Any:
            """Handle unknown values."""
            return o.as_dict if isinstance( o, StreakLine ) else super().default( o )

    def save( self ) -> None:
        """Save the streaks to local storage."""
        self.data_file.write_text( dumps(
            list( self.query( StreakLine ) ),
            cls    = self.Encoder,
            indent = 4
        ) )

    async def load( self ) -> None:
        """Load any streak data from storage."""
        if self.data_file.exists():
            await self.mount( *[
                StreakLine.from_dict( streak )
                for streak in loads( self.data_file.read_text() )
            ] )

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

    def on_streak_line_updated( self ) -> None:
        """Save the streaks when they get updated in some way."""
        self.save()

### streaks.py ends here
