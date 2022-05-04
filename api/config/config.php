<?php 

// header("Access-Control-Allow-Origin: *");
// header("Access-Control-Allow-Methods: POST, GET, DELETE, PUT, PATCH, OPTIONS");
// header("Access-Control-Allow-Headers: X-Requested-With, X-Auth-Token, Content-Type, Accept, Origin,  client-security-token, host, date, cookie, cookie2");
// header("Access-Control-Max-Age: 1728000");
// header("Content-Length: 0");
// header("Content-Type: text/plain");

// $_SERVER = "http://localhost:8100";


// if ($_SERVER['REQUEST_METHOD'] == 'OPTIONS') {
//     // The request is using the POST method
//     header("HTTP/1.1 200 OK");
//     return;

// }

$con = mysqli_connect("localhost", "root", "", "mindme") or die("Couldnt connect to database");

if (isset($_SERVER['HTTP_ORIGIN'])) {

    header("Access-Control-Allow-Origin: {$_SERVER['HTTP_ORIGIN']}");
    header('Access-Control-Allow-Credentials: true');
    header('Access-Control-Max-Age: 86400');    // cache for 1 day
}

// Access-Control headers are received during OPTIONS requests
if ($_SERVER['REQUEST_METHOD'] == 'OPTIONS') {

    if (isset($_SERVER['HTTP_ACCESS_CONTROL_REQUEST_METHOD']))
        // may also be using PUT, PATCH, HEAD etc
        header("Access-Control-Allow-Methods: GET, POST, OPTIONS");         

    if (isset($_SERVER['HTTP_ACCESS_CONTROL_REQUEST_HEADERS']))
        header("Access-Control-Allow-Headers: {$_SERVER['HTTP_ACCESS_CONTROL_REQUEST_HEADERS']}");

    exit(0);
}

?>