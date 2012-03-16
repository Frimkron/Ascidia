% Ascii Diagram Tool
% Mark Frimston
% 2012-03-15

Motivation
----------

[Ditaa][1] is a neat tool for turning ascii-art diagrams into rendered images. 
This is great, but the syntax relies heavily on extra annotations for doing 
things like colours, box types and so on.

[1]: __TODO__ ditaa url

[Ascii2svg][2] is a similar project written in PHP, inspired by Ditaa, but 
but which focuses on outputting to a scalable format - namely svg. It has nicer
rounded corner syntax. The author is fan of markdown, however Ascii2svg still 
suffers from the same syntax issue.

[2]: __TODO__ ascii2svg url

[Markdown][3] is awesome both in its philosophy and its implementation. But it 
would be nice to be able to embed diagrams in it and have them transformed to 
a pretty format when converting the document to something that supports images.
The Markdown philosophy is that the raw text should be perfectly readable and 
formatting should not have to pollute the document with extra syntax. 
Markdown's syntax attempts to work on conventions that people already use and 
are familiar with, and would recognise the significance of in other peoples' 
documents.

[3]: __TODO__ markdown url

[Pandoc-ditaa][4] is a quick perl script that someone wrote to pre-process a 
Pandoc document, extract code blocks marked as ditaa format, render them to 
images, and substitude them with image links in the document before it is 
converted. This is a great idea.

[4]: __TODO__ pandoc-ditaa url

The problem with ditaa and ascii2svg is that they both rely on special syntax 
that a person viewing the ascii diagram would not be able to make any sense of.
Much better would be to have an ascii diagram syntax that followed the markdown
philosophy and turned common and meaningful conventions in the raw text into 
recognised syntax.

For example, to label a box as being a database cylinder symbol, it must be 
marked with a `{d}` label:

    +--------+
    |{d}     |
    | Master |
    |        |
    +--------+

A human can make sense of this, but it defeats the purpose of having a 
visualisation in the first place. It doesn't *look* like a cylinder symbol.

Similarly, ascii2svg's syntax has the user appending a bunch of metadata to the
bottom of the diagram, including whether the box should have a special symbol 
such as a database cylinder:

    +--------+ 
    |[1]     |
    | Master |
    |        |  [1]: { "type": "database" }
    +--------+

(Or something like that).

So, the intention is to create an ascii diagram format which follows the 
Markdown philosophy. It has a set of rules which attempt to turn existing 
conventions into recognised syntax. Diagrams look perfectly understandable 
in their raw text format, with minimal additional annotations concerned only 
with the converted format.


Rules
-----

### Solid Lines

    ---   |   \    /
          |    \  /

* Horizontal runs of hyphens
* Vertinal runs of pipes
* SE Diagonal runs of backslashes
* NE Diagonal runs of forwardslashes
* 2 or more horizontally
* 1 or more vertically
* 1 or more diagonally

### Dashed Lines

    ...   :   '''
          :

* Horizontal runs of periods
* Horizontal runs of apostraphes
* Verical runs of colons
* 2 or more horizontally
* 1 or more vertically

### Wavy Lines

    ~~~  S
         S

* Horizontal runs of tildes
* Vertical runs of S's
* 2 or more horizontally
* 1 or more vertically

### Jagged Lines

    \/\/\/\    \  
               /                 
               \                 
               
* Horizontal alternating slashes
* Vertical alternating slashes
* 2 or more horizontally
* 2 or more vertically

### Fluffy lines

    nnnnn  )  uuuuu  (           .-----------------------.    
           )         (           (/                       )
           )         (           .                       )
                                 (       INTERNET        )
                                 (                       )
                                 (                       )
                                 (                       )
                                 '-----------------------'
                           

### Square Corners / Intersections

                         |/
    ----+    +----+      +--
        |    |     \    / \
        +----+      +--+   

* Plus's at the end of lines
* 2 or more lines

### Rounded Corners
                               .
                               |\     
    ----.    .----.      .   . ' \   /
        |    |     \    / \ /|/   ' .  
        '----'      '--'   ' '    | |        

* Period ending horizontal line and diagonal/vertical below
* Period ending 
* Apostraphe ending ( hori | diag above) and ( vert | diag ) above
* Exactly 2 lines

### Jumps

       |        |        |
    ---)---  ---(---  ---^---
       |        |        |

* Left bracket at end of 4 lines (horizontal goes under)
* Right bracket at end of 4 lines (horizontal goes under)
* Caret at end of 4 lines (vertical goes under)
* Exactly 4 lines

### Arrowheads

    --->  <---   |   |   ^  
                 v   V   |   

* Right chevron ending horizontal line
* Left chevron ending horizontal line
* Lowercase v ending vertical line
* Uppercase v ending vertical line
* Caret ending vertical line

### Small Circles

    O  ( ) 
    
* Uppercase o
* Round-bracketted single space

### Small Squares

    []  [ ]
    
* Empty square brackets
* Square bracketted single space

### Titled Boxes

    +--------+   +---------------+
    |        |   | Title         |
    +--------+   +---------------+
    |        |   |               |
    |        |   |  Content      |
    +--------+   |               |
                 |               |
                 +---------------+

* Pair of enclosed rectangles
* One flush above other
* At least 10 wide
* Top box at least 3 high (single content line)
* Bottom box at least 4 high (2 content lines)

### Database Cylinder

    .-----.   .---------. 
    '-----'   '---------' 
    |     |   |         | 
    '-----'   | Content | 
              |         | 
              '---------'

* Enclosed, rounded top box
* Rounded, closing bottom line
* Bottom line flush to top box
* Top box exactly 2 high (no content line)
* Bottom box at least 3 high (single content line)
* At least 7 wide

### Document Symbol

    +-----+  +---------+  +---------+  
    |     |  |         |  |         |  
    |.-._.'  | Content |  |         |   
             |         |  |.-._.-._.'
             |.---.___.'

* Square box top
* Wave bottom, flush
* Wave pattern: `/\|(\.-+\._+)+\.'/`
* One or more 'waves', variable 'peak' and 'trough' widths
* At least 7 wide
* At least 3 high (single content line)

### Ellipses

      .--.       .-------.     
     /    \     /         \    
    '      '   /           \     
    |      |  '             '  
    '      '  |             |  
     \    /   |             |   
      '--'    '             '
               \           /
                \         /
                 '-------'

* Rounded, elongated octogon
