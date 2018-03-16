from subprocess import Popen, PIPE
from os import remove
from matrix import *

class PPMGrid(object):

    ############################################################################
    # original sauce
    ############################################################################

    #constants
    XRES = 500
    YRES = 500
    MAX_COLOR = 255
    RED = 0
    GREEN = 1
    BLUE = 2

    DEFAULT_COLOR = [0, 0, 0]

    def __init__( self, width = XRES, height = YRES ):
        self.screen = []
        self.width = width
        self.height = height
        for y in range( height ):
            row = []
            self.screen.append( row )
            for x in range( width ):
                self[y].append( PPMGrid.DEFAULT_COLOR[:] )

    def __getitem__(self, i):
        return self.screen[i]

    def __setitem__(self, i, val):
        self.screen[i] = val

    def __len__(self):
        return len(self.screen)

    def plot( self, color, x, y ):
        (x,y) = (int(x),int(y))
        newy = PPMGrid.YRES - 1 - y
        if ( x >= 0 and x < PPMGrid.XRES and newy >= 0 and newy < PPMGrid.YRES ):
            self[newy][x] = color[:]

    def clear( self ):
        for y in range( len(self) ):
            for x in range( len(self[y]) ):
                self[y][x] = PPMGrid.DEFAULT_COLOR[:]

    def save_ppm( self, fname ):
        f = open( fname, 'w' )
        ppm = 'P3\n' + str(len(self[0])) +' '+ str(len(self)) +' '+ str(PPMGrid.MAX_COLOR) +'\n'
        for y in range( len(self) ):
            row = ''
            for x in range( len(self[y]) ):
                pixel = self[y][x]
                row+= str( pixel[ PPMGrid.RED ] ) + ' '
                row+= str( pixel[ PPMGrid.GREEN ] ) + ' '
                row+= str( pixel[ PPMGrid.BLUE ] ) + ' '
            ppm+= row + '\n'
        f.write( ppm )
        f.close()

    def save_extension( self, fname ):
        ppm_name = fname[:fname.find('.')] + '.ppm'
        self.save_ppm( ppm_name )
        p = Popen( ['convert', ppm_name, fname ], stdin=PIPE, stdout = PIPE )
        p.communicate()
        remove(ppm_name)

    def display( self ):
        ppm_name = 'pic.ppm'
        self.save_ppm( ppm_name )
        p = Popen( ['display', ppm_name], stdin=PIPE, stdout = PIPE )
        p.communicate()
        remove(ppm_name)

    ############################################################################
    # line
    ############################################################################

    def draw_line( self, x0, y0, x1, y1, color ):
        if ( x1 < x0 ):
            (x0, x1) = (x1, x0)
            (y0, y1) = (y1, y0)
        a = y1 - y0
        b = x0 - x1
        (x,y) = (x0,y0)
        if ( 0 <= a <= -b ): # oct 1
            d = 2*a + b
            while ( x <= x1 ):
                self.plot( color, x, y)
                if ( d > 0 ):
                    y += 1
                    d += 2*b
                x += 1
                d += 2*a
            return
        if ( -b <= a ): # oct 2
            d = a + 2*b
            while ( y <= y1 ):
                self.plot( color, x, y)
                if ( d < 0 ):
                    x += 1
                    d += 2*a
                y += 1
                d += 2*b
            return
        if ( b <= a <= 0 ): # oct 8
            d = 2*a - b
            while ( x <= x1 ):
                self.plot( color, x, y)
                if ( d < 0 ):
                    y -= 1
                    d -= 2*b
                x += 1
                d += 2*a
            return
        if ( a <= b ): # oct 7
            d = a - 2*b
            while ( y >= y1 ):
                self.plot( color, x, y)
                if ( d > 0 ):
                    x += 1
                    d += 2*a
                y -= 1
                d -= 2*b
            return

    ############################################################################
    # matrix
    ############################################################################

    def draw_lines( self, matrix, color ):
        for c in range(matrix.cols//2):
            self.draw_line( matrix[c*2][0],
                            matrix[c*2][1],
                            matrix[c*2+1][0],
                            matrix[c*2+1][1],
                            color )
                            
    ############################################################################
    # transform
    # curves
    ############################################################################
    def parse_file( self, fname, color ):
        fopen = open(fname,'r')
        fread = fopen.read()
        fopen.close()

        t = Matrix.ident()
        e = Matrix(0,4)

        cmd = fread.split('\n')
        for i in range(len(cmd)):
            if ( i != len(cmd)-1 ):
                args = cmd[i+1].split()
            if ( cmd[i] == "line" ):
                e.add_edge(float(args[0]),float(args[1]),float(args[2]),
                           float(args[3]),float(args[4]),float(args[5]))
            elif ( cmd[i] == "ident" ):
                t = Matrix.ident()
            elif ( cmd[i] == "scale" ):
                t *= Matrix.scaler(float(args[0]),float(args[1]),float(args[2]))
            elif ( cmd[i] == "move" ):
                t *= Matrix.mover(float(args[0]),float(args[1]),float(args[2]))
            elif ( cmd[i] == "rotate" ):
                if ( args[0] == 'x' ):
                    t *= Matrix.rotx(math.radians(float(args[1])))
                elif ( args[0] == 'y' ):
                    t *= Matrix.roty(math.radians(float(args[1])))
                elif ( args[0] == 'z' ):
                    t *= Matrix.rotz(math.radians(float(args[1])))
            elif ( cmd[i] == "apply" ):
                e *= t
            elif ( cmd[i] == "clear" ):
                e = Matrix(0,4)
            elif ( cmd[i] == "display" ):
                self.clear()
                self.draw_lines(e, color)
                self.display()
            elif ( cmd[i] == "save" ):
                self.clear()
                self.draw_lines(e, color)
                self.save_extension(args[0])
            elif ( cmd[i] == "quit" ):
                return
            elif ( cmd[i] == "circle" ):
                e.add_circle(float(args[0]),float(args[1]),float(args[2]),
                             float(args[3]))
            elif ( cmd[i] == "bezier" or cmd[i] == "hermite" ):
                e.add_curve(float(args[0]),float(args[1]),
                            float(args[2]),float(args[3]),
                            float(args[4]),float(args[5]),
                            float(args[6]),float(args[7]),
                            0.001,cmd[i])
        

