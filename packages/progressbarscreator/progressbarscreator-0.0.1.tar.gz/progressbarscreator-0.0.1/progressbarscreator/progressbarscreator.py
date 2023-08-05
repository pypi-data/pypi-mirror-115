class bcolors:
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    OKGREEN = '\033[92m'
    
class Progressbar():
	def __init__(self, titel, SymOn=0, SymOff=0, color=0, SMCOError=False):
		self.max_value = 35
		self.titel = titel
		sym_on = ["#", "*", "+"]
		sym_off = [" ", "-", "."]
		self.sym = (sym_on[SymOn], sym_off[SymOff])
		self.smc = SMCOError
		if color == 0:
			self.color = None
		elif color == 1:
			self.color = bcolors.OKGREEN
		elif color == 2:
			self.color = bcolors.WARNING
		elif color == 3:
			self.color = bcolors.FAIL
		else:
			self.color = None
			
	def update(self, val):
		value = int((self.max_value*val)/100)+1
		self.bar = f"{self.titel} ["
		for full in range(0, value):
			self.bar += self.sym[0]
		for empt in range(value, self.max_value):
			self.bar += self.sym[1]
		self.bar += "]"
		br = ""
		for sp in self.bar:
			br += " "
		print(br, end='\r')
		if val == 100:
			self.bar += "...done "
			if not self.color == None:
				print(self.color + self.bar + bcolors.ENDC, end='\r')
				print("")
			else:
				print(self.bar, end='\r')
				print("")
		else:
			self.bar += f": {val}%"
			if not self.color == None:
				print(self.color + self.bar + bcolors.ENDC, end='\r')
			else:
				print(self.bar, end='\r')
				
	def error(self, reason):
		br = ""
		for sp in self.bar:
			br += " "
		print(br, end='\r')
		self.bar = f"{self.titel} [ {reason} ]       "
		if not self.color == None and self.smc:
			print(self.color + self.bar + bcolors.ENDC, end='\r')
			print("")
		else:
			print(bcolors.FAIL + self.bar + bcolors.ENDC, end='\r')
			print("")
		
class Marker():
	def __init__(self, titel, mode=0,  reverse=False, color=0, SMCOError=False):
		self.state = 0
		self.titel = titel
		self.mark = f"{self.titel}: "
		mkr = [["|", "/", "-", "\\", 3], ["|", " |", "  |", " |", "|", 4]]
		self.mk = mkr[mode]
		self.count = 0
		if reverse:
			self.mk = list(reversed(self.mk))
			self.mk.append(self.mk[0])
			del self.mk[0]
		self.smc = SMCOError
		if color == 0:
			self.color = None
		elif color == 1:
			self.color = bcolors.OKGREEN
		elif color == 2:
			self.color = bcolors.WARNING
		elif color == 3:
			self.color = bcolors.FAIL
		else:
			self.color = None
			
	def update(self):
		mrk = ""
		for sp in self.mark:
			mrk += " "
		print(mrk, end='\r')
		self.mark = f"{self.titel}: {self.mk[self.state]}"
		self.state += 1
		self.count += 1
		if self.state > self.mk[-1]:
			self.state = 0
		if not self.color == None:
			print(self.color + self.mark + bcolors.ENDC, end='\r')
		else:
			print(self.mark, end='\r')
			
	def stop(self, Message="...done"):
		mrk = ""
		for sp in self.mark:
			mrk += " "
		print(mrk, end='\r')
		self.mark = f"{self.titel}:{Message}"
		if not self.color == None:
			print(self.color + self.mark + bcolors.ENDC, end='\r')
			print("")
		else:
			print(self.mark, end='\r')
			print("")
		
	def error(self, reason):
		mrk = ""
		for sp in self.mark:
			mrk += " "
		print(mrk, end='\r')
		self.mark = f"{self.titel}:...{reason}"
		if not self.color == None and self.smc:
			print(self.color + self.mark + bcolors.ENDC, end='\r')
			print("")
		else:
			print(bcolors.FAIL + self.mark + bcolors.ENDC, end='\r')
			print("")

def Porange(message):
	'''Um einen teil in einem Print befehl Orange zu färben'''
	return bcolors.WARNING + message + bcolors.ENDC
	
def Pred(message):
	'''Um einen teil in einem Print befehl Rot zu färben'''
	return bcolors.FAIL + message + bcolors.ENDC
	
def Pgreen(message):
	'''Um einen teil in einem Print befehl Grün zu färben'''
	return bcolors.OKGREEN + message + bcolors.ENDC
	
def info():
	print("progress Version: 0.01 ;)")