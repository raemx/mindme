<?php

  include "config.php";
  $input = file_get_contents('php://input');
  $msg = array();

  $id = $_GET['id'];
  $q = mysqli_query($con, "DELETE FROM 'USERS' WHERE 'id='{$id}' LIMIT 1")
  

  if($q){
    http_response_code(201);
    $msg['status'] = "Success";
  }else{
    http_response_code(422);
    $msg['status'] = "Error";
  }

    echo json_encode($msg);
    echo mysqli_error($con);
?>
