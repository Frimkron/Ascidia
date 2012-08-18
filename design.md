% Ascii Diagram Tool
% Mark Frimston
% 2012-03-15

Motivation
----------

[Ditaa][1] is a neat tool for turning ascii-art diagrams into rendered images. 
This is great, but the syntax relies heavily on extra annotations for doing 
things like colours, box types and so on.

[1]: http://ditaa.org

[Ascii2svg][2] is a similar project written in PHP, inspired by Ditaa, but 
but which focuses on outputting to a scalable format - namely svg. It has nicer
rounded corner syntax. The author is fan of markdown, however Ascii2svg still 
suffers from the same syntax issue.

[2]: http://9vx.org/~dho/a2s/

[Markdown][3] is awesome both in its philosophy and its implementation. But it 
would be nice to be able to embed diagrams in it and have them transformed to 
a pretty format when converting the document to something that supports images.
The Markdown philosophy is that the raw text should be perfectly readable and 
formatting should not have to pollute the document with extra syntax. 
Markdown's syntax attempts to work on conventions that people already use and 
are familiar with, and would recognise the significance of in other peoples' 
documents.

[3]: http://daringfireball.net/projects/markdown/

[Pandoc-ditaa][4] is a quick perl script that someone wrote to pre-process a 
Pandoc document, extract code blocks marked as ditaa format, render them to 
images, and substitude them with image links in the document before it is 
converted. This is a great idea.

[4]: http://nichtich.github.com/ditaa-markdown/README.html

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
    |        |  [1]: { "a2s:type": "storage" }
    +--------+

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

    )    (        
    )    (                                  
    )    (                                  
                           
* Runs of 2 or more vertical left parentheses
* Runs of 2 or more vertical right parentheses

                               
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
        |    |     \    / \ /|/   : :  
        '----'      '--'   ' '    | |        
        
* Period joining 2 diag/vert lines below
* Period joining horiz line and diag/vert line below
* Apostraphe joining 2 diag/vert lines above
* Apostraphe joining horiz line and diag/vert line above
* Colon joining diag/vert line above and diag/vert line below
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

### Crows Feet

        |  |        |    -----
    ---<|  |>---    ^      V
        |  |      -----    |
        
* Left chevron with horizontal line to left and vertical to right
* Right chevron with horizontal line to right and vertical to left
* Carent with vertical line above an horizontal line below
* Upper/lowercase v with vertical line below and horizontal above

### Empty Diamond Association

                        |    -----
          |  |          ^      ^   
    ---< >|  |< >---    v      v   
          |  |        -----    |    

* Chevrons enclosing optional space with horizontal line on one side
  and vertical on the other
* Caret over upper/lower v with optional space between and vertical 
  line on one side, horizontal on the other
  
## Filled Diamond Association

                        |    -----
          |  |          ^      ^
    ---<#>|  |<#>---    #      #
          |  |          v      v
                      -----    |

* Chevrons enclosing hash with horizontal line on one side and 
  vertical on the other
* Caret over hash over v with with vertical line on one size and 
  horizontal on the other

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
                 |               |
                 |               |
                 +---------------+

* 2 or 3 of enclosed, stacked rectangles
* One flush above other
* At least 10 wide
* Top box at least 3 high (single content line)
* Bottom boxes at least 4 high each (2 content lines)

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

__TODO__: Wave is other way round
__TODO__: Stacked boxes

                            +---------+
    +-----+  +---------+  +---------+ | 
    |     |  |         |  |         | |  
    |.-._.'  | Content |  |         |_'  
             |         |  |.-._.-._.'
             |.---.___.'

* Square box top
* Wave bottom, flush
* Wave pattern: `/\|(\.-+\._+)+\.'/`
* One or more 'waves', variable 'peak' and 'trough' widths
* At least 7 wide
* At least 3 high (single content line)

### Large Circle

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

__TODO__ Proper circles e.g. state diagram
__TODO__ Diamonds
__TODO__ 3d Boxes
__TODO__ Stick figures
__TODO__ Crow's feet
__TODO__ Diamond line endings
__TODO__ Circlce line endings
__TODO__ Square line endings
__TODO__ Cloud bubbles
__TODO__ Folded corner documents
__TODO__ Stacked boxes
__TODO__ Computer symbol
__TODO__ IO rhombus
__TODO__ Points on lines using asterisk


Parsing
-------

What's the best way to parse a 2-dimensional character array? We can assume the
array is all held in memory at once - don't have to be concerned about 
lookaheads because we can access whatever cells we need as and when.

	 ____          +---+     .-----.
	/___/|  .-.   +---+|    (       )       .-.                     .---.
	|   ||  '-'   |   |+   (         )     ( A )     (  foo  )     (     )
	|___|/  '-'   +---+     (       )       '-'          |         (     )
	                         '-----'                     v          '---'
	                                                 (  bar  )
	        +---.                                                ^
	        |  |_\          .--.       ^                   are all files   Y      +------+
	        |    |         ( 12 )   < foo >   [ foo ]   <   ready to be   >--->---| blah |
	        +----+          '--'       v                   pre-processed?         +------+
	                                                             v
	                                                             |
	      <#>-- ^           /\       +----.   +-----+            v
	            #         /    \     |   |_\  |file |            |
	            v         \    /     |     |  |     |         .-----.
	            |           \/       '._.-.|  '._.-.|        ( stop  )
	    +===+                               +---+     .---.   '-----'
	   +---+"	 +----+ +-------------+    +---+|    .---.'
	   |   |+    |[  ]| |+-----------+|   +---+|+   .---.'|
	   +---+     +----+ ||           ||   |   |+    '---'|'
                 [    ] ||           ||   +---+     |   |'
                        |+-----------+|             '---'
                        +-------------+
                             |   |
                        +-------------+
                        |             |
                        +-------------+
