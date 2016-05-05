#!/usr/bin/python
from bs4 import BeautifulSoup
from random import randint
import json
import sys,os
import argparse

class Application:
	
	def __init__(self,name):
		self.name = name
		self.componentList = []
		self.intentList = []
		self.allowedActions = []

class Component:
	
	def __init__(self,type,cName,requiredPermissions,intentFilter,propagatedPermissions):
		self.type = type
		self.cName = cName
		self.requiredPermissions = requiredPermissions
		self.intentFilter = intentFilter
		self.propagatedPermissions = propagatedPermissions
		self.linkToList = []
		
class Filter:
	
	def __init__(self,actions,categories,pathData):
		self.actions = actions
		self.categories = categories
		self.pathData = pathData

class Intent:
	
	def __init__(self,calledAt,sender,component,action,dataType,scheme,extra,sensitiveData,consumerMethod,id,random):
		self.calledAt = calledAt
		self.sender = sender
		self.component = component
		self.action = action
		self.dataType = dataType
		self.scheme = scheme
		self.extra = extra
		self.sensitiveData = sensitiveData
		self.consumerMethod = consumerMethod
		self.id = id
		self.random = random

def xmlToJSON(xml):
	
	# Read from xml file
	soup = BeautifulSoup(open(xml),"xml")

	# Get the application name
	appName = soup.find_all("name")[-1].string

	ComponentList = []

	totalActionsAllowed = []
	
	usesPermissionList = []
	
	for p in soup.find_all("permission"):
		 usesPermissionList.append(p.string.strip('\"'))
		

	# Extract components
	for c in soup.find_all("Component"):
		
		actionList = []
		
		for f in c.find_all("filter"):
		    for a in f.find_all("actions"):
				actionList.append(str(a.string))										
				totalActionsAllowed.append(str(a.string))
				
		actions = actionList
			
		try :
			categories = c.find("filter").categories.string.strip('\"').replace("\"", "")
		except AttributeError:
			categories = "None"

		try :
			pathData = c.find("filter").pathData.string.strip('\"').replace("\"", "")
		except AttributeError:
			pathData = "None"
		
		filterOject = Filter(actions,categories,pathData)
		
		try :
			componentType = c.type.string.strip('\"').replace("\"", "")
		except AttributeError:
			componentType = "None"
		
		try :
			componentName = c.find("name").string.strip('\"').replace("\"", "")
		except AttributeError:
			componentName = "None"
			
		try :
			RP = c.RequiredPermissions.string.strip('\"').replace("\"", "")
		except AttributeError:
			RP = "None"
			
		try :
			PP = c.PropagatedPermissions.string.strip('\"').replace("\"", "")
		except AttributeError:
			PP = "None"
		
		componentObject = Component(componentType, componentName, RP, filterOject, PP)
		ComponentList.append(componentObject)

	intentList = []
	totalIntents = []
	
	for i in soup.find_all("Intent"):
		
		try :
			calledAt = i.calledAt.string.strip('\"').replace("\"", "")
		except AttributeError:
			calledAt = "None"
		
		try :
			sender = i.sender.string.strip('\"').replace("\"", "")
		except AttributeError:
			sender = "None"
			
		try :
			component = i.component.string.strip('\"').replace("\"", "")
		except AttributeError:
			component = "None"

		try :
			action = i.action.string.strip('\"').replace("\"", "")
		except AttributeError:
			action = "None"
			
		try :
			dataType = i.dataType.string.strip('\"').replace("\"", "")
		except AttributeError:
			dataType = "None"
		
		try :
			scheme = i.scheme.string.strip('\"').replace("\"", "")
		except AttributeError:
			scheme = "None"
			
		try :
			extra = i.extra.string.strip('\"').replace("\"", "")
		except AttributeError:
			extra = "None"
			
		try :
			sensitiveData = i.sensitiveData.string.strip('\"').replace("\"", "")
		except AttributeError:
			sensitiveData = "None"
			
		try :
			consumerMethod = i.consumerMethod.string.strip('\"').replace("\"", "")
		except AttributeError:
			consumerMethod = "None"
			
		intentID = i.id.string
			
		try :
			random = i.random.string.strip('\"').replace("\"", "")
		except AttributeError:
			random = "None"
		
		intentObject = Intent(calledAt, sender, component, str(action.strip('\"')), dataType, scheme, extra, sensitiveData, consumerMethod, intentID, random)
		
		intentList.append(intentObject)
		totalIntents.append(intentObject)
		
	a = Application(appName)
	a.componentList = ComponentList
	a.intentList = totalIntents
	a.allowedActions = totalActionsAllowed
	
	AppList.append(a)
	
	# Convert to JSON

	jsonStr = ""

	jsonStr = jsonStr + '\"Name\":\"'+ appName +'\",'

	# Components

	'''
		# component
		self.type = type
		self.cName = cName
		self.requiredPermissions = requiredPermissions
		self.intentFilter = intentFilter
		self.propagatedPermissions = propagatedPermissions
		
		# filter
		self.actions = actions
		self.categories = categories
		self.pathData = pathData

		# intent 
		self.calledAt = calledAt
		self.sender = sender
		self.component = component
		self.action = action
		self.dataType = dataType
		self.scheme = scheme
		self.extra = extra
		self.sensitiveData = sensitiveData
		self.consumerMethod = consumerMethod
		self.id = id
		self.random = random

	'''
	
	if len(usesPermissionList) == 0:
		jsonStr = jsonStr + '\"usesPermissions\":[],'
	else:
		jsonStr = jsonStr + '\"usesPermissions\":['
		
		for index,p in enumerate(usesPermissionList):
			if index == len(usesPermissionList)-1:
				# Last item
				jsonStr = jsonStr + "\"" + p + "\"],"			
			else:
				jsonStr = jsonStr + "\"" + p + "\","			


	jsonStr = jsonStr + '\"Components\":['

	for cOjbect in ComponentList:
		
		jsonStr = jsonStr + '{\"type\":\"' + cOjbect.type +'\",'
		jsonStr = jsonStr + '\"name\":\"' + cOjbect.cName +'\",'		
		jsonStr = jsonStr + '\"requiredPermissions\":\"' + str(cOjbect.requiredPermissions) +'\",'

		# filters
		jsonStr = jsonStr + '\"intentFilter\":['
		fObject = cOjbect.intentFilter
		#jsonStr = jsonStr + '\"actions\":[\"' + str(fObject.actions) +'\"'
		
		for index,a in enumerate(fObject.actions):
			if index == len(fObject.actions)-1:
				jsonStr = jsonStr + '{\"actionName\":\"' + a +'\"}'
			else:
				jsonStr = jsonStr + '{\"actionName\":\"' + a +'\"},'
		
		#jsonStr = jsonStr + '\"categories\":\"' + str(fObject.categories) +'\",'
		#jsonStr = jsonStr + '\"pathData\":\"' + str(fObject.pathData) +'\"'
		jsonStr = jsonStr + '],'
		
		if cOjbect == ComponentList[-1]:
			jsonStr = jsonStr + '\"propagatedPermissions\":\"' + str(cOjbect.propagatedPermissions) +'\"}'
		else:
			jsonStr = jsonStr + '\"propagatedPermissions\":\"' + str(cOjbect.propagatedPermissions) +'\"},'


	jsonStr = jsonStr + '],'


	jsonStr = jsonStr + '\"Intents\":['

	'''
	# intent 
	self.calledAt = calledAt
	self.sender = sender
	self.component = component
	self.action = action
	self.dataType = dataType
	self.scheme = scheme
	self.extra = extra
	self.sensitiveData = sensitiveData
	self.consumerMethod = consumerMethod
	self.id = id
	self.random = random

	'''


	for iObject in intentList:
		
		jsonStr = jsonStr + '{\"calledAt\":\"' + str(iObject.calledAt) +'\",'
		jsonStr = jsonStr + '\"sender\":\"' + str(iObject.sender) +'\",'
		jsonStr = jsonStr + '\"component\":\"' + str(iObject.component) +'\",'
		jsonStr = jsonStr + '\"action\":\"' + str(iObject.action) + '\",'
		#jsonStr = jsonStr + '\"dataType\":\"' + str(iObject.dataType) +'\",'
		#jsonStr = jsonStr + '\"scheme\":\"' + str(iObject.scheme) +'\",'
		#jsonStr = jsonStr + '\"extra\":\"' + str(iObject.extra) +'\",'
		#jsonStr = jsonStr + '\"sensitiveData\":\"' + str(iObject.sensitiveData) +'\",'
		#jsonStr = jsonStr + '\"consumerMethod\":\"' + str(iObject.consumerMethod) +'\",'
		#jsonStr = jsonStr + '\"id\":\"' + str(iObject.id) +'\",'
		
		if iObject == intentList[-1]:
			jsonStr = jsonStr + '\"id\":\"' + str(iObject.id) +'\"}'
			#jsonStr = jsonStr + '\"random\":\"' + str(iObject.random) +'\"}'
		else:
			jsonStr = jsonStr + '\"id\":\"' + str(iObject.id) +'\"},'
			#jsonStr = jsonStr + '\"random\":\"' + str(iObject.random) +'\"},'

	jsonStr = jsonStr + ']'
	
	return jsonStr


