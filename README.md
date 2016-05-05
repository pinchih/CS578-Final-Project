#What's this?
This is a final project for Software Architecture ( CSCI578 ) at University of Southern California. In this project, we designed and implemented a web-based tool that enables users to check if installed apps on their Android devices are exposed to any threats of Inter-Component Communication (ICC) attacks and users can see a visualized result of overall architecture of targeted apps and also the potential vulnerable paths among applications. The analysis tools that we used in this project are [COVERT](http://www.sdalab.com/tools/covert) and [DidFail](https://www.cs.cmu.edu/~wklieber/didfail/).

#Members
* [Chris Daniels](https://github.com/chris-daniels)
* [Pin-Chih Lin](https://github.com/pinchih)
* [Tatsuhiko Tomita](https://github.com/tomitatsu)

#An overview of the system     
![picture alt](https://github.com/pinchih/CS578-Final-Project/blob/master/image/system_graph.png?raw=true)

#Overall system architecture visualization example

![](/image/overall_system_architecture_example.gif)

The overall system architecture visulaization gives you glance of how your application and other applications that we chosen interact with each other in terms of ICC calls. You may mouse over the path info icon to see what components were interacting, or mouse over the node to see what user permissions are alloed for this application. If you would like to know the interaction among components within an application, just click the name of that app, it will open up another window and show you the result.

#Vulnerable paths visualization example

 ![](https://github.com/pinchih/CS578-Final-Project/blob/master/image/VulnerablePath_example.gif?raw=true)
 
The vulunerable path visualization gives you the sense of what are the vulnerable paths suggested by the analysis tool, including COVERT and DidFail. The path suggested by COVERT will have a little C icon attached to the link while DidFail will have a D icon. Uers can mouse over the icon to see the detail of the vulnerable path.

#Intra Component Communication within an application

![](https://github.com/pinchih/CS578-Final-Project/blob/master/image/intra_compo_example.gif?raw=true)

Overall system architecture and vulnerable paths visualization show the ICC calls among applications, but if users would like to know what components are interacting with what components inside an application, just simply click the name of the application in either overall system architecture or vulnerable paths visualization, a new window will open and show you the intra component communications.

#Analysis for real application
- Sample applications
![picture alt](https://github.com/pinchih/CS578-Final-Project/blob/master/image/Analysis_Overall_1.png)
![picture alt](https://github.com/pinchih/CS578-Final-Project/blob/master/image/Analysis_Vul_1.png)
  - Echoer application, which is a sample application of DidFail, is vulnerable that is detected by both COVERT and DidFail. COVERT suggests this vulnerability is Intent Spoofing. We can see that the Intent type is Action.SEND by seeing overall system architecture.
  - CatDogToe, which was implemented by us for Homework 2, is vulnerable that is detected by both COVERT and DidFail. This is also recognized as Intent Spoofing. We can see that the Intent type is Action.START_SERVICE.

- Real applications with Sample
![picture alt](https://github.com/pinchih/CS578-Final-Project/blob/master/image/Analysis_Overall_2.png)
![picture alt](https://github.com/pinchih/CS578-Final-Project/blob/master/image/Analysis_Vul_2.png)
  - "Send2U" application can receive Action.SEND Intent, and it is vulnerable detected by COVERT. It implies users should user "Send2U" application carefully.

#Tools and how to use them
- OverallArchitectureXMLConverter.py
  - This tool takes inputs of series of XML files generated by COVERT, gathers information for the inter- and intra-ICC relationships and output them as a JSON file in a pre-defined format, which will later be used for overall architecture visualization.
  - All the inputs XML from COVERT should be placed within the overallArchitecture folder.
  - The output file will be a overallArchitecture.json.

- VulnerablePathXMLConverter.py
  - This tool takes one XML files (pre-named apkfiles.xml) generated by COVERT , gathers information for vulnerable paths and output a JSON file in a pre-defined format, which will later be used by VulnerablePathDidFail.py.
  - The input apkfiles.xml should be placed within the overallArchitecture folder.
  - The output file will be a graph.json.

- VulnerablePathDidFail.py
  - This tool takes inputs of series of XML files (*.fd.xml) and one flow.out file generated by DidFail. It looks into analysis results, gathers the information about potential vulnerable paths and combine these information to the JSON file which generated by VulnerablePathXMLConverter.py.
  - All the *.fd.xml files and the flow.out file should be placed within the overallArchitecture folder.
  - The output file will be a graph.json, which overrided the original graph.json generated by VulnerablePathXMLConverter.py.

- soup.py
  - This takes inputs of series of XML files (*.xml) generated by COVERT. You can specify the files as command-line arguments.
  - This outputs series of JSON files each of which relates to each application.
  - You can see the intra component communication of each application by seeing compo.html and give each json file to the html file, e.g. "http://compo.html?file=app_name.json".

#Usage
Go to our [website](http://192.241.189.66/top.html), upload your applications, and see the analysis results.(Please note that at any point in the future, the server might went done due to limitation of the usage of the server.)

#Architectural pattern/styles used
- Client-Server style
  - The architectural style that we chose for implementing this project is Client-Server sytle. The main reason for using this  style is because that this project is going to be a web-based tool, which narrows us done to few architectural styles that we can choose from, and practically, a Client-Server style will be a safe and easy way to go, because it's been tested and proven to be reliable.

  - In this sytle, components of the system will be mulitiple clients and one server, and the connector between client and server will be the RPC-based network protocols, such as TCP/IP. Technically speaking, the server in a Client-Server style should be capable of handling multiple connections from different clients, however, in our case, due to the heavy loading of executing the analysis tools(DidFail, COVERT), our server will not take another apk inputs if there's already a processing going on. This issue can be solved by increasing the computing power and the memory of the server, or implementing the asynchronous mechanism at the server-end.  

- Polling Pattern
  - To improve userability, we decided to use polling pattern in two cases:
      - While analizing overall system architecture, we keep to show consecutive dot (.) on regular intervals s
o that users can see it is working. To know the end of the process, our system polls a log file that the extra
ct tool outputs until it finishes.
      - After showing overall system architecture, we continue to analyze vulnerable path in background. Hence,
 users can get overall system architecture first before we get whole vulnerable path analysis. Users should po
ll it by clicking "Get Vulnerable Path" button until they get the result of vulnerable path visualization.

#Directory tree
- analysis_tool/
  - covert_dist/ and didfail/ are supposed to be here (there not exist in git repository)
- APK/
  - apk files that we have examined
- apkfiles/
  - apk files that users upload will be here
- css/
- image/
- interCompo/
  - used for Intra Component Communication visualization
- javascripts/
- overallSystemArchitecture/
  - used for Overall system architecture and Vulnerable paths visualization
- scripts/
- compo.html
  - Intra Component Communication Visualization
- exec.php
  - main routine
- graph.json
  - used for Vulnerable paths visualization
- index.html
  - Vulnerable paths visualization
- overallArchitecture.html
  - Overall system architecture visualization
- php.ini
- README.md
  - this file
- top.html
  - portal page
- vulnerable.php
  - sub routine for showing vulnerable path visualization

#Execution flow
- Prepare
  - uploaded files are saved in `TOP/apkfiles`
- COVERT (for overall architecture visualization)
  - copy apkfiles to `TOP/analysis_tool/covert/app_repo`
  - run COVERT (only extract apks (i.e. don't execute whole process) and get `model/` directory)
  - copy `TOP/analysis_tool/covert/app_repo/analysis/model/.apk` to `TOP/overallSystemArchitecture`
  - run converter `OverallArchitectureXMLConverter.py` and get `overallArchitecture.json`
  - run converer `soup.py` and get a series of `.json` files for each apks
  - wait until there exist "__Finieshed__" in `TOP/scripts/log.txt`
  - include `TOP/overallArchitecture.html` and get overall visualization
- COVERT (vulnarable path)
  - run COVERT (get `apkfiles.xml` that includes vulnerable path)
  - copy `TOP/analysis_tool/covert/app_repo/apkfiles.xml` to `TOP/overallSystemArichitecture`
  - run converter `VulnerablePathXMLConverter.py` for vulnerable path, and get `graph.json`
- DidFail (vulnarable path)
  - run DidFail (get `.fd.xml` , `flows.out` that includes vulnerable path)
  - when DidFail finishes, it outputs "__Finished__" into `TOP/scripts/log_vul.txt` so that we can know whether it finishes or no by seeing the file
  - copy `TOP/analysis_tool/didfail/out/flows.out` and `.fd.xml` to `TOP/overallSystemArchitecture`
  - run converter `VulnerablePathDidFail.py`, and update `graph.json`
  - include `TOP/index.html` and get valunarable path visualization


#Reference tools/libraries/web services
* Beautiful Soup ([https://www.crummy.com/software/BeautifulSoup/](https://www.crummy.com/software/BeautifulSoup/))
* D3.js ([https://d3js.org/](https://d3js.org/))
* DigitalOcean ([https://www.digitalocean.com/](https://www.digitalocean.com/))
* DidFail ([https://www.cs.cmu.edu/~wklieber/didfail/](https://www.cs.cmu.edu/~wklieber/didfail/))
* COVERT ([http://www.sdalab.com/tools/covert](http://www.sdalab.com/tools/covert))
* Apache ([https://httpd.apache.org/](https://httpd.apache.org/))
* PHP ([https://secure.php.net/manual/ja/index.php](https://secure.php.net/manual/ja/index.php))




