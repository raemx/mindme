<?php

  $dbhost = "localhost";
  $dbport = "root";
  $dbuser = "";
  $dbpwd = "loginsystem";

  //create connection
  $conn = new mysqli($dbhost, $dbhost, $dbuser, $dbpwd);
    //check connection
  if (!$conn){
    die("Connection failed: " . $conn->connect_error);
  }

  $email = $_POST['email'];
  $password = $_POST['password'];

  if ($_SERVER['REQUEST_METHOD'] == 'POST'){ //insert query doesn't run everytime page is loaded

    $sql = "INSERT INTO users (firstname, lastname, email, username, password) VALUES ('$firstname', '$lastname','$email', '$username','$password')"; //adds new users into database

    if($conn->query($sql) === TRUE){
    //   echo '<aside> <h1>WELCOME BACK</h1> </aside>' .$row["firstname"] $row["lastname"];
      header("Location: tab1.page.html")
    }
    else {
      echo "Error: " . $sql . "<br>" . $conn->error;
    }
      $conn->close();
  }

?>
