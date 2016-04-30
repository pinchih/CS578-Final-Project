# -*- coding: utf-8 -*-
# usage: python soup.py input_folder(which has *.xml) output_folder(which will have *.json)
# output: *.json, merge.json
# Ex.
#  $ python soup.py analyze/ output/
#  Create: hoge.json
#  Create: foo.json
#  Create: merge.json
##############################

from bs4 import BeautifulSoup
from collections import namedtuple
from sets import Set
import os
import sys


##############################
# Class / Struct
##############################
Sendto 	= namedtuple("send"	, "action to")
App 	= namedtuple("app"	, "name perms groupNum")
Intent 	= namedtuple("intent", "sender component action")
Link 	= namedtuple("link"	, "source target action")
Compo	= namedtuple("compo", "name longname filters perms groupNum")	# perms is always None(it's used as App instance)
Action	= namedtuple("action", "name sameGrpFlg filterCompoSet sendCompoSet")

##############################
# Global variables
##############################
g_xml_dir 		= sys.argv[1]
g_output_dir	= sys.argv[2]
g_intentArray 	= []
g_appArray 		= []
g_cnt 			= 0
g_groupDict 	= {}	# { compoName, groupNum }
g_compoDict		= {}	# { compoName, compo_ins }

##############################
# Function
#   arg		: Ex. "com.android.hoge"
#   return	: Ex. hoge
##############################
def getLastString (stringWithDot) :
	tmp = stringWithDot.split('.')
	return tmp[-1]

##############################
# Function
#   arg		: intentArray
#	arg		: compoDict ([compoName : compo])
#	return 	: linkArray
##############################
def createLinkArray(intentArray, compoDict):
	linkArray = []
	for intent in intentArray:
		sender_compo = compoDict.get(intent.sender)
		recver_compo = compoDict.get(intent.component)
		if recver_compo is None:
			for compo in compoDict.values():
				breakFlg = False
				for filter in compo.filters:
					if intent.action == filter:
						recver_compo = compo
						breakFlg = True
						break
				if breakFlg == True:
					break

		# create link instance
		if recver_compo is not None and sender_compo is not None:
			link = Link(sender_compo.longname, recver_compo.longname, intent.action)
			
			# add the instance to link array
			linkArray.append(link)

	return linkArray

##############################
# Function
#	breif	: Manipulate linkArray to linkDict
#   arg1	: linkArray		 : link = (source_compo, target_compo, action)
#	return 	: linkDictionary : {(source, target) : [actions]} , action = (Set([fiterCompos]), Set([sendCompos]))
##############################
def createLinkDictionary (linkArray):
	linkDict = {}
	for link in linkArray:
		if linkDict.has_key((link.source, link.target)):
			actions = linkDict[(link.source, link.target)]
			sameActFlg = False
			for act in actions:
				if act.name == link.action:
#					print "Same action"
					sameActFlg = True
					act.filterCompoSet.add(link.target)
					act.sendCompoSet.add(link.source)
					break
			# if the link's action has already been in link dictionary, do nothing
			if not sameActFlg:
				action = Action(link.action, False, Set([link.target]), Set([link.source]))
				actions.append(action)
		else:
			# action has an action name, sameGroupFlag, a set of target, and a set of source
			action = Action(link.action, False, Set([link.target]), Set([link.source]))
			linkDict[(link.source, link.target)] = [action]
				
	return linkDict

##############################
# Function
#	breif	: Manipulate linkDict corresponding to group for json output
#   arg1	: linkDict				[("com.hoge.src", "com.foo.trg"): [actions]]
#	arg2	: group dictionary		["com.hoge.src": groupNum]
#	return 	: linkDictionaryGroup	[groupNum1, groupNum2, [actions]]
##############################
def createLinkDictionaryGroup (linkDict, groupDict):
	linkDictGrp = {}
	for (key_src, key_trg), actions in linkDict.items()[:-1]:
		if linkDictGrp.has_key((groupDict[key_src], groupDict[key_trg])):
			acts = linkDictGrp[(groupDict[key_src], groupDict[key_trg])]
			acts.extend(actions)
		else:
			linkDictGrp[(groupDict[key_src], groupDict[key_trg])] = actions

	return linkDictGrp


