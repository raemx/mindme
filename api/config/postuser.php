<?php

$con = mysqli_connect("localhost", "root", "", "mindme") or die("Couldnt connect to database");

  include "config.php";
  $input = file_get_contents("php://input");
  $data = json_decode($input, true);
  $msg = array();

  $name = $data["name"];
  $name2 = $data["name2"];
  $email = $data["email"];
  $password = $data["password"];
  $no = $data["no"];
  $line1 = $data["line1"];
  $line2 = $data["line2"];
  $city = $data["city"];
  $town = $data["town"];
  $postcode = $data["postcode"];

  $q = mysqli_query($con, "INSERT INTO users (name, name2, email, password, no, line1, line2, city, town, postcode) VALUES ('$name', '$name2', '$email', '$password', '$no', '$line1', '$line2', '$city', '$town', '$postcode')");

    if($q){
      http_response_code(200);
      $msg["status"] = "Success";
    }else{
      http_response_code(422);
      $msg["status"] = "Error";
    }

    echo json_encode($msg);
    echo mysqli_error($con);
  

  ?>