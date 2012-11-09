Ascii Diagram Converter
=======================

Facilitates the creation of technical diagrams using ascii art.

* [Usage](#usage)
* [Credits and Licence](#credits-and-licence)
** TODO **

Usage
-----

`asciidi [options] [file]`

### Positional Arguments

`file`

Path to the input file to read. Use `-` to read from standard input. This is 
the default.

### Options

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
width and height of the output. Defauts to 24.

** TODO **

Credits and Licence
-------------------

Written by Mark Frimston

* Project page: ** TODO **
* Homepage: <http://markfrimston.co.uk>
* Email: <mfrimston@gmail.com>
* Twitter: [@frimkron](http://twitter.com/frimkron)

Licenced under the MIT Licence - see source for full text of this licence.
