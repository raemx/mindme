<!--adds a new post to a simple table within a MySQL database and redirects to
viewBlog.php. -->
<?php

//get post variables from page

$name = $_POST['name'];
$name2 = $_POST['name2'];
$email = $_POST['email'];
$password = $_POST['password'];
$no = $_POST['no'];
$line1 = $_POST['line1'];
$line2 = $_POST['line2'];
$city = $_POST['city'];
$town = $_POST['town'];
$postcode = $_POST['postocde'];


//mnake connection to mysql server with hostname,username,password and database
$conn = new mysqli('localhost', 'root','',' mindme');
  //check connection
if (!$conn){
  die("Connection failed: " . $conn->connect_error);
}

//query inserting records to table
$sql = "INSERT INTO users (name, name2, email, password, no, line1, line2, city, town, postcode) VALUES ('$name', '$name2', '$email', '$password', '$no', '$line1', '$line2', '$city', '$town', '$postcode')";

if(!mysqli_query($conn, $sql))
{
 die("Error inserting records".$conn->connect_error);
 header("Location: login.page.html");

}
else{
  header("Location: register.page.html");
}

?>
