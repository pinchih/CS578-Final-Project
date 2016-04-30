#!/bin/bash

echo " <br>"
echo "1. Execute COVERT, IccTA, and DidFail<br>"
echo "  \$ ./exec_covert.sh "   $1 " > covert.xml* <br>"
echo "  \$ ./exec_iccta.sh "    $1 " > iccta.xml* <br>"
echo "  \$ ./exec_didfail.sh "  $1 " > didfail.xml* <br>"


echo " <br>"
echo "2. Convert XML to JSON for Overall Architecture<br>"
echo "  \$ ./overall.py covert.xml* > overall.json <br>"


echo " <br>"
echo "3. Convert XML to JSON <br>"
echo "  \$ ./convert_covert.py covert.xml   > covert.json <br>"
echo "  \$ ./convert_iccta.py iccta.xml     > iccta.json <br>"
echo "  \$ ./convert_didfail.py didfail.xml > didfail.json <br>"


echo " <br>"
echo "4. Visualize HTML <br>"
echo "  Just read index.html <br>"