AppList = []
filesInDir = []
appNameToNumberDict = {}
linkedPair = {}


covertXML = 'apkfiles.xml'


files = [f for f in os.listdir('.') if os.path.isfile(f)]
for f in files:
	if f.find(".xml") != -1 and f != covertXML:
		filesInDir.append(f)

json_string = "{\"nodes\":["

appIndex = 0

for xml in filesInDir:
	
	appNameToNumberDict[xml] = appIndex
	
	json_string = json_string + "{\"x\":"

	json_string = json_string + str(randint(50,900)) + ",\"y\":"

	json_string = json_string + str(randint(30,770)) + ","
	
	if xml == filesInDir[-1]:
		json_string = json_string + xmlToJSON(xml) + '}'
	else:
		json_string = json_string + xmlToJSON(xml) + '},'
	
	appIndex = appIndex + 1

json_string = json_string + "],"
		
# Find links among apks
for app in AppList:
	for otherApp in AppList:
		if app != otherApp:
			for intent in app.intentList:
				if intent.action in otherApp.allowedActions:					
					temp = None
					for c in otherApp.componentList:
						if intent.action in c.intentFilter.actions:
							temp = c
							break
												
					linkedPair[str(app.name)] = [str(otherApp.name),intent.action,intent.sender,c.cName]

	
	#print appNameToNumberDict[key+".xml"],appNameToNumberDict[value+".xml"]



