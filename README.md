Ascidia
=======

A command-line utility for rendering technical diagrams from ASCII art.

This:

```	
               O     
              -|-  -.
              / \   | 
              User  | Request
                    V
 Foobar         +--------+       .------.
  Layer         |  Acme  |       '------'
- - - - - - +   | Widget |<----->|      |
   .----.   ;   +--------+       |      |
  | do-  |  ;       |            '------'
  |  dad |--^--<|---+            Database
   '----'   ;
            ;
```

Becomes this:

![](https://raw.github.com/Frimkron/Ascidia/master/rm-images/example.png)


* [About Ascidia](#about-ascidia)
* [Requirements](#requirements)
* [Usage](#usage)
* [Diagram Format](#diagram-format)
* [Feedback](#feedback)
* [Credits and Licence](#credits-and-licence)
* [Related Projects](#related-projects)


About Ascidia
-------------

Ascidia converts ASCII-art technical diagrams, created using particular 
symbols, into prettier raster and vector graphic formats. Technical diagrams
can be created and embedded within plain text documentation (source code 
comments, for example) so that they can be maintained in the same place. Later,
the diagrams can be rendered as images ready for publishing.

Ascidia was inspired by similar applications of this type, namely [Ditaa][] 
and [ASCIItoSVG][]. It also takes inspiration from the philosophy of John 
Gruber's [Markdown][], which aims to define a rich text format using intuitive 
formatting rules in place of the syntactic clutter of a markup language.
Ascidia attempts to do the same for ASCII diagrams, by defining a set of 
patterns which are as recognisable in raw text as they are in their rendered 
form.

Ascidia is, apparently, another name for the [Sea Squirt][].

[Ditaa]: http://ditaa.sourceforge.net/
[ASCIItoSVG]: http://9vx.org/~dho/a2s/
[Markdown]: http://daringfireball.net/projects/markdown/
[Sea Squirt]: http://en.wikipedia.org/wiki/Sea_squirt


Requirements
------------

Ascidia requires the following:

* [Python 2.7](http://python.org)
* [PyCairo](http://www.cairographics.org/pycairo/)


Usage
-----

`ascidia [options] [file]`


### Positional Arguments ###

`file`

Path to the input file to read. Use `-` to read from standard input. This is 
the default.


### Options ###

`-h, --help`

Show brief help text

`-o, --outfile`

Path to the output file to write. Use `-` to write to standard output. This is 
the default if reading from standard input, otherwise defaults to 
`<input-file-name>.<output-extension>`.

`-f, --foreground`

The foreground colour, as comma-separated RGB values between 0 and 1. Some 
basic predefined colour names are also supported ("black", "red", "blue", etc).
Defaults to black.

`-b --background`

The background colour, as comma-separated RGB values between 0 and 1. Some
basic predefined colour names are also supported ("black", "red", "blue", etc).
Defaults to white.

`-c, --charheight`

The height to render each character as, in pixels. This will affect the overall
width and height of the output. Defaults to 24.

`-t --type`

The output format. Options are as follows:

* `svg` - Scalable Vector Graphics format. An XML document describing the 
  diagram as a set of shape-drawing instructions.
* `png` - PNG format. A losslessly-compressed raster image format.

Defaults to `png`.

`-q, --quiet`

If specified, causes informational output to be suppressed. Note that such 
output is omitted anyway when writing the diagram to standard output.


### Examples ###

Convert the ASCII diagram `diagram.txt` to a PNG image:

	$ ascidia diagram.txt
	

Convert diagram `foobar.txt` to the SVG file `result.svg`:

	$ ascidia -o result.svg foobar.txt
	

Convert the output of `mycommand` to an SVG file called `output`:

	$ mycommand | ascidia -o output -t svg -


Diagram Format
--------------

Ascidia reads ASCII character data with Unix line endings and converts it to an
image, recognising particular character patterns as diagram elements. The 
following subsections describe the patterns that Ascidia understands.

* [Lines](#lines)
	* [Horizontal Lines](#horizontal-lines)
	* [Vertical Lines](#vertical-lines)
	* [Diagonal Lines](#diagonal-lines)
	* [Square Corners](#square-corners)
	* [Rounded Corners](#rounded-corners)
	* [Hops](#hops)
* [Boxes](#boxes)
	* [Rectangular Boxes](#rectangular-boxes)
	* [Rounded Boxes](#rounded-boxes)
	* [Rhombus Boxes](#rhombus-boxes)
	* [Elliptical Boxes](#elliptical-boxes)
	* [Diamond Boxes](#diamond-boxes)
* [Connectors](#connectors)
	* [Arrows](#arrows)
	* [Enclosed Arrows](#enclosed-arrows)
	* [Crow's Feet](#crows-feet)
	* [Diamond Connectors](#diamond-connectors)
* [Symbols](#symbols)
	* [Stick Figures](#stick-figures)
	* [Storage Symbols](#storage-symbols)
* [Misc](#misc)
	* [Text](#text)


### Lines ###

Ascidia recognises horizontal, vertical and diagonal lines of any length. Lines
can be on their own, or attached to [Boxes](#boxes) or 
[Connectors](#connectors). They may have [square](#square-corners) or 
[rounded](#rounded-corners) corners.


#### Horizontal Lines

Example Input

```	
----------	
- - - - - 
```

Example Output

![](https://raw.github.com/Frimkron/Ascidia/master/rm-images/horiz-lines.png)

Solid horizontal lines consist of one or more dash or hyphen `-` characters.

Dashed horizontal lines consist of alternating dash or hyphen `-` characters, 
and space characters. Note, a dashed horizontal line must begin with a 
hyphen and end with a space. Dashed horizontal lines have a minimum length of
4:

```	
- - 
```

Note that single line characters with text beside them are not recognised as
lines:

```	
---test

-test
```

![](https://raw.github.com/Frimkron/Ascidia/master/rm-images/hline-text.png)


#### Vertical Lines

Example Input

```	
| ;
| ;
| ;
| ;
```

Example Output

![](https://raw.github.com/Frimkron/Ascidia/master/rm-images/vert-lines.png)

Solid vertical lines consist of one or more vertical-bar or pipe `|` characters.

Dashed vertical lines consist of one or more semi-colon `;` characters.

Note that single line characters with text beside them are not recognised as 
lines:

```	
|	
|test   |test
|
```

![](https://raw.github.com/Frimkron/Ascidia/master/rm-images/vline-text.png)


#### Diagonal Lines

Example Input

```	
  /  ,  \  `
 /  ,    \  `
/  ,      \  `
```

Example Output

![](https://raw.github.com/Frimkron/Ascidia/master/rm-images/diag-lines.png)

Solid, right-leaning diagonal lines consist of one or more forwardslash `/` 
characters. 

Dashed, right-leaning diagonal lines consist of one or more comma `,` 
characters.

Solid, left-leaning diagonal lines consist of one or more backslash `\` 
characters.

And dashed, left-leaning diagonal lines consist of one or more grave-accent or 
backtick ` characters.

Note, the line characters should line up diagonally. Also, single line 
characters with text beside them are not recognised as lines:

```	
\     
 \test  \test
  \
```

![](https://raw.github.com/Frimkron/Ascidia/master/rm-images/dline-text.png)


#### Square Corners

Example Input

```	
    +---+
|   |   |
|   |   +
+---+    \ 
       ---+---
```

Example Output

![](https://raw.github.com/Frimkron/Ascidia/master/rm-images/sq-corners.png)

Square line corners are constructed using plus `+` characters. 

Corners may be placed at the intersection of one or more 
[horizontal](#horizontal-lines), [vertical](#vertical-lines) or 
[diagonal](#diagonal-lines) lines.


#### Rounded Corners

Example Input

```	
    .---. 
|   |   |
|   |   :
'---'    \
       ---'---
```

Example Output

![](https://raw.github.com/Frimkron/Ascidia/master/rm-images/rnd-corners.png)

Rounded line corners that curve upwards are constructed using apostrophe or 
single-quote `'` characters.

For corners that curve downwards, full-stop or period characters `.` are used.

Corners that join lines above to lines below are constructed using colon `:` 
characters.

Corners may be placed at the intersection of one or more 
[horizontal](#horizontal-lines), [vertical](#vertical-lines) or 
[diagonal](#diagonal-lines) lines.


#### Hops

Example Input

```	
   |        |        |
---)---  ---(---  ---^---
   |        |        |
```

Example Output

![](https://raw.github.com/Frimkron/Ascidia/master/rm-images/hops.png)

Hops are often used to indicate that two crossing lines are not connected to 
each other.

A hop may be placed at the intersection of any [horizontal](#horizontal-lines) 
line with any [vertical](#vertical-lines) line.

A left-parenthesis or left-round-bracket `(` character, right-parenthesis `)` 
character, or caret `^` character may be used.


### Boxes ###

Boxes enclose other content and may have [lines](#lines) or 
[connectors](#connectors) attached to their outer edges.


#### Rectangular Boxes

Example Input

```	
+-------+
|  My   |
|  Box  |
+-------+
```

Example Output

![](https://raw.github.com/Frimkron/Ascidia/master/rm-images/rect-box.png)

Rectangular boxes are used to represent many things including class, processes 
and database tables.

Rectangular boxes use pipe `|` characters for the sides, hyphen `-` characters 
for the top and bottom, and plus `+` characters for the corners. They may have 
a minimum size of 1 x 1:

```	
+-+
| |
+-+
```

Dashed lines may be used for the sides instead of solid lines. Here, the sides 
are semi-colon `;` characters and the top an bottom are constructed with 
alternating hyphen `-` and space characters. Note, dashed lines must start 
with a hyphen and end with a space:

```	
+- - - - +
;  My    ;
;  Box   ;
+- - - - +
```

![](https://raw.github.com/Frimkron/Ascidia/master/rm-images/dash-rect-box.png)

Rectangular boxes may have separator lines to partition their content, allowing
for the creation of tables or UML class boxes. Hyphen `-` characters are used
for horizontal separators and pipe `|` characters for vertical separators. At
the intersection of two separator lines, either pipe or hyphen may be used. 
Note, each partitioned section inside the box must be at least 1 x 1 in size:

```	
+-----------+
| A | B | C |
|-----------|
| 1 | 50|   |
| 24|   | 7 |
+-----------+
```

![](https://raw.github.com/Frimkron/Ascidia/master/rm-images/sep-rect-box.png)


#### Rounded Boxes

Example Input

```	
.-------.
|  My   |
|  Box  |
'-------'	
```

Example Output

![](https://raw.github.com/Frimkron/Ascidia/master/rm-images/round-box.png)

Rounded boxes use pipe `|` characters for the sides and hyphen `-` characters 
for the top and bottom. The top left and top right corners are full-stop or 
period `.` characters. The bottom left and right corners are apostrophe or
single-quote characters `'`. Rounded boxes have a minimum size of 1 x 1:

```	
.-.
| |
'-'
```

Alternatively, forwardslash `/` and backslash `\` characters may be used for
the corners:

```	
/-------\
|  My   |
|  Box  |
\-------/
```

Dashed lines may be used for the sides instead of solid lines. Here, the sides 
are semi-colon `;` characters and the top an bottom are constructed with 
alternating hyphen `-` and space characters. Note, dashed lines must start 
with a hyphen and end with a space:

```	
.- - - - .
;  My    ;
;  Box   ;
'- - - - '
```

![](https://raw.github.com/Frimkron/Ascidia/master/rm-images/dash-round-box.png)


#### Rhombus Boxes

Example Input

```	
   +------+
  / My   /
 /  Box /
+------+
```

Example Output

![](https://raw.github.com/Frimkron/Ascidia/master/rm-images/rhom-box.png)

Right-leaning rhombus or parallelogram boxes are sometimes used to represent
I/O in data flow diagrams.

Rhombus boxes consist of hyphen or dash `-` characters for the top and bottom, 
forwardslash `/` characters for the sides, and plus `+` characters for the 
corners. Rhombus boxes have a minimum size of 1 x 1:

```	
  +-+
 / /	
+-+
```


#### Elliptical Boxes

Example Input

```	
 .-----.
|  My   |
|  Box  |
 '-----'
```

Example Output

![](https://raw.github.com/Frimkron/Ascidia/master/rm-images/ell-box.png)

Elliptical or circular boxes are used to represent many things including
states and data flow starts and ends.

Elliptical boxes consist of hyphen or dash `-` characters for the top and 
bottom and pipe or vertical-bar `|` characters for the sides. The top
left and top right corners are full-stop or period `.` characters, and the 
bottom left and bottom right corners are apostrophe or single-quote `'` 
characters. Note, ellipses differ subtly from [rounded boxes](#rounded-boxes)
in that the sides are offset from the corners by one character.

Ellipses have a minimum size as follows:

```	
 .-.
|   |
 '-'
```

Elliptical boxes may use slashes in conjunction with the period-apostrophe 
corners to make large ellipses a bit more rounded. Here, the top left and 
bottom right corners use forwardslash `/` characters, and the top right and 
bottom left corners use backslash `\` characters. Multiple slashes may be used 
for long diagonal corners. The periods and apostrophes must be on the top and 
bottom rows, respectively:

```	
   .----.	
  /      \
 /        \
|          |
|          |
 \        /
  \      /
   '----'

```


#### Diamond Boxes

Example Input

```	
     .'.
   .'My '.
  <  Box  >
   '.   .'
     '.'
```

Example Output

![](https://raw.github.com/Frimkron/Ascidia/master/rm-images/diam-box.png)

Diamond-shaped boxes are used to represent a decision point in data flow 
diagrams.

Diamond boxes use a left chevron or angle-bracket `<` character for the 
left side and a right chevron or angle-bracket `>` character for the right 
side. The diagonal lines use alternating full-stop or period `.` characters and
apostrophe or single-quote characters `'`. Note, the top and bottom peaks may 
be periods or apostrophes. Diamonds have a minimum size of 1 x 1:

```	
 . 
< >
 '
```


### Connectors ###

Connectors can be attached to [lines](#lines) and/or [boxes](#boxes).


#### Arrows

Example Input

```	
      ^        |
<---  |  --->  |
      |        v
```

Example Output

![](https://raw.github.com/Frimkron/Ascidia/master/rm-images/arrows.png)

Arrowheads may be attached to the end of any [horizontal](#horizontal-lines) 
or [vertical](#vertical-lines) line.

Left-pointing arrowheads use the left chevron or left angle-bracket `<` 
character.

Up-pointing arrowheads use the hat or caret `^` character.

Right-pointing arrowheads use the right chevron or right angle-bracket `>`
character.

Down-pointing arrowheads use the letter vee `v` character, either uppercase or 
lowercase.

An arrowhead pointing at a [box](#boxes) will be rendered flush against it:

```	
+---+
|   |<----
+---+
```

![](https://raw.github.com/Frimkron/Ascidia/master/rm-images/arrow-box.png)


#### Enclosed Arrows

Example Input

```	
       /_\          |
<|---   |   ---|>  _|_
        |          \ /
```

Example Output

![](https://raw.github.com/Frimkron/Ascidia/master/rm-images/enc-arrows.png)

Enclosed, empty arrowheads are used in UML class diagrams to represent 
inheritance.

Enclosed arrowheads may be attached to the end of almost any 
[horizontal](#horizontal-lines) or [vertical](#vertical-lines) line. Note, 
however, that *the line must be 2 or more characters long*.

Left-pointing arrowheads consist of a left chevron or angle-bracket character 
`<`, followed by a vertical-bar or pipe `|` character.

Up-pointing arrowheads consist of a forwardslash `/` character, followed by an 
underscore `_` character, and finally a backslash `\` character.

Right-pointing arrowheads consist of a vertical-bar or pipe `|` character, 
followed by a right chevron or angle-bracket character `>`.

Down-pointing arrowheads are constructed by placing an underscore `_` character
on either side of the vertical line, then on the next row, backslash `\` 
followed by space, followed by forwardslash `/`.

An arrowhead pointing at a [box](#boxes) will be rendered flush against it:

```	
+---+
|   |<|---
+---+
```

![](https://raw.github.com/Frimkron/Ascidia/master/rm-images/enc-arrow-box.png)


#### Crow's Feet

Example Input

```	          
                             
          +---+              |
+---+     |   |     +---+    ^
|   |>--  +---+  --<|   |  +---+
+---+       v       +---+  |   |
            |              +---+            
```

Example Output

![](https://raw.github.com/Frimkron/Ascidia/master/rm-images/crowsfeet.png)

Crow's feet are often used in entity-relationship diagrams to indicate a 
one-to-many relationship.

Crow's feet connectors can be used to join any [horizontal](#horizontal-lines)
or [vertical](#vertical-lines) line to any [box](#boxes).

On the right side of a box, the right chevron or angle-bracket `>` character is
used.

On the bottom side of a box, the letter vee `v` character is used, uppercase or
lowercase.

On the left side of a box, the left chevron or angle-bracket `<` character is 
used.

On the top side of a box, the hat or caret `^` character is used.


#### Diamond Connectors

Example Input

```	
            +---+               | |
            |   |               | ^
+---+       +---+       +---+   ^ #
|   |<>---   ^ ^   ---<>|   |   v v
|   |<#>--   v #   --<#>|   |  +---+
+---+        | v        +---+  |   |
             | |               +---+
```

Example Output

![](https://raw.github.com/Frimkron/Ascidia/master/rm-images/dmd-connectors.png)

Diamond-shaped connectors are used in UML class diagrams to represent 
composition or "has-a" relationships.

Diamond connectors can be used to join any [horizontal](#horizontal-lines)
or [vertical](#vertical-lines) line to any [box](#boxes). They come in empty
and filled varieties.

Empty, horizontal diamond connectors consist of a left chevron or angle-bracket
`<` character, followed by a right chevron or angle-bracket `>` character. 

Filled horizontal diamond connectors are similar, but with a hash or pound `#`
character in the middle.

Empty, vertical diamond connectors consist of a hat or caret `^` character with
a letter vee `v` character below it, uppercase or lowercase.

Filled vertical diamond connector are similar, but with a hash or pound `#`
character in the middle.


### Symbols ###

Ascidia supports a number of commonly-used symbols, converted to ASCII 
representations.


#### Stick Figures

Example Input

```	
 O
-|-
/ \
```

Example Output

![](https://raw.github.com/Frimkron/Ascidia/master/rm-images/stick-figure.png)

Stick figures are often used to represent the point at which a human being 
interacts with a system.

The stick figure's head is either a letter oh `O` character (uppercase or 
lowercase) or a zero `0` character. The midsection on the middle row consists
of a dash or hyphen `-` character, followed by a vertical-bar or pipe `|`
character, followed by another dash `-` character. The legs on the final row
consist of a forwardslash `/` character, followed by a space, followed by a 
backslash `\` character.


#### Storage Symbols

Example Input

```	
.----.
'----'
| DB |
'----'
```

Example Output

![](https://raw.github.com/Frimkron/Ascidia/master/rm-images/storage.png)

Storage cylinder symbols are often used in system architecture diagrams to 
represent some kind of storage device such as a database or hard disk.

The storage symbol uses dash or hyphen `-` characters for the horizontal lines
and vertical-bar or pipe `|` characters for the vertical lines. The 
downward-curving corners are full-stop or period `.` characters, and the 
upward-curving corners are apostrophe or single-quote `'` characters.

The symbol may vary in width or height, but has a minimum size as follows:

```	
           .----.
.-------.  '----'  .-.
'-------'  |    |  '-'
| Wide  |  |tall|  | |
'-------'  |    |  '-'
           '----'  min
```


### Misc ###

#### Text

Example Input

```	
  The quick brown fox
jumps over the lazy dog
```

Example Output

![](https://raw.github.com/Frimkron/Ascidia/master/rm-images/text.png)

Character data which is not recognised as a diagram element is written to
the output as plain text. The position of each character is preserved.


Feedback
--------

Any and all feedback is much appreciated. Please submit suggestions and bug 
reports to the [Github project page][], or otherwise send me an [email][].

[Github project page]: https://github.com/Frimkron/Ascidia
[email]: mailto:mfrimston@gmail.com


Credit and Licence
------------------

Written by Mark Frimston

Project page: <https://github.com/Frimkron/Ascidia>  
Homepage: <http://markfrimston.co.uk>  
Email: <mfrimston@gmail.com>  
Twitter: [@frimkron](http://twitter.com/frimkron)  

Released under the MIT Licence. See the source code for the full text of this 
licence.


Related Projects
----------------

Some other related projects that you might find interesting:

* [Ditaa](http://ditaa.sourceforge.net/) - A similar, more popular ASCII diagram 
  converter written in Java
* [ASCIItoSVG](http://9vx.org/~dho/a2s/) - Another ASCII diagram converter, influenced
  by Markdown and written in PHP
* [Asciio](http://search.cpan.org/dist/App-Asciio/lib/App/Asciio.pm) - A Perl application
  for drawing ASCII diagrams using a graphical user interface
* [AsciiFlow](http://www.asciiflow.com) - An online editor for drawing ASCII diagrams
* [Fossil Draw](http://www.fossildraw.com/) - Another online ASCII diagram editor
* [Text Bunny](http://www2.b3ta.com/_bunny/texbunny.gif) - an ASCII bunny
