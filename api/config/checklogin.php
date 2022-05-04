<?php

$con = mysqli_connect("localhost", "root", "", "mindme") or die("Couldnt connect to DB");

  include "config.php";
  $input = file_get_contents("php://input");

  if (isset($input)) {
    $request = json_decode($input);
    $email = $request->email;
    $password = $request->password;

  }

   
  $login = "SELECT id FROM users WHERE email='$email' AND password='$password'";
  $result = mysqli_query($con,$login);
  $row = mysqli_fetch_array($result,MYSQLI_ASSOC);
  $count = mysqli_num_rows($result);

    
    // If result matched $myemail and $mypassword, table row must be 1 row
    
  if($count >0) {
  $response= "Login Success";
    }else {
  $response= "Your Login Email or Password is invalid";
  
  }
 
 
  echo json_encode($response);

?>