vulnerableApp = {}

soup2 = BeautifulSoup(open(covertXML),"xml")

for i in soup2.findAll('vulnerability'):

	vulnerableComponent = str(i.find('vulnerabilityElements').find('description').text)
	for app in AppList:
		for c in app.componentList:
			if vulnerableComponent in c.cName:
				vulnerableApp[str(app.name)] = (str(i.find('type').text),str(i.find('description').text))
				break


json_string = json_string + "\"links\":["



index = 0
for key, value in  linkedPair.iteritems():	
	source = appNameToNumberDict[key+".xml"]
	target = appNameToNumberDict[value[0]+".xml"]
	
	description = None
	#print key,value[0]
	if key in vulnerableApp.keys():
		description = vulnerableApp[key]
	
	if description == None:
		if value[0] in vulnerableApp.keys():
			description = vulnerableApp[value[0]]
	
	if index == len(linkedPair)-1:
		json_string = json_string + "{\"source\":" + str(source) +",\"target\":" + str(target) + ","
		json_string = json_string + "\"fromComponent\":" + "\"" + str(value[2]) + "\","
		json_string = json_string + "\"toComponent\":" + "\"" + str(value[3]) + "\","
		json_string = json_string + "\"byTool\":" + "\"" + "Covert" + "\","
		json_string = json_string + "\"type\":" + "\"" + str(description[0]) + "\","
		json_string = json_string + "\"description\":" + "\"" + str(description[1]) + "\","
		json_string = json_string + "\"fromIntent\":" + "\"" + str(value[1]) + "\"" + "}"
	else:
		json_string = json_string + "{\"source\":" + str(source) +",\"target\":" + str(target) + ","
		json_string = json_string + "\"fromComponent\":" + "\"" + str(value[2]) + "\","
		json_string = json_string + "\"toComponent\":" + "\"" + str(value[3]) + "\","
		json_string = json_string + "\"byTool\":" + "\"" + "Covert" + "\","
		json_string = json_string + "\"type\":" + "\"" + str(description[0]) + "\","
		json_string = json_string + "\"description\":" + "\"" + str(description[1]) + "\","
		json_string = json_string + "\"fromIntent\":" + "\"" + str(value[1]) + "\"" + "},"
	index = index + 1	
json_string = json_string + "]}"

#print vulnerableApp.keys()
#print json_string
#print linkedPair
#print AppList[1].componentList[0].cName
#print AppList[1].intentList
#parsed_json = json.loads(json_string)


try:
	parsed_json = json.loads(json_string)
	
	with open('../graph.json', 'w') as outfile:
		json.dump(parsed_json, outfile)
	
except ValueError:
	print "Invaild json string"



	
#print parsed_json['Name']