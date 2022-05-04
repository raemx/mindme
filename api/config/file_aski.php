<?php

header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Credentials: true');
header('Access-Control-Allow-Methods: GET, POST, OPTIONS, PUT, DELETE');
header('Access-Control-Allow-Headers: Origin, X-Requested-With, Content-Type, Accept, Authorization');
header('Content-Type: application/json; charset=UTF-8');

include "config.php";

$postjson = json_decode(file_get_contents('php://input'), true);
$today = date('Y-m-d');


$postjson['aksi']=='getUser';
    $data = array();
    $query = mysqli_query($mysqli, "SELECT * FROM users WHERE id = '$id'");

    while($row = mysqli_fetch_array($query)){

        $data[] = array(
            "id" => $row[0],
            "name" => $row[1],
            "name2" => $row[2],
            "email" => $row[3],
            "password" => $row[4]
        );
    }

    if($query) $result = json_encode(array('success'=>true, 'result'=>$data));
    else $result = json_encode(array('success'=>false));
    
    echo $result;



?>
    
    