import sys
import re
class rut:
	"""Usage:
		r=rut.rut("10.253.930-3")
		print "validando 10.253.930-3:" , r.validate()
	or:
		r.rut("")
		r.setBody("10253930")
		r.getDV()
	"""
	data=""
	body=""
	dv  =""

	def __str__(self):
		if not self.body:
			self.clear()
			self.split()
		return self.getFormated()
	def __init__(self,data):
		self.data = str(data.lower())
		self.clear()
		self.split()

	def clear(self):
		self.data = self.data.replace(".","").replace("-","")
		self.data = re.sub("^0*","",self.data)
		return self.data

	def setBody(self,body):
		self.body = body

	def split(self):
		self.body = self.data[0:-1]
		self.dv   = self.data[-1:]

	def getDV(self):
		serie_multiplicadora = [2,3,4,5,6,7]*3 # la repetimos un par de veces para no quedarnos cortos de digitos
		suma = 0
		j=0
		for i in range(len(self.body)-1,-1,-1):
			#print suma, "+=", int(self.body[i]) ,"*",serie_multiplicadora[j]
			suma += int(self.body[i]) * serie_multiplicadora[j]
			j+=1
		dv_value= 11 - (suma % 11)
		if dv_value==11:
			return "0"
		if dv_value==10:
			return "k"
		else:
			return dv_value.__str__()
	def isValid(self):
		if not self.body:
			self.clear()
			self.split()
		if self.dv != self.getDV():
			print "self.dv: ",self.dv
			print "self.getDV(): ",self.getDV()
			return False
		else:
			return True
	def getFormated(self):
		resp = ""
		b = self.body[:]
		while len(b)>3:
			if len(resp):
				resp = b[-3:] + "." + resp
			else:
				resp = b[-3:]
			b = b[0:-3]
		if len(b):
			resp = b +"." + resp
		return resp + "-" + self.dv

	def validate(self):
		if not self.isValid():
			raise Exception('Rut Invalido')


#(cuerpo,digver) = rut.split("-")
#print suma
#print 11- (suma % 11)

#if len(sys.argv)<2:
#	rut = "10253930-3"
#else:
#	rut = sys.argv[1]
#
#rut = clearRut(rut)
