from Point import Point
from Vector import Vector
from Tuple import Tuple
from Ray import Ray
import math

class Object(object):
	def __init__(self, color, Kdiffuse=1.0, Kspecular=0.0, shinyness=1.0):
		self.diffuse=Kdiffuse
		self.specular=Kspecular
		self.shinyness=shinyness
		self.color = color
	
	def intersect(self, ray):
		pass

class Sphere(Object):
	def __init__(self, origin, r, color, diffuse=1.0, specular=0.0, shinyness=1.0):
		super(Sphere, self).__init__(color, diffuse, specular, shinyness)
		self.origin = origin
		self.r = r
	
	def intersect(self, ray):
		# a is always 1 since r.d is normalized!
		# pg 37 - Introduction to Ray Tracing
		dist = (ray.o-self.origin)
		b=(ray.d*dist)
		b = b[0]+b[1]+b[2]
		b*=2.0
		
		c = dist[0]**2+dist[1]**2+dist[2]**2 - self.r**2
		
		disc = b*b-4.0*c
		if disc <= 0:
			return -1
		
		disc = math.sqrt(disc)
		
		t0 = (-b-disc)/2.0
		if t0 > 0:
			return t0
		t1 = (-b+disc)/2.0
		
		return t1
		
	def getReflectedNormal(self, ray, t):
		# need to find the point, then find normal at point
		#then get reflected ray, origin=pt
		p = Point(*(ray.d.scale(t)).v )+ray.o
		normal = Vector(*(p-self.origin).v)

		normal.normalize()
		
		rr = Ray()
		
		rr.o=p
		
		rr.d = ray.d - normal.scale(2*ray.d.dot(normal))
		rr.d=Vector(*rr.d.v)
		return rr, normal
		
		
