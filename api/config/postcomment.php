<?php

$con = mysqli_connect("localhost", "root", "", "mindme") or die("Couldnt connect to database");

  include "config.php";
  $input = file_get_contents('php://input');
  $data = json_decode($input, true);
  $msg = array();

  $comment = $data['emot'];
  $discussionid = $data['discussionid'];
  $now = time();
  $timestamp = date("Y-m-d H:i:s", $now);
  $id = $_GET['id'];

  $sql = "INSERT INTO community (id, discussionid, comment, timestamp) VALUES ('$id', '$discussionid', '$comment', '$timestamp')";
  $q = mysqli_query($con, $sql);

  	if($q){
      http_response_code(200);
      $msg['status'] = "Success";
    }else{
      http_response_code(422);
      $msg['status'] = "Error";
    }

      echo json_encode($msg);
      echo mysqli_error($con);
  

  ?>
