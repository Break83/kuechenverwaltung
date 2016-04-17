<?php
/*
 * This file should demonstrate how to connect to the python-server
 * and how to close it.
 *
 * To use this php-script. please start the python server by doing:
 * python -b /path/to/the/main/py/of/this/project/main.py
 *
 * Now reload this webpage.
 * */



/* get the current weight */
$s = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
socket_connect($s, "localhost", 32792);
socket_send($s, "get weight", 10, MSG_EOF);
$weight = "untitled";
socket_recv($s, $weight, 4096, MSG_PEEK);
socket_close($s);
print_r("current weight: " . $weight . "<br/>");


/* get the current weight */
$s = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
socket_connect($s, "localhost", 32792);
socket_send($s, "store weight johndoe .756", 27, MSG_EOF);
$entry = "untitled";
socket_recv($s, $entry, 4096, MSG_PEEK);
socket_close($s);
print_r("entry: " . $entry . "<br/>");


/* get all registred values */
$s = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
socket_connect($s, "localhost", 32792);
socket_send($s, "get all", 7, MSG_EOF);
$all = "untitled";
socket_recv($s, $all, 4096, MSG_PEEK);
socket_close($s);
print_r("all: " . $all . "<br/>");

/* to close the server send the following lines via php:*/
$s = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
socket_connect($s, "localhost", 32792);
socket_send($s, "close server", 12, MSG_EOF);
$a = "";
socket_recv($s, $a, 4096, MSG_PEEK);
socket_close($s);

?>


