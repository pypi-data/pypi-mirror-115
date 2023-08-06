from os import linesep
from .from_cp import from_cp
from .to_svg import to_svg
    
def cp2svg(infile, outfile, margin=10):
    cp = from_cp(infile)

    svgString = to_svg(cp, margin)
    
    with open(outfile, 'w') as im:
        im.write(svgString)
