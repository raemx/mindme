
<?php

// $con = mysqli_connect("localhost", "root", "", "mindme") or die("Couldnt connect to inputbase");

//   include "config.php";
//   $id = $_GET['id'];
//   $input = array();

//   $q = mysqli_query($con, "SELECT (id, name, name2) FROM  users WHERE 'email' = $email LIMIT 1");

// while ($row = mysqli_fetch_object($q)){
//     $input[] = $row;
// }

// echo json_encode($input);
// echo mysqli_error($con);

include "config.php";
$input = file_get_contents("php://input");
$request = json_decode($input);

$id = $_GET['id'];

// if (isset($input)) {
//   $request = json_decode($input,true);
//   $email = $request['email'];
// }

$sql = "SELECT * FROM users WHERE id = '$id'";
$result = mysqli_query($con,$sql);
$response = array();

  
while ($row = mysqli_fetch_array($result)) {
  array_push($response, array("id" => $row[0],
        "name" => $row[1],
        "name2" => $row[2],
        "email" => $row[3],
        "password" => $row[4]
    )
);
}

echo json_encode($response);

mysqli_close($con)

  // $command = escapeshellcmd('mindme\python\model.py');
  // $output = shell_exec($command);

?>