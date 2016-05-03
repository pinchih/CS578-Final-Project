#What's this?
This is a final project for Software Architecture ( CSCI578 ) at University of Southern California. In this project, we designed and implemented a web-based tool that enables users to check if installed apps on their Android devices are exposed to any threats of Inter-Component Communication (ICC) attacks and users can see a visualized result of overall architecture of targeted apps and also the potential vulnerable paths among applications.

#Members
* [Chris Daniels](https://github.com/chris-daniels)
* [Pin-Chih Lin](https://github.com/pinchih)
* [Tomita Tatsuhiko](https://github.com/tomitatsu)

#An overview of the system     
![picture alt](https://github.com/pinchih/CS578-Final-Project/blob/master/image/system_graph.png?raw=true)

#Overall system architecture visualization example
![](/image/overall_system_architecture_example.gif)
#Vulerable paths visualization example

#Tools
- OverallArchitectureXMLConverter.py
  - This tool takes inputs of XML files generated from COVERT, and create a JSON file for visualization in browser.
- VulnerablePathXMLConverter.py
  - This tool takes inputs of XML files generated from COVERT for potential vulnerable paths, and create a JSON file for visualization in browser.
- VulnerablePathDidFail.py
  - This tool takes inputs of XML files generated from DidFail for potential vulnerable paths and JSON file created by VulnerablePathXMLConverter.py, combined the information into one JSON file.

#Usage

#Architectural pattern/styles used

#Reference tools/libraries/web services
* Beautiful Soup ([https://www.crummy.com/software/BeautifulSoup/](https://www.crummy.com/software/BeautifulSoup/))
* D3.js ([https://d3js.org/](https://d3js.org/))
* DigitalOcean ([https://www.digitalocean.com/](https://www.digitalocean.com/))
* DidFail ([https://www.cs.cmu.edu/~wklieber/didfail/](https://www.cs.cmu.edu/~wklieber/didfail/))
* COVERT ([http://www.sdalab.com/tools/covert](http://www.sdalab.com/tools/covert))






