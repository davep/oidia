"""Provides a widget for inputting titles."""

##############################################################################
# Textual imports.
from textual.widgets import Input
from textual.binding import Binding

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

### title_input.py ends here
