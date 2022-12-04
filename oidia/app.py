"""The main app class."""

##############################################################################
# Textual imports.
from textual.app import App

##############################################################################
# Local imports.
from .        import __version__
from .screens import Main

##############################################################################
class OIDIA( App[ None ] ):
    """The main app class."""

    TITLE = "OIDIA"
    """str: The title of the application."""

    SUB_TITLE = f"The simple terminal streak tracker - v{__version__}"
    """str: The subtitle of the application."""

    SCREENS = {
        "main": Main
    }
    """dict[ str, Screen ]: The screens for the application."""

    def on_mount( self ) -> None:
        """Initialise the application on startup."""
        self.push_screen( "main" )

##############################################################################
def run() -> None:
    """Run the application."""
    OIDIA().run()

### app.py ends here
