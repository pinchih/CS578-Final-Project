<?php
  $logfile = "scripts/log_didfail.txt";

  // Check log for DidFail
  echo "<br> Last Log: ";
  echo exec("tail " . $logfile);
  echo "<br>";

  // Check status from log file
  exec ("grep __Finished__ " . $logfile, $retval, $ret);
  if ($ret == 0) {
    echo "<br> Status: DidFail Finished <br>";
  } else {
    echo "<br> Status: DidFail is still Running ... Close this and try again <br>";
  }
?>

