<?php
  $logfile = "scripts/log_covert.txt";

  // Check log for COVERT
  echo "<br> Last Log: ";
  echo exec("tail " . $logfile);
  //system("tail scripts/log.2.txt", $status);
  echo "<br>";

  // Check status from log file
  exec ("grep __Finished__ " . $logfile, $retval, $ret);
  if ($ret == 0) {
    echo "<br> Status: COVERT Finished <br>";
  } else {
    echo "<br> Status: COVERT is still Running ... Close this and try again <br>";
  }

  // Show visualization for valunerable path
  
?>

