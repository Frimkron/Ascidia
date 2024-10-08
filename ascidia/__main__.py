import argparse
import sys

from . import patterns
from .main import *


class FileOutContext:

    filename = None
    binary = False
    stream = None
    last_report_len = 0
    
    def __init__(self,filename, binary):
        self.filename = filename
        self.binary = binary
        
    def __enter__(self):
        self.stream = open(self.filename,"wb" if self.binary else "w")
        return self.stream
        
    def __exit__(self,extype,exvalue,traceback):
        self.stream.close()
        
    def report(self,message):
        sys.stdout.write("\b"*self.last_report_len)
        sys.stdout.write(message)
        sys.stdout.flush()
        self.last_report_len = len(message)
        
    
class StdOutContext:

    binary = False

    def __init__(self, binary):
        self.binary = binary
    
    def __enter__(self):
        return sys.stdout.buffer if self.binary else sys.stdout
        
    def __exit__(self,extype,exvalue,traceback): 
        pass
        
    def report(self,message): 
        pass
    
    
class FileInContext:
    
    def __init__(self,filename):
        self.filename = filename
        
    def __enter__(self):
        self.stream = open(self.filename,"r")
        return self.stream
        
    def __exit__(self,extype,exvalue,traceback):
        self.stream.close()
        
    
class StdInContext:
    
    def __enter__(self):
        return sys.stdin
        
    def __exit__(self,extype,exvalue,traceback):
        pass
    
    
def colour(s):
    if s.lower() in NAMED_COLOURS: return NAMED_COLOURS[s.lower()]
    bits = s.split(",")
    if len(bits) != 3: raise ValueError(s)
    for b in bits:
        if not( 0 <= float(b) <= 1):
            raise ValueError(s)
    return tuple(map(float,bits))


def opt_colour(s):
    if s == 'none':
        return None
    return colour(s)    


def main():

    fmtbyname = { 
        "png": PngOutput, 
        "svg": SvgOutput }
    fmtbyext = dict(
        sum([[(e,f) for e in f.EXTS] for f in fmtbyname.values()],[]))
    fmtdefault = PngOutput

    ap = argparse.ArgumentParser()
    ap.add_argument(
        "-o", "--outfile", default=None, 
        help="output file")
    ap.add_argument(
        "-f", "--foreground", default="black", type=colour,
        help="foreground colour")
    ap.add_argument(
        "-b", "--background", default="white", type=opt_colour,
        help="background colour")
    ap.add_argument(
        "-c", "--charheight", default="24", type=int,
        help="character height in pixels")
    ap.add_argument(
        "-t", "--type", default=None, choices=fmtbyname.keys(),
        help="output format")
    ap.add_argument(
        "-q", "--quiet", action="store_true",
        help="no progress output")
    ap.add_argument(
        "infile", default="-", nargs="?",
        help="input file")
    args = ap.parse_args()

    if args.infile == "-":
        inctx = StdInContext()
    else:
        inctx = FileInContext(args.infile)
    
    if args.type is not None:
        fmt = fmtbyname[args.type]
    elif args.outfile not in (None,"-") and "." in args.outfile:
        ext = args.outfile[args.outfile.rfind(".")+1:].lower()
        fmt = fmtbyext.get(ext,fmtdefault)
    else:
        fmt = fmtdefault

    if args.outfile == "-":
        outctx = StdOutContext(fmt.IS_BINARY)
    elif args.outfile is not None:
        outctx = FileOutContext(args.outfile, fmt.IS_BINARY)
    elif args.infile == "-":
        outctx = StdOutContext(fmt.IS_BINARY)
    else:
        name = args.infile
        extpos = name.rfind(".")
        if extpos != -1: name = name[:extpos]
        name += "." + fmt.EXTS[0]
        outctx = FileOutContext(name, fmt.IS_BINARY)
    
    prefs = OutputPrefs(args.foreground, args.background, args.charheight)
    
    with inctx as instream:
        ipt = instream.read()

    if not args.quiet:
        reporter = lambda x: outctx.report(
            "[{}] {}%".format(
                "#"*int(math.floor(x*10)) + ":"*int(math.ceil((1-x)*10)),
                int(x*100)))
    else:
        reporter = lambda x: None
    
    diagram = process_diagram(ipt, patterns.PATTERNS, reporter)
    if not args.quiet: outctx.report("\n")

    with outctx as outstream:
        fmt.output(diagram, outstream, prefs)


if __name__ == "__main__":
    main()
