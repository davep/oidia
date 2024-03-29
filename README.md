# OIDIA

## Introduction

OIDIA is a simple terminal-based streak tracker, written in Python using
[Textual](https://textual.textualize.io/).

By simple I *mean* simple. There's no shaming and streak counting and all
that stuff; it just lets you record what you've done, what days you've done
it on, and how many times you did it on those days.

That's it.

No judgement.

![OIDIA in action](https://raw.githubusercontent.com/davep/oidia/main/oidia.png)

## Usage

I aim to add a help screen so that the keys etc will be visible within the
application. Hopefully though most features can be found from the footer or
are easily discovered. The main points are:

- <kbd>a</kbd> adds a new streak
- <kbd>Ctrl+d</kbd> deletes a new streak
- <kbd>Ctrl+Up</kbd> moves a streak up
- <kbd>Ctrl+Down</kbd> moves a streak down
- <kbd>Enter</kbd> edits the title of a streak
- <kbd>Space</kbd> or <kbd>=</kbd> increase the count for a day
- <kbd>Backspace</kbd> or <kbd>-</kbd> decrease the count for a day
- <kbd>[</kbd> zooms the timeline in
- <kbd>]</kbd> zooms the timeline out

## TODO

- [ ] Add a help screen

## Licence

OIDIA - A simple judgement-free terminal-based streak tracker  
Copyright (C) 2022-2023 Dave Pearson

This program is free software: you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the Free
Software Foundation, either version 3 of the License, or (at your option)
any later version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
more details.

You should have received a copy of the GNU General Public License along with
this program. If not, see <https://www.gnu.org/licenses/>.

[//]: # (README.md ends here)
