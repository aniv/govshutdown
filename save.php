<?php
  $con=mysqli_connect("mbdb.aniv.info","tweets","stuartdiamond","lgsttweets");
  $data = file_get_contents("php://input");
  mysqli_query($con,"INSERT INTO tweets (tweets) VALUES ('$data')");
?>
