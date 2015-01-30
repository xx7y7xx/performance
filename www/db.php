<?php

/*
CREATE TABLE user4 (
  uid INTEGER PRIMARY KEY   AUTOINCREMENT,
  name varchar NOT NULL,
  pay int(11) NOT NULL,
  boost boolean NOT NULL DEFAULT 0,
  quality float NOT NULL DEFAULT 1
);
*/

$TB = "user4";

class MyDB extends SQLite3
{
   function __construct()
   {
      $this->open('jixiao.db');
   }
};

function check_param( $param_name )
{
    if ( isset($_POST[$param_name]) && $_POST[$param_name] != "" )
    {
        return $_POST[$param_name];
    }
    else
    {
        die ( '{"status" : 1, "message" : "field '.$param_name.' not found"}' );
    }
}

if ( isset($_POST["oper"]) )
{

    $db = new MyDB();
    if(!$db){
       echo $db->lastErrorMsg();
    } else {
       //echo "Opened database successfully\n";
    }

    switch($_POST["oper"])
    {
        case "add":
            // check post param
            $name = check_param("name");
            $pay = check_param("pay");
            $boost = check_param("boost");
            $quality = check_param("quality");
            $sql = <<<EOF
               INSERT INTO $TB (name, pay, boost, quality)
               VALUES ("$name", $pay, $boost, $quality);
EOF;
            break;
        case "edit":
            // check post param
            $id = check_param("id");
            $name = check_param("name");
            $pay = check_param("pay");
            $boost = check_param("boost");
            $quality = check_param("quality");
            $sql = <<<EOF
               UPDATE $TB
               SET name="$name", pay=$pay, boost=$boost, quality=$quality
               WHERE uid=$id;
EOF;
            break;
        case "del":
            // check post param
            $id = check_param("id");
            $sql = <<<EOF
               DELETE FROM $TB
               WHERE uid=$id;
EOF;
            break;
        default:
            exit;
            break;
    }


    $ret = $db->exec($sql);
    if(!$ret){
       echo $db->lastErrorMsg();
    } else {
       //echo "Records created successfully\n";
    }
    $db->close();

    exit;
}

if ( isset($_GET["action"]) && $_GET["action"] == "read" )
{
    $db = new MyDB();
    if ( !$db )
    {
        echo $db->lastErrorMsg();
    }
    else
    {
        //echo "open suc\n";
    }

    $sql = <<<EOF
        SELECT COUNT(*) AS count FROM $TB;
EOF;
    $ret = $db->query($sql);
    $row = $ret->fetchArray(SQLITE3_ASSOC);
    $count = $row["count"];

    $sql = <<<EOF
        SELECT * FROM $TB;
EOF;

    $res = new stdClass();
    $res->page = 1;
    $res->total = 1;
    $res->records = $count;

    $ret = $db->query($sql);

    $i = 0;
    while( $row = $ret->fetchArray(SQLITE3_ASSOC) )
    {
        $res->rows[$i]["id"] = $row["uid"];
        $res->rows[$i]["cell"] = array(
            $row["uid"],
            $row["name"],
            $row["pay"],
            $row["boost"],
            $row["quality"]
        );
        $i++;
    }
    echo json_encode($res);
}
?>
