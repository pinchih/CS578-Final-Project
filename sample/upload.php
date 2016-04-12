<html><body>
  <form action="exec.php" method="get">
    <input type="submit" name="send" value="COVERT">
    <input type="submit" name="send" value="IccTA">
    <input type="submit" name="send" value="DidFail">
  </form>

<?php

// Clean tmp directory "./files/"
shell_exec("rm files/*");

if (is_uploaded_file($_FILES["upfile"]["tmp_name"])) {
  if (move_uploaded_file($_FILES["upfile"]["tmp_name"], "files/" . $_FILES["upfile"]["name"])) {
    chmod("files/" . $_FILES["upfile"]["name"], 0644);
    print "How do you want to analyze \"" .$_FILES["upfile"]["name"] . "\" ? <br>";
  } else {
    echo "Error: upload failed. <br>";
  }
} else {
  echo "Error: file not selected. <br>";
}

//<!--$fileName = $_FILES["upfile"]["name"];-->
//<!--$output = shell_exec('scripts/exec.sh '.escapeshellarg($fileName).' aaa');-->
//<!--echo $output;-->
?>

</body>
</html>
