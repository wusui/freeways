# Freeways Draftsperson

> We're goin' ridin' on the Freeway of Love. Wind's against our backs...

-- Aretha Franklin

## Description

This directory consists of a set of python files used to direct the drawing
of roads in the Steam game Freeways designed by Justin Smith.

## Insane Manifesto Style Rant

Freeways is a very good game with one serious flaw -- the user interface is
unforgiving.  There is no way to take back a mistake other than to clear the
whole screen and start over.  I have fat fingers, my motor skills leave a lot
to be desired, and I never got higher than a D+ in penmanship, so you can
imagine how well I handle a mouse.  Since I am somewhat sapient and therefore
a toolmaker, I have started to try to handle this by designing a tool to do
the drudgery of mousing and clicking for me.

Note that ideally I will have an application where one can describe what one
wants to do and the actions get automatically performed by the program.
This to me, feels like a good solution and does not intefere with what I believe to be the core feature of the game -- solving the puzzle of
connecting the roads efficiently.  The user still has to design a map to optimize scores.  The fun stuff is still there in all its glory.
The icky stuff isn't.


## Word Usage

Each of the 81 map/interchange pages will be referred to as a level in this
document

## Freeway Definition Language

The key to this program is a freeway definition language which will be used
to define the mouse movements and clicks to construct a solution to a given
level. The following is a BNF description of the language.

```
<program> ::= <statement> | <statement> <program>
<statement> ::= <comment> | <action>
<comment> ::= "^#" <text> "\n"
<action> ::= <line> | <move> | <arc> | "(" <arc-params> ")" | <commands>
<line> ::= "line" <point> <point> <line-name><terminator>
<defline> ::= "defline" <point> <point> <line-name>
<move> ::= "move" <point> <terminator>
<arc> ::= "arc" <line-name> <line-name> <number> <terminator>
<direction> ::= "clockwise" | "counterclockwise"
<point> ::= <number> "," <number>
<number> ::= <sign> <pos-num>
<sign> ::=  "" | "-"
<pos-num> ::= <digit> | <pos-num><digit>
<digit> ::= [0-9]
<line-name> ::= [A-Z_]
<terminator> ::= "" | ";"
<arc_params> ::= <radius> "," <origin> "," <start> "," <end> "," <clockwise>
<radius> ::= <pos-num>
<origin> ::= <point>
<start> ::= <number>
<end> ::= <number>
<clockwise> ::= True | False
<commands> ::= "rbu" | "rbd" | "clear" | "stopwatch" | "hole"

"^#" is a # character at the start of the line. "\n" is a new line.
"<text>" is any text.

<point> is an x, y coordinate of a mouse location on the screen relative
to the drawable portion of the Freeways window.

<line> moves to the first <point>, clicks the left button down, and moves
to the second <point>

<move> moves to the <point> from the current location

<arc> tests if the absolute values of the differences between the two points
are equal.  If they are, a circular arc can be drawn in the direction
specified.  For example, 'arc 100,100 200,200 counterclockwise' will draw a
90 degree curve from point 100, 100 to 200, 200.  'arc 100, 100 200, 200
clockwise' would draw a 270 degree curve from 100, 100 to 200, 200 using the
other side of the circle that drew the 90 degree circle.  The radius of the
arc drawn is the value of the absolute value of the differences on one
of the coordinates.

<arc-params> are parameters to the arc functions if you want to draw arcs
on points in non cartesian grid orientations (do a 60 degree turn, for
instance).  The start and end points are specified in degrees with 0 degrees
being east, 90 degrees being south, 180 degrees being west, and 270 degrees
being north.  Negative values and values greater than 360 are allowed.

<rbd> is used to draw bridges (right button down).

<rbu> stops drawing a bridge (right button up).

<hole> does a ramp-up and a ramp-down (makes a hole for a road to go through)

<clear> clears the screen.

<stopwatch> runs the stopwatch test.
```

Lexically, tokens in the language can be separated by blanks, new lines, and
the defined isolated punctuation marks (",", ";", "(", ")").

## Fragility of the code

This code fails if the windows coordinates are changed.  After starting
a program, do not move the mouse until the program terminates.  Also,
moving the Freeways window may adversely affect the behavior

The windows placement of the game screen may vary between launches slightly.
Because of this, whenever a new game window is brought up some calibration
code is run and offsets are stored in a local json file.

## cmpvalues.json

Due to some inexactness in bit counts on the display, every time a new instance of the
freeway game is started, the cmpvalues.json file in the source directory needs to be
created or updated.  The json file contains two fields: wef_info which consists of bit counts
of green and blue pixels in the "World Efficiency" text on the main map, and a greycount value
which is the number of grey pixels in the menu area.  The "World Efficiency" text is used
to determine if we are on the world map, and the greycount value is needed to find the menu
key.

## Usage

Once a freeway game is started, "python freeway_setup"  needs to be run to set cmpvalues.json
and handle other initialization tasks.  It redraws map 1 and completes once that page has
finished redrawing and retimed.

Now if a user is on a map, running python page_tester.py <level> redraws that map.

python find_points.py <level> is a development tool that prints the coordinates of the cursor every
five seconds.  It is useful for getting coordinate values when developing the solutions found

python find_points.py (no parmeters) keeps track of all lines that get entered
onto the screen.  Line information is stored in linedata.txt.

The uniquify function in compiler.py makes sure that all lines in the solution
number passed are unique.

level is a directory which contains the coded text for each solution.

## Non-generality of code

The code that I have here probably only works on the screen of my laptop.  It is Windows
specific, and uses numbers that correspond to coordinates on a fixed screen size.  The code
can probably be adapted to any screen size by changing all numbers to use values relative to
the window size returned, but I am not motivated enough to make these changes.  It is open
source MIT licensed code so have at it if you want to generalize things.

To demonstrate how this behaves on my laptop, I have made copies of my solutions in
[this YouTube playlist](https://www.youtube.com/playlist?list=PLyGVhG3HR7_z0RlyXKd8QDOv_oxX4plDS)
