<html><body>
  <form method="post" action="covert.php" target="_blank">
    <input type="submit" name="send" value="COVERT">
  </form>
  <form method="post" action="iccta.php" target="_blank">
    <input type="submit" name="send" value="IccTA">
  </form>
  <form method="post" action="didfail.php" target="_blank">
    <input type="submit" name="send" value="DidFail">
  </form>

<?php
  shell_exec('../scripts/covert.sh > /dev/null &');

  // Show the progress
  echo str_pad(" ",4096)."<br />\n";
  ob_end_flush();
  ob_start('mb_output_handler');
  $retval = array();
  $ret = 0;
  for ( $i = 1; $i <= 1000; $i++ ) {
    // Output log every 5 sec (if no progress, not output)
    sleep( 5 );
    $output = shell_exec('tail -n 1 ../scripts/log.txt');
    if ($output != $tmp) {
      echo $output;
      echo "<br>";
    }
    $tmp = $output;

    // If find string "Finished" in log file, then break the loop
    exec ('grep Finished ../scripts/log.txt', $retval, $ret);
    if ($ret == 0) {
      echo $retval . "<br>";
      break;
    }
    
    ob_flush();
    flush();
  }

  echo "<br>";
  echo "<h1>Overall Architecture:</h1>";
  include("./tats_hw3.html");
  // echo "<a href=\"https://csci578-project-tomitatsu.c9users.io/sample/tats_hw3.html\"><h1>Overall Architecture:</h1></a>";
  echo "<br>";

?>


</body>
</html>
