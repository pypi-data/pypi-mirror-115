Brutal Maze
===========

Brutal Maze is a thrilling shoot 'em up game with minimalist art style.

.. image:: https://brutalmaze.rtfd.io/_images/screenshot.png
   :target: https://brutalmaze.rtfd.io/recplayer.html

The game features a trigon trapped in an infinite maze.  As our hero tries
to escape, the maze's border turns into aggressive squares trying to stop per.
Your job is to help the trigon fight against those evil squares and find
a way out (if there is any).  Be aware that the more get killed,
the more will show up and our hero will get weaker when wounded.

Brutal Maze has a few notable features:

* Being highly portable.
* Auto-generated and infinite maze.
* No binary data for drawing.
* Enemies with special abilities: stun, poison, camo, etc.
* Somewhat a realistic physic and logic system.
* Resizable game window in-game.
* Easily customizable via INI file format.
* Recordable in JSON (some kind of silent screencast).
* Remote control through TCP/IP socket (can be used in AI researching).

Installation
------------

Brutal Maze is written in Python and is compatible version 3.6 and above.
The installation procedure should be as simple as follows:

* Install Python and pip_.  Make sure the directory for `Python scripts`_
  is in your ``$PATH``.
* Open Terminal or Command Prompt and run ``pip install --user brutalmaze``.

For more information, see Installation_ page from the documentation.

After installation, you can launch the game by running the command
``brutalmaze``.  Below are the default bindings, which can be configured as
shown in the next section:

F2
   New game.
``p``
   Toggle pause.
``m``
   Toggle mute.
``a``
   Move left.
``d``
   Move right.
``w``
   Move up.
``s``
   Move down.
Left Mouse
   Long-range attack.
Right Mouse
   Close-range attack, also dodge from bullets.

Additionally, Brutal Maze also supports touch-friendly control.  In this mode,
touches on different grid (empty, wall, enemy, hero) send different signals
(to guide the hero to either move or attack, or start new game).  Albeit it is
implemented using *mouse button up* event, touch control is not a solution for
mouse-only input, but an attempt to support mobile GNU/Linux distribution such
as postmarketOS, i.e. it's meant to be played using two thumbs :-)

Configuration
-------------

Brutal Maze supports both configuration file and command-line options.
Apparently, while settings for graphics, sound and socket server can be set
either in the config file or using CLI, keyboard and mouse bindings are limited
to configuration file only.

Settings are read in the following order:

0. Default configuration [1]_
1. System-wide configuration file [2]_
2. Local configuration file [2]_
3. Manually set configuration file [3]_
4. Command-line arguments

Later-read preferences will override previous ones.

Remote control
--------------

If you enable the socket server [4]_, Brutal Maze will no longer accept
direct input from your mouse or keyboard, but wait for a client to connect.
The I/O format is explained in details in the `Remote Control`_ page.

Game recording
--------------

Either game played by human or client script can be recorded to JSON format.
This can be enabled by setting the output directory to a non-empty string [5]_.
Recordings can be played using Brutal Maze `HTML5 record player`_.

Copying
-------

Brutal Maze's source code and its icon are released under GNU Affero General
Public License version 3 or later. This means if you run a modified program on
a server and let other users communicate with it there, your server must also
allow them to download the source code corresponding to the modified version
running there.

This project also uses Tango color palette and several sound effects, whose
authors and licenses are listed in the Copying_ page in our documentation.

.. [1] This can be copied to desired location by ``brutalmaze --write-config
   PATH``.  ``brutalmaze --write-config`` alone will print the file to stdout.
.. [2] These will be listed as fallback config in the help message
   (``brutalmaze --help``). See the Configuration_ documentation for more info.
.. [3] If specified by ``brutalmaze --config PATH``.
.. [4] This can be done by either editing option *Enable* in section *Server*
   in the configuration file or launching the game via ``brutalmaze --server``.
.. [5] ``brutalmaze --record-dir DIR``.  Navigate to Configuration_
   to see more options.

.. _pip: https://pip.pypa.io/en/latest/
.. _Python scripts: https://docs.python.org/3/install/index.html#alternate-installation-the-user-scheme
.. _Installation: https://brutalmaze.rtfd.io/install.html
.. _Remote Control: https://brutalmaze.rtfd.io/remote.html
.. _HTML5 record player: https://brutalmaze.rtfd.io/recplayer.html
.. _Copying: https://brutalmaze.rtfd.io/copying.html
.. _Configuration: https://brutalmaze.rtfd.io/config.html
