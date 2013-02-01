
from Ray import *
from Object import *
from Point import *
from Light import *
from random import random

class Window:
	def __init__(self, x, y):
		self.xmax=float(x)
		self.ymax=float(y)
		self.viewpoint = Point(0,0,.9)
		
		self.window = [[Tuple(0,0,0) for i in range(y)] for i in range(x)]
	
	def getRay(self, x,y):
		p = Point((x/self.xmax)-0.5, (y/self.ymax)-0.5, 0.0)
		
		r = Ray()
		
		r.o=self.viewpoint
		r.d=Vector(*(p-self.viewpoint).v)
		
		return r
	
	def outputPPM(self):
		print("P3\n{} {}\n255".format(int(self.xmax), int(self.ymax)))
		
		for i in range(int(self.xmax)):
			for j in range(int(self.ymax)):
				color = self.window[i][j].v
				color = [min(int(color[k]*255.0), 255) for k in range(3)]
				print "{} {} {} ".format(color[0],color[1], color[2]),  
			
			print("")
	


class Tracer:
	def __init__(self, x, y):
		self.objects = []
		self.lights = []
		self.w = Window(x,y)
		self.recursionLimit=10
	
	def addObject(self, o):
		self.objects.append(o)	
	def addLight(self, l):
		self.lights.append(l)
	
	def _trace(self, r, intensityList, recursion):
		r.d.normalize()
		close = float("inf")
		closeObj = None
		
		for obj in self.objects: #find the closest intersection
			t = obj.intersect(r)
			if t<close and t>0.0:
				close = t
				closeObj = obj
		
		if closeObj != None: # if there was in fact an intersection do this...
			close-=.000001
			rr,normal = closeObj.getReflectedNormal(r, close) #calculate reflected + normal vector
			intersectPoint = rr.o
			
			intensityList.append(IntensityRecord(closeObj.color))
			
			for l in self.lights:
				inshade = False
				Lray = Ray(intersectPoint, Vector(*(l.pos-intersectPoint).v))
				Ldist = Lray.d.length()
				Lray.d.normalize()
				#print "lray: ", Lray.d.v, Lray.o.v
				for obj in self.objects:
					odist = obj.intersect(Lray)
					if odist>0.001:
						#print odist
						inshade = True
						
				
				if not inshade:
					#Lray.d.negate()
					Lscale = normal.dot(Lray.d)
					#print "normal dot lray", normal.dot(Lray.d)
					#print "normal: ", normal.v, "Lray.d", Lray.d.v
					if Lscale >0.01:
						intensityList[-1].intensity+= l.intensity.scale(Lscale)
				else:
					intensityList[-1].intensity+=Tuple(.1,.1,.1)
			
			#so after we do all the lights then we can use the reflected ray to trace again
			#if recursion < self.recursionLimit:
			#	self._trace(rr, intensityList, recursion+1)
					
					
	
	def trace(self):
		for i in range(int(self.w.xmax)):
			for j in range(int(self.w.ymax)):
				#print i,j, 
				r = self.w.getRay(i,j)
				intensityList = []
				self._trace(r, intensityList, 8)
				intensity = Tuple(0.0,0.0,0.0)
				while( len(intensityList) > 0 ):
					curin = intensityList.pop()
					#print curin.intensity.v
					intensity+= curin.getIntensity()
				
				self.w.window[i][j] = intensity
				
				
t = Tracer(700,700)
for i in range(10):
	t.addObject(Sphere( Point(2.5-random()*5.,2.5-random()*5,-13.0+random()*5), random()*0.3+1., 
		Tuple(random()*.5+.4,random()*.5+.4,random()*.5+.4)))
#t.addObject(Sphere( Point(1.0,0.0,-10.0), 2.0, Tuple(1,0,0)))
#t.addObject(Sphere( Point(-3.0,0.0,-10.0), 2.0, Tuple(1,0,1)))
#t.addObject(Sphere( Point(3.5,-0.0,-8.0), .25, Tuple(.2,.5,1)))
#t.addLight(Light(Point(-10,-10,-15.5), Tuple(.4,.4,.4)))
t.addLight(Light(Point(10.,10.,45.), Tuple(.8,.8,.8)))

t.trace()

t.w.outputPPM()



