<?php
  $logfile = "scripts/log_vul.txt";

  // Check log 
  echo "<br> Last Log: ";
  echo exec("tail " . $logfile);
  echo "<br>";

  // Check status from log file
  exec ("grep __Finished__ " . $logfile, $retval, $ret);
  if ($ret == 0) {
    echo "<br> Status: Finished <br>";

    // Show visualization for valunerable path
    include("index.html");
  } else {
    echo "<br> Status: COVERT or DidFail is still Running ... Close this and try again <br>";
  }

?>