##############################
# Function
#   breif	: Output json
# 	Example:
#  "nodes":[
#    {"name":" ActionSenderTats ","group": 0 },
#    {"name":" AirDroid ","group": 1 }
#  ],
#  "links":[
#    {"source": 0 ,"target": 1 ,"value": "[Intent] KEEP_RUNNING \n   [filter]\n      LocalService \n   [sender]\n      LocalService \n "},
#    {"source": 0 ,"target": 1 ,"value": "[Intent] KEEP_RUNNING \n   [filter]\n      LocalService \n   [sender]\n      LocalService \n "},
#    {"source": 0 ,"target": 0 ,"value": "dummy"}
#  ]
#}
##############################
def printJson (moduleArray, linkDictGrp, groupDict, outputFile):
	f = open(outputFile, 'w') # If exist, overwrite

	print >> f, "{"
	print >> f, "  \"nodes\":["
	for app in moduleArray[:-1]:
		print >> f, "    {\"name\":\"", app.name , "\",\"group\":", app.groupNum, ",\"value\":\"[permissions]\\n",
		for perms in app.perms:
			print >> f, "  ", perms, "\\n",
		print >> f, "\"},"
	# last index
	app = moduleArray[-1]
	print >> f, "    {\"name\":\"", app.name , "\",\"group\":", app.groupNum, ",\"value\":\"", 
	for perms in app.perms:
		print >> f, "  ", perms, "\\n",
	print >> f, "\"}"
	
	print >> f, "  ],"
	print >> f, "  \"links\":["
	printFlag = True
	for (key_src, key_trg), actions in linkDictGrp.items()[:-1]:
		printFlag = True
		for action in actions:
			if key_src != key_trg:
				if printFlag:
					print >> f, "    {\"source\":", key_src,
					print >> f,     ",\"target\":", key_trg,
					print >> f,     ",\"value\":\"",
					printFlag = False

				print >> f, "[Intent]", action.name, "\\n",
				print >> f, "  [filter]\\n",
				for filter in action.filterCompoSet:
					print >> f, "    ", getLastString(filter), "\\n",
				print >> f, "  [sender]\\n",
				for sender in action.sendCompoSet:
					print >> f, "    ", getLastString(sender), "\\n",
		if not printFlag:
			print >> f, "\"},"
	print >> f, "    {\"source\": 0 ,\"target\": 0 ,\"value\": \"dummy\"}"
	print >> f, "  ]"
	print >> f, "}"

	f.close()
	print "Created: " + outputFile

##############################
# Parse function
#   breif	: parse xml file and add information to global variant g_intentArray, g_compoDict, and g_appArray
#   arg		: fileName
#	return 	: None
##############################
def parse(fileName):
	global g_cnt
	soup = BeautifulSoup(open(g_xml_dir + "/"+fileName), "xml")
	
	# create app instance [name, permissions, groupNum]
	app = App(soup.find("application").find("name", recursive=False).string, [], g_cnt)

	groupDict = {}
	compoDict = {}
	cnt = 0
	### Find Component
	compos = soup.findAll("Component")	
	for c in compos:
		name = c.find("name").string
		# Create a component instance (name, longname, filters, permissions, groupNum)
		# perms is always None(it's used as App instance)
		compo_ins = Compo(getLastString(name), name, Set([]), [], g_cnt)

		# Add actions to the component
		for f in c.findAll("actions"):
			# since filters is "set", value is uniq 
			compo_ins.filters.add(f.string)

		# Add the component to app dictionary w/ the name
		compoDict[name] = compo_ins
		g_compoDict.update(compoDict)
		
		# Memorize this compo is in which group 
		g_groupDict[name] = g_cnt
		groupDict[name] = cnt
		cnt += 1

	### Find permissions
	permissions = soup.usesPermissions.findAll("permission")
	for p in permissions:
		app.perms.append(p.string)
	
	# Add app instance to array
	g_appArray.append(app)

	# inclement counter for group number (1 group represents for 1 app)
	g_cnt += 1
	
	### Find Intent
	intentArray = []
	intents = soup.findAll("Intent")
	for i in intents:
		sender = i.find("sender").string

		sendToComponent = i.find("component").string
		if sendToComponent is None:
			sendToComponent = "Implicit"

		action = i.find("action").string
		if action is None:
			action = "Explicit"
		action = action.replace("\"","")

		# create intent instance
		intent = Intent(sender, sendToComponent, action)
		
		# add intent to array
		intentArray.append(intent)
	g_intentArray.extend(intentArray)

	# Create compo array
	compoArray = compoDict.values()

	main(intentArray, compoDict, groupDict, compoArray, g_output_dir + "/" + app.name + ".json")

def main (intentArray, compoDict, groupDict, appArray, outputFileName):
	# Create link array
	linkArray = createLinkArray(intentArray, compoDict)
	# Do Uniq
	linkArray = list(set(linkArray))

	# Create link dictionary
	linkDict = createLinkDictionary(linkArray)
	linkDictGrp = createLinkDictionaryGroup (linkDict, groupDict)

	# Output json file
	printJson(appArray, linkDictGrp, groupDict, outputFileName)


##############################
# Main
##############################
for fileName in os.listdir(g_xml_dir):
	parse(fileName)

main(g_intentArray, g_compoDict, g_groupDict, g_appArray, g_output_dir + "/merge.json")

