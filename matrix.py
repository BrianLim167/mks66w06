import math


class Matrix(object):

    #m1 * m2 -> m2
    @staticmethod
    def mult( m1, m2 ):
        m = Matrix(0, m1.rows)
        for c in range( m2.cols ):
            m.append([])
            for r in range( m1.rows ):
                m[-1].append( 0 )
                for i in range(m1.cols):
                    m[c][r] += (m1[i][r] * m2[c][i])
        return m

    @staticmethod
    def ident(s=4):
        m = Matrix(s,s)
        for c in range( m.cols ):
            m[c][c] = 1
        return m

    @staticmethod
    def mover(x,y,z):
        m = Matrix.ident(4)
        m[3][0] = x
        m[3][1] = y
        m[3][2] = z
        return m

    @staticmethod
    def scaler(x,y,z):
        m = Matrix.ident(4)
        m[0][0] = x
        m[1][1] = y
        m[2][2] = z
        return m

    @staticmethod
    def rotx(a):
        m = Matrix.ident(4)
        a = math.radians(a)
        m[1][1] = math.cos(a)
        m[1][2] = math.sin(a)
        m[2][1] = -math.sin(a)
        m[2][2] = math.cos(a)
        return m
    
    @staticmethod
    def roty(a):
        m = Matrix.ident(4)
        a = math.radians(a)
        m[2][2] = math.cos(a)
        m[2][0] = math.sin(a)
        m[0][2] = -math.sin(a)
        m[0][0] = math.cos(a)
        return m
    
    @staticmethod
    def rotz(a):
        m = Matrix.ident(4)
        a = math.radians(a)
        m[0][0] = math.cos(a)
        m[0][1] = math.sin(a)
        m[1][0] = -math.sin(a)
        m[1][1] = math.cos(a)
        return m

    @staticmethod
    def bezier():
        m = Matrix(4,4)
        m[0] = [-1, 3,-3, 1]
        m[1] = [ 3,-6, 3, 0]
        m[2] = [-3, 3, 0, 0]
        m[3] = [ 1, 0, 0, 0]
        return m

    @staticmethod
    def hermite():
        m = Matrix(4,4)
        m[0] = [ 2,-3, 0, 1]
        m[1] = [-2, 3, 0, 0]
        m[2] = [ 1,-2, 1, 0]
        m[3] = [ 1,-1, 0, 0]
        return m
    
    def __init__(self, cols = 4, rows = 4):
        if ( isinstance(cols, list) ):
            self.ary = cols
            self.cols = len(cols)
            self.rows = len(cols[0])
            return
        self.ary = []
        self.rows = rows
        self.cols = 0
        for c in range( cols ):
            self.append( [] )
            for r in range( rows ):
                self[c].append( 0 )

    def __mul__(self, other):
        return Matrix.mult(self,other)

    def __imul__(self, other):
        self = other * self
        return self

    def __getitem__(self, i):
        return self.ary[i]

    def __setitem__(self, i, val):
        self.ary[i] = val
        return self.ary[i]

    def __len__(self):
        return len(self.ary)

    def __str__(self):
        s = ""
        for r in range(self.rows):
            for c in range(self.cols):
                s += ("     "+str(self[c][r]))[:10][-5:]
                s += ' '
            s += '\n'
        return s

    def append(self, val):
        if ( isinstance(val, list) ):
            self.ary.append(val)
            self.cols += 1
            return
        if ( isinstance(val, Matrix) ):
            for c in range(val.cols):
                self.append(val[c])
            return

    def print( self ):
        print(self)

    def __arghandler( *func ):
        pass

    def add_edge( self, x0, y0, z0, x1, y1, z1 ):
        self.add_point(x0,y0,z0)
        self.add_point(x1,y1,z1)

    def add_point( self, x, y, z=0 ):
        self.append([x,y,z,1])

    def add_circle( self, cx, cy, cz, r, step=0.001, connect=True ):
        t = 0
        m = Matrix(0,4)
        while ( t <= 1 ):
            a = math.radians(360*t)
            m.add_point(cx + r*math.cos(a), cy + r*math.sin(a), cz)
            a = math.radians(360*(t+step))
            if ( connect ):
                m.add_point(cx + r*math.cos(a), cy + r*math.sin(a), cz)
            t += step
        if ( not connect ):
            a = math.radians(360*t)
            m.add_point(cx + r*math.cos(a), cy + r*math.sin(a), cz)
        self.append(m)

    def add_curve( self, x0, y0, x1, y1, x2, y2, x3, y3, step, curve_type ):
        if ( curve_type.lower() == "bezier" ):
            curve_type = Matrix.bezier
        elif ( curve_type.lower() == "hermite" ):
            curve_type = Matrix.hermite
        x_coeff = curve_type() * Matrix([[x0,x1,x2,x3]])
        y_coeff = curve_type() * Matrix([[y0,y1,y2,y3]])
        t = 0
        m = Matrix(0,4)
        while ( t <= 1 ):
            x = x_coeff[0][0]*t**3 + x_coeff[0][1]*t**2 + x_coeff[0][2]*t + x_coeff[0][3]
            y = y_coeff[0][0]*t**3 + y_coeff[0][1]*t**2 + y_coeff[0][2]*t + y_coeff[0][3]
            m.add_point(x,y,0)
            x = x_coeff[0][0]*(t+step)**3 + x_coeff[0][1]*(t+step)**2 + x_coeff[0][2]*(t+step) + x_coeff[0][3]
            y = y_coeff[0][0]*(t+step)**3 + y_coeff[0][1]*(t+step)**2 + y_coeff[0][2]*(t+step) + y_coeff[0][3]
            m.add_point(x,y,0)
            t += step
        self.append(m)

    def add_box( self, x, y, z, width, height, depth ):
        a, b, c = x+width, y-height, z-depth

        self.add_point(x,y,z)
        self.add_point(a,y,z)

        self.add_point(a,y,z)
        self.add_point(a,b,z)

        self.add_point(a,b,z)
        self.add_point(x,b,z)

        self.add_point(x,b,z)
        self.add_point(x,y,z)

        
        self.add_point(x,y,c)
        self.add_point(a,y,c)

        self.add_point(a,y,c)
        self.add_point(a,b,c)

        self.add_point(a,b,c)
        self.add_point(x,b,c)

        self.add_point(x,b,c)
        self.add_point(x,y,c)


        self.add_point(x,y,z)
        self.add_point(x,y,c)
        
        self.add_point(a,y,z)
        self.add_point(a,y,c)
        
        self.add_point(a,b,z)
        self.add_point(a,b,c)
        
        self.add_point(x,b,z)
        self.add_point(x,b,c)

    def add_sphere( self, cx, cy, cz, r, step=0.02 ):
        m = Matrix.sphere(cx,cy,cz, r, step)
        for i in range(m.cols):
            self.append(m[i])
            n = m[i].copy()
            n[2] += 1
            self.append(n)

    @staticmethod
    def sphere( cx, cy, cz, r, step=0.02 ):
        m = Matrix(0,4)
        t = 0
        rot = Matrix.roty(360 * step)
        while ( t <= 1 ):
            m.add_circle(0,0,0, r, step, False)
            m *= rot
            t += step
        m *= Matrix.mover(cx, cy, cz)
        return m

    def add_torus( self, cx, cy, cz, r, step=0.02 ):
        m = Matrix.torus(cx,cy,cz, r, step)
        for i in range(m.cols):
            self.append(m[i])
            n = m[i].copy()
            n[2] += 1
            self.append(n)

    @staticmethod
    def torus( cx, cy, cz, r0, r1, step=0.02 ):
        m = Matrix(0,4)
        t = 0
        rot = Matrix.roty(360 * step)
        while ( t < 1 ):
            m.add_circle(r1,0,0, r0, step, False)
            m *= rot
            t += step
        m *= Matrix.rotx(90)
        m *= Matrix.mover(cx, cy, cz)
        return m
            
        
