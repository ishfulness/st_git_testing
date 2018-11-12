
import glob









def rho(k,err):
	beff = 0.0075

	dollars = round(((k-1)/k)/beff,7)

	up = round( (((k+err)-1)/(k+err))/beff - dollars   ,7)
	dn = round(-((((k-err)-1)/(k-err))/beff - dollars) ,7)

	return[dollars,up,dn]




def parse():
	print('todo')

def findfiles():
	results = []
	s0rw = []
	s500rw = []
	s1000rw = []
	
	r0sw = []
	r500sw = []
	r1000sw = []

	path = 'K:/AT/Sheetpy/outputs/*'

	for name in glob.glob(path+'.o'):

		shim,reg,k,err = parsefile(name)
		dol,up,dn = rho(k,err)

		# Stupid check
		if dol<5:
			results.append([shim,reg,dol,up,dn])

			if shim == 0:
				s0rw.append([shim,reg,dol,up,dn])
			if shim == 500:
				s500rw.append([shim,reg,dol,up,dn])
			if shim == 1000:
				s1000rw.append([shim,reg,dol,up,dn])
			if reg == 0:
				r0sw.append([shim,reg,dol,up,dn])
			if reg == 500:
				r500sw.append([shim,reg,dol,up,dn])
			if reg == 1000:
				r1000sw.append([shim,reg,dol,up,dn])


	createcsv(normalize(results))
	createcsvsep([s0rw,s500rw,s1000rw,r0sw,r500sw,r1000sw])



def normalize(data):
	minvalue = 1
	for item in data:
		print(item)
		if item[2]<minvalue:
			minvalue = item[2]

	newdata = []
	for item in data:
		newdata.append([item[0],item[1],round(item[2]-minvalue,7),item[3],item[4]])

	return newdata


def createcsv(data):
	datastring = 'shim,reg,dol,up,dn\n'
	print(data)
	for line in data:
		for item in line:
			datastring+=f'{item},'
		datastring = datastring[:-1]
		datastring+='\n'

	print(datastring)

def createcsvsep(indata):
	# Normalize
	r0sw = normalize(indata[0])
	r500sw = normalize(indata[1])
	r1000sw = normalize(indata[2])
	s0rw = normalize(indata[3])
	s500rw = normalize(indata[4])
	s1000rw = normalize(indata[5])


	datadata = [r0sw,r500sw,r1000sw,s0rw,s500rw,s1000rw]

	for csv in datadata:
		datastring = 'shim,reg,dol,up,dn\n'
		for line in csv:
			for item in line:
				datastring+=f'{item},'
			datastring = datastring[:-1]
			datastring+='\n'

		print(datastring)




def parsefile(file):
	# '''''error handling'''''
	finalresult = 999
	finalerror = 111
	


	# Open file
	with open(file,'r') as outputfile:
		ofile = outputfile.readlines()
	
	for line in ofile:
		if '!SHIM' in line:
			shim = round(float(line.split()[4])*(1000/38.1),3)
		if '!REG' in line:
			reg = round(float(line.split()[4])*(1000/38.1),3)




		if 'final result' in line:
			finalresult = round(float(line.split()[2]),7)
			finalerror  = round(float(line.split()[3]),7)


	return([shim,reg,finalresult,finalerror])

findfiles()

