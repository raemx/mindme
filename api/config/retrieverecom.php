
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

$sql = "SELECT * FROM recoms where recom = (SELECT rmdn FROM recommendations WHERE rmdn regexp '^[3]+' AND id = '$id' ORDER BY timestamp DESC LIMIT 1)";
$result = mysqli_query($con,$sql);
$response = array();

if ($row = mysqli_fetch_array($result)) {
  array_push($response, array("recom" => $row[0],
        "NHS" => $row[2]
    )
);
}
else{
  $response = 'General Recommendation';
}

echo json_encode($response);

mysqli_close($con)

  // $command = escapeshellcmd('mindme\python\model.py');
  // $output = shell_exec($command);

?>