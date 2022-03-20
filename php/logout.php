<!--- Resets all the $_SESSION variables and redirects to the homepage. -->

<?php
 session_start();

 $_SESSION = array();
 session_destroy();

 header("Location: login.page.html");
?>
