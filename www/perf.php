<?php
if ( isset($_POST["action"]) && $_POST["action"] == "gen" )
{
    $url = "http://192.168.2.21:8080/job/performance2/build?token=3Y33nfbU0gd7rxOgvM088JyJPVqd20jt";
    //$url = "http://192.168.2.21:8080/view/check/job/xuanran001_gluenode_env/build?token=sp12345678";
    $res = file_get_contents($url);
    echo "0";
    exit;
}
/*
if ( isset($_GET["action"]) && $_GET["action"] == "status" )
{
    $url = 'http://192.168.2.21:8080/view/check/job/xuanran001_gluenode_env/buildHistory/ajax';
    $data = array('key1' => 'value1', 'key2' => 'value2');
    
    // use key 'http' even if you send the request to https://...
    $options = array(
        'http' => array(
            'header'  => "Content-type: application/x-www-form-urlencoded\r\nn: 14\r\n",
            'method'  => 'POST',
            'content' => http_build_query($data),
        ),
    );
    $context  = stream_context_create($options);
    $result = file_get_contents($url, false, $context);
    
    echo $result;
}
*/
?>
<html>
    <head>
        <meta charset="utf-8">
        <script src="http://libs.baidu.com/jquery/1.9.0/jquery.js"></script>
        <script src="http://libs.baidu.com/bootstrap/3.0.3/js/bootstrap.js"></script>
        <link href="http://libs.baidu.com/bootstrap/3.0.3/css/bootstrap.css" rel="stylesheet">
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
            <li class="active"><a href="#">生成绩效</a></li>
            <li><a href="/oa/man.php">员工管理</a></li>
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
        <p>
            <a id="gen-btn" class="btn btn-lg btn-primary" role="button">生成绩效报告</a>
        </p>
        <iframe id="result-win" src="./ods/?C=M;O=D" width="800" height="400">
        </iframe>
      </div>

    </div> <!-- /container -->

<div class="modal js-loading-bar">
 <div class="modal-dialog">
   <div class="modal-content">
     <div class="modal-body">
       <div class="progress progress-popup">
        <div class="progress-bar"></div>
       </div>
     </div>
   </div>
 </div>
</div>

<style>
.js-loading-bar {
    top: 20%;
}
.progress-bar.animate {
   width: 100%;
   -webkit-transition: width 30.0s ease !important;
      -moz-transition: width 30.0s ease !important;
        -o-transition: width 30.0s ease !important;
           transition: width 30.0s ease !important;
}
</style>

        <script>
        $( document ).ready(function() {

            // Setup
            $('.js-loading-bar').modal({
              backdrop: 'static',
              show: false
            });

            var refresh_iframe = function() {
                document.getElementById("result-win").contentDocument.location.reload(true);
            };
            //setInterval(refresh_iframe, 5000);

            $("#gen-btn").on("click", function() {
                var data = {};
                data.action = "gen";
                $.post("perf.php", data, function(data) {
                    console.log(data);
                });

                var $modal = $('.js-loading-bar'),
                    $bar = $modal.find('.progress-bar');
                
                $modal.modal('show');
                $bar.addClass('animate');

                setTimeout(function() {
                    refresh_iframe();
                    $bar.removeClass('animate');
                    $modal.modal('hide');
                }, 20000);
            });

        });
        </script>
    </body>
</html>
