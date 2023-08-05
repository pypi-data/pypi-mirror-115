#!/usr/bin/python3

from .__init__ import __doc__ as description, __version__ as version
from os import popen
from os.path import abspath, expanduser, exists, isfile
from sys import argv, exit
from argparse import ArgumentParser as Parser, RawDescriptionHelpFormatter as Formatter
from pdfrw import PdfReader, PdfWriter
from libfunx import ask, get_source, get_target

# classes

class args:
    "container for arguments"
    pass

# main

def swapdf(argv):
    "SWAP PDF pages after scan of a two-sided sheet pack through a one-sided feeder"

    # get arguments
    parser = Parser(prog="swapdf", formatter_class=Formatter, description=description)
    parser.add_argument("-V", "--version", action="version", version=f"swapdf {version}")
    parser.add_argument("-v", "--verbose", action="store_true", help="show what happens")
    parser.add_argument("-y", "--yes",  action="store_true", help="overwrite existing target file (default: ask)")
    parser.add_argument("-n", "--no",  action="store_true", help="don't overwrite existing target file (default: ask)")
    parser.add_argument("-o", "--open",  action="store_true", help="at end open the target file for check and print (default: ask)")
    parser.add_argument("-q", "--quit",  action="store_true", help="at end don't open the target file for check and print (default: ask)")
    parser.add_argument("source", nargs="?", help="source file with pages from scanner 1 3 5 ... 6 4 2, default = 'Scanned Document.pdf'")
    parser.add_argument("target", help="target file with swapped pages 1 2 3 4 5 6 ...")
    parser.parse_args(argv[1:], args)
    args.source = args.source or 'Scanned Document.pdf'
    if args.verbose:
        for k, v in sorted(args.__dict__.items()):
            if not k.startswith('_'):
                print(f'{k} = {v!r}')

    # check arguments
    if args.yes and args.no:
        exit("ERROR: you can't give both -y/--yes and -n/--no arguments")
    if args.open and args.quit:
        exit("ERROR: you can't give both -o/--open and -q/--quit arguments")
    source = get_source(args.source, ".pdf")
    target = get_target(args.target, ".pdf", yes=args.yes, no=args.no)
    if source == target:
        exit(f"ERROR: source = {source!r} = target, but they can't be the same")
    
    # check source content
    try:
        pages = PdfReader(source).pages
        assert pages
    except:
        exit(f"ERROR: source file {source!r} doesn't contain any pages")
    source_npages = len(pages)
    if source_npages % 2:
        exit(f"ERROR: pages in source file {source!r} must be even but they are {source_npages} which is odd")

    # source --> target
    writer = PdfWriter()
    if args.verbose:
        print("copied:", end=" ")
    for j in range(source_npages // 2):
        writer.addpage(pages[j]) # odd page
        writer.addpage(pages[-j-1]) # even page
        if args.verbose:
            print(j + 1, source_npages - j, end=" ")
    try:
        writer.write(target)
    except:
        exit(f"\nERROR: error writing output file {target!r}")
    if args.verbose:
        print(f"\ncopied {source_npages} pages from source {source!r} ...\n... into target {target!r}")
    if args.open or not args.quit and ask(f"Open the target file {target!r} for check and print or Quit? (o=open, q=quit) --> ", "oq") == "o":
        popen(f"xdg-open {target!r}")
        
def main():
    try:
        swapdf(argv)
    except KeyboardInterrupt:
        print()

if __name__ == "__main__":
    main()
