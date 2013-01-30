
from Ray import *
from Object import *
from Point import *

class Window:
	def __init__(self, x, y):
		self.xmax=float(x)
		self.ymax=float(y)
		self.viewpoint = Point(1,0,0)
		
		self.window = [[Tuple(0,0,0) for i in range(y)] for i in range(x)]
	
	def getRay(self, x,y):
		p = Point(.5+(x/self.xmax), (y/self.ymax)-0.5, 0.0)
		
		r = Ray()
		
		r.o=self.viewpoint
		r.d=Vector((self.viewpoint - p).v)
		
		return r
	
	def outputPPM(self):
		print("P3\n{} {}\n255".format(self.xmax, self.ymax))
		
		for i in range(int(self.xmax)):
			for j in range(int(self.ymax)):
				color = self.window[i][j].v
				color = [int(color[i]*255) for i in range(3)]
				print color, 
			
			print("")
	


class Tracer:
	def __init__(self, x, y):
		self.objects = []
		self.w = Window(x,y)
	
	def addObject(self, o):
		self.objects.append(o)
	
	def trace(self):
		for i in range(int(self.w.xmax)):
			for j in range(int(self.w.ymax)):
				close = float("inf")
				closeO = None
				r = self.w.getRay(i,j)
				r.d.normalize()
				for obj in self.objects:
					t = obj.intersect(r)
					if t<close and t>0:
						t=close
						closeO = obj
				
				if closeO != None:
					self.w.window[i][j][0]=1.0
				
t = Tracer(100,100)
t.addObject(Sphere( Point(0.0,0.0,-5.0), 2.0))

t.trace()

t.w.outputPPM()



