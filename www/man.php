<?php

$ip = $_SERVER['REMOTE_ADDR'];
$permit = array(
    "192.168.0.61",
    "192.168.2.220",
    "192.168.2.140"
);

$admin = $_SERVER['PHP_AUTH_USER'];

if ( !in_array($ip, $permit) )
//if(0)
{
    header("HTTP/1.0 404 Not Found");
    $uri = $_SERVER["REQUEST_URI"];
    echo <<<EOF
<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html><head>
<title>404 Not Found</title>
</head><body>
<h1>Not Found</h1>
<p>The requested URL $uri was not found on this server.</p>
<hr>
<address>Apache/2.2.22 (Ubuntu) Server at 192.168.2.21 Port 80</address>
</body></html>
EOF;
    exit;
}
?>

<html>
    <head>
        <meta charset="utf-8">
        <link rel="stylesheet" type="text/css" media="screen" href="http://xuanran001.com/libs/jqgrid/css/ui.jqgrid.css" />
        <link rel="stylesheet" type="text/css" media="screen" href="http://xuanran001.com/libs/jqgrid/plugins/ui.multiselect.css" />
        <link rel="stylesheet" type="text/css" media="screen" href="http://xuanran001.com/libs/jqgrid/plugins/searchFilter.css" />
        <link rel="stylesheet" type="text/css" media="screen" href="http://xuanran001.com/libs/jquery/jquery-ui.css" />
<script src="http://libs.baidu.com/bootstrap/3.0.3/js/bootstrap.min.js"></script>
<link href="http://libs.baidu.com/bootstrap/3.0.3/css/bootstrap.min.css" rel="stylesheet">
        <style>
            table {
                font-size: 12px;
            }
            .ui-jqgrid .ui-pg-input {
                height: 15px;
            }
        </style>
    </head>
    <body>

    <!-- Fixed navbar -->
    <nav class="navbar navbar-default navbar-static-top">
      <div class="container">
        <div class="navbar-header">
          <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
            <span class="sr-only">Toggle navigation</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <a class="navbar-brand" href="/oa">首页</a>
        </div>
        <div id="navbar" class="navbar-collapse collapse">
          <ul class="nav navbar-nav">
            <li><a href="/oa/perf.php">生成绩效</a></li>
            <li class="active"><a href="#">员工管理</a></li>
            <li><a href="/oa/review.php">自评表</a></li>
          </ul>
          <!--<ul class="nav navbar-nav navbar-right">
            <li><a href="../navbar/">Default</a></li>
            <li><a href="../navbar-static-top/">Static top</a></li>
            <li class="active"><a href="./">Fixed top <span class="sr-only">(current)</span></a></li>
          </ul>-->
        </div><!--/.nav-collapse -->
      </div>
    </nav>

    <div class="container">

      <!-- Main component for a primary marketing message or call to action -->
      <div class="jumbotron">
        <!--<h1>Navbar example</h1>-->
        <?php echo $ip; ?>
        <?php echo $admin; ?>
        <table id="list2"></table>
        <div id="pager2"></div>
      </div>

    </div> <!-- /container -->

        <script src="http://libs.baidu.com/jquery/1.9.0/jquery.js"></script>
        <script src="http://xuanran001.com/libs/jqgrid/js/i18n/grid.locale-cn.js" type="text/javascript"></script>
        <script src="http://xuanran001.com/libs/jqgrid/js/jquery.jqGrid.min.js" type="text/javascript"></script>
        <script>
        $( document ).ready(function() {
            var grid = $("#list2");
            grid.jqGrid({
                url: "db.php?action=read",
                datatype: "json",
                colModel: [
                    //{ label: "action", name:'act',index:'act', width:75,sortable:false},
                    { label: "id", name: 'uid', index: 'uid', width: "110" },
                    { label: "name", name: 'name', index: 'name', width: "300", editable:true },
                    { label: "pay", name: 'pay', index: 'pay', width: "100", editable:true },
                    { label: "boost", name: 'boost', index: 'boost', width: "100", editable:true, edittype:"checkbox", editoptions: {value:"1:0"}, formatter: "checkbox" },
                    { label: "quality", name: 'quality', index: 'quality', width: "100", editable:true }
                ],
                pager: '#pager2',
                //jsonReader: { repeatitems: false },
                rowNum: 40,
                viewrecords: true,
                caption: "user list",
                height: "auto",
                sortorder: 'desc',
                sortname: 'uid',
                ignoreCase: true,
                editurl: "db.php",
            });
        
            grid.jqGrid('navGrid', '#pager2',
                { add: true, edit: true, del: true }, {}, {}, {},
                { multipleSearch: true, multipleGroup: true });
            grid.jqGrid('filterToolbar', { defaultSearch: 'cn', stringResult: true });
            //grid.jqGrid('inlineNav',"#pager2");
        });
        </script>
    </body>
</html>
