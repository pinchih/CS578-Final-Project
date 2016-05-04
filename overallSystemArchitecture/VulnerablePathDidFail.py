from bs4 import BeautifulSoup
import os, sys, json

#global obj that will be output to JSON
obj = None

#dumps json for given object
def to_JSON(obj):
	return json.dumps(obj, default=lambda o: o.__dict__, sort_keys=True, indent=4)

#process each phase 1 analysis
def processFD(inputFileName):
	global obj
	#open given file
	fullpath = '~/didfail/toyapps/out/' + inputFile
	with open(fullpath,'r') as inputFile:
		#beautiful soup to get package name
		soup = BeautifulSoup(inputFile, "xml")
		#get package name
		package = soup.results['package'].strip()
		#get name of application
		name = inputFileName.split('.')[0].strip()
		#check if application already exists in object
		foundMatch = False
		for node in obj['nodes']:
			if node['Name'] == name:
				node['package'] = package
				foundMatch = True
				break
		#if input didn't have this app, add it
		if not foundMatch:
			app = {}
			app['Name'] = name
			app['package'] = package
			obj['nodes'].append(app)
		inputFile.close()

#process flows.out. this is where I'll generate the links
def processPhaseTwo(inputFile):
	global obj
	#read first line
	line = inputFile.readline()
	#read down until intents definition
	while line != '--------------------':
		line = inputFile.readline().strip()

	#examine all the intents
	while line:
		#if it's just regular intent
		if '### \'Intent(' in line:
			#first process this line:
			edge = {}
			edge['resources'] = []
			line = line.split('Intent(')[1]
			args = line.split('),')
			for arg in args:
				arg = arg.strip()
				if 'tx=' in arg:
					arg = arg.split('tx=(\'')[1].strip()
					arg = arg.split('\',')[0].strip()
					edge['source'] = arg
				if 'rx=' in arg:
					arg = arg.split('rx=(\'')[1].strip()
					arg = arg.split('\',')[0].strip()
					edge['dest'] = arg
				if 'intent_id' in arg:
					arg = arg.split('intent_id=\'')[1].strip()
					arg = arg.split('\')')[0].strip()
					edge['id'] = arg

			#get a new line:
			line = inputFile.readline().strip()
			#we've processed the first line, let's look at all the sources now
			while ('### \'Intent(' not in line) and (line != '--------------------'):
				if 'Src:' in line:
					source = {}
					line = line.split('<')[1].strip()
					line = line.split('>')[0].strip()
					edge['resources'].append(line)
				line = inputFile.readline().strip()

			#add the link we built
			link = {}
			link['id'] = edge['id']
			link['byTool'] = 'DidFail'
			link['description'] = 'This is a description of vulnerable path' 
			link['dataFlow'] = False
			for i in range(len(obj['nodes'])):
				if 'package' in obj['nodes'][i].keys():
					if obj['nodes'][i]['package'] == edge['source']:
						link['source'] = i
					elif obj['nodes'][i]['package'] == edge['dest']:
						link['target'] = i
			link['resources'] = edge['resources']
			obj['links'].append(link)
		elif '### \'IntentResult(' in line:
			line = inputFile.readline().strip()
			print 2
		else:
			line = inputFile.readline().strip()

#main driver function
def main(args):
	global obj
	
	#open generated json file and load into object
	with open('../graph.json','r') as jsonFile:
		obj = json.load(jsonFile)
		jsonFile.close()

	#open output file
	with open('../graph.json','w+') as outputFile:
		#look at all didfail FD outputs
		for filename in os.listdir('./'):
			if filename.endswith('.fd.xml'):
				processFD(filename)

		#now look at phase 2 flows output
		with open('./flows.out','r') as flowsOut:
			processPhaseTwo(flowsOut)
			flowsOut.close()

		#write to output file
		outputFile.write(to_JSON(obj))
		outputFile.close()

main(sys.argv);
