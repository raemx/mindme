
<?php

//get post variables from page

$emot = $_POST['emot'];
$email = $_GET = ['email']
//mnake connection to mysql server with hostname,username,password and database
$conn = new mysqli('localhost', 'root','',' mindme');
  //check connection
if (!$conn){
  die("Connection failed: " . $conn->connect_error);
}

//query inserting records to table
$sql = "INSERT INTO mood ('emot') VALUES ('$emot') WHERE ('email') == ('$email')";

if(!mysqli_query($conn, $sql))
{
 die("Error inserting records".$conn->connect_error);
 header("Location: tab1.page.html");

}
else{
  header("Location: tab1.page.html");
}

?>
