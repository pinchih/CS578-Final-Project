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

  // Clean tmp directory
  shell_exec("rm apkfiles/*");

  // Move uploaded files to apkfiles/
  foreach ($_FILES["upfile"]["error"] as $key => $value) {
    // Successful
    if ($value == UPLOAD_ERR_OK) {
      $file_name = $_FILES["upfile"]["name"][$key];
      // $file_type = $_FILES["upfile"]["type"][$key];
      // $file_size = $_FILES["upfile"]["size"][$key];
      $file_temp = $_FILES["upfile"]["tmp_name"][$key];
      $file = "upload".$file_name;

      if (($result = move_uploaded_file($file_temp, "apkfiles/" . $file_name)) === true) {
          echo "upload succeeded. " . $file_name . "<br>";
          chmod("apkfiles/" . $file_name, 0644);
      } else {
        echo "Error: upload failed. <br>";
      }
    } else {
        $file_name = $_FILES["upfile"]["name"][$key];
        echo "Error: upload failed. " . $file_name . " errno[" . $value . "]<br>";
    }
  }
  
  // Create params for sending apks to other servers 
  $i = 0;
  foreach(glob('apkfiles/*') as $file){
  	if(is_file($file)){
  		$index = "upfile[" . strval($i). "]";
  		$params[$index] = "@".$file;
  		$i += 1;
  	}
  }
  
  // Send apks by curl
  $url = "https://csci578-test-tomitatsu.c9users.io/sample/test.php";

  // Run other servers
  // echo "send files to " . $url . "<br>";
  // echo $params["upfile[0]"] . "<br>";
  // echo $params["upfile[1]"] . "<br>";
  // $curl=curl_init($url);
  // curl_setopt( $curl, CURLOPT_POSTFIELDS, $params );
  // $output= curl_exec($curl);
  // // echo "Result: " . $output . "<br>";
  // curl_close($curl);


  // Clean tmp directory "./files/"
  shell_exec("rm -rf analysis_tool/covert_dist/app_repo/apkfiles");
  shell_exec('cp -rf apkfiles/ analysis_tool/covert_dist/app_repo/');

  // Extract apks
  echo "<br> Extracting by COVERT ... <br>";
  // $output = shell_exec('../scripts/exec.sh '.escapeshellarg($fileName));
  // $output = shell_exec('../scripts/overall.sh &');
  shell_exec('./scripts/overall.sh > /dev/null &');

  // Show the progress
  echo str_pad(" ",4096)."<br />\n";
  ob_end_flush();
  ob_start('mb_output_handler');
  $retval = array();
  $ret = 0;
  for ( $i = 1; $i <= 1000; $i++ ) {
    // Output log every 5 sec (if no progress, not output)
    sleep( 3 );
    $output = shell_exec('tail -n 1 ./scripts/log.txt');
    if ($output != $tmp) {
      //echo $output;
      //echo "<br>";
      echo ".";
    }
    $tmp = $output;

    // If find string "Finished" in log file, then break the loop
    exec ('grep Finished ./scripts/log.txt', $retval, $ret);
    if ($ret == 0) {
#      echo $retval . "<br>";
      break;
    }
    
    ob_flush();
    flush();
  }

  echo "<br>";
  //echo "<h1>Overall Architecture:</h1>";
  //include("./tats_hw3.html");
  // echo "<a href=\"https://csci578-project-tomitatsu.c9users.io/sample/tats_hw3.html\"><h1>Overall Architecture:</h1></a>";
  include("./overallArchitecture.html");
  echo "<br>";

  // Execute Covert on this Server
  // shell_exec('../scripts/covert.sh > /dev/null &');
  // $output = shell_exec('../scripts/covert.sh');
  // echo $output;
?>


</body>
</html>
