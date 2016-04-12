<?php
  if (@$_GET['send']) {
    echo "Output[".$_GET['send']."]<br>";
  } else {
    echo "Press Button on sample.html";
  }
  
  $files = shell_exec("ls files");
  $output = shell_exec('../scripts/exec.sh '.escapeshellarg($files));
  echo $output;

  include("./tats_hw3.html");
?>
