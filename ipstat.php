
<html>
<body>
<style>
.main {
// border: 1px solid black;
}
td, th{
  font-family: sans-serif;
  font-size: 10pt;
}
td {
  text-align: left;
}

th, td {
  text-align: left;
  padding: 8px;
}

tr:nth-child(even){background-color: #f2f2f2}

th {
  text-align: left;
  background-color: #4CAF50;
  color: white;
}

</style>


<?php

/*

//enable debugging by uncommenting

error_reporting(E_ALL);
ini_set('display_errors', '1');

if(function_exists('exec')) {
    echo "exec is enabled";
} else {
    echo "exec is disabled";
}*/

$rootpath="/home/user/github/netmonitor";

$time_start = microtime(true); 

$total = array();
exec ("/usr/bin/python3 $rootpath/query.py todaytotal", $total);

//echo("todaytotal:".(microtime(true) - $time_start)."<br/>");


//$time_start = microtime(true); 
$sources = array();
exec ("/usr/bin/python3 $rootpath/query.py sources", $sources);

//echo("sources:".(microtime(true) - $time_start)."<br/>");

//$time_start = microtime(true); 
$dests = array();
exec ("/usr/bin/python3 $rootpath/query.py dests", $dests);

//echo("dests:".(microtime(true) - $time_start)."<br/>");

//$time_start = microtime(true); 
$localnetsources = array();
exec ("/usr/bin/python3 $rootpath/query.py localnetsources", $localnetsources);
//echo("localnetsources:".(microtime(true) - $time_start)."<br/>");

//$time_start = microtime(true); 
$localnetdests = array();
exec ("/usr/bin/python3 $rootpath/query.py localnetdests", $localnetdests);
//echo("localnetdests:".(microtime(true) - $time_start)."<br/>");

//$time_start = microtime(true); 
$latest = array();
exec ("/usr/bin/python3 $rootpath/query.py latest", $latest);
//echo("latest:".(microtime(true) - $time_start)."<br/>");


//$time_start = microtime(true); 
$sourcesport = array();
exec ("/usr/bin/python3 $rootpath/query.py sourcesportsonly", $sourcesport);

//echo("sourcesport:".(microtime(true) - $time_start)."<br/>");

//$time_start = microtime(true); 
$destsport = array();
exec ("/usr/bin/python3 $rootpath/query.py destsportsonly", $destsport);

//echo("destsport:".(microtime(true) - $time_start)."<br/>");


$rows = json_decode($total[0]);

echo("<h4>Local Network</h4>");
//echo("<h4>".gethostname()."</h4>");
echo("<strong>Total: ".round(($rows[1][0]/1000.0/1000.0),3)."</strong><br/><br/>");


$rows = json_decode($sources[0]);

echo "<table>";

echo("<tr>");
echo("<td>Sources <br/>");
echo "<table class='main'>";

echo("<tr>");
echo("<th>Src Host</th><th>Bytes In</th>");
echo("</tr>");

$i=0;
foreach ($rows as $row)
{
  if($i==0) { $i++; continue; }
  echo("<tr>");
  echo("<td>".$row[1]."</td><td>".$row[0]."</td>");
  echo("</tr>");
}

echo "</table></td>";

$rows = json_decode($dests[0]);

echo("<td>Dests <br/>");
echo "<table class='main'>";
echo("<tr>");
echo("<th>Dst Host</th><th>Bytes Out</th>");

echo("</tr>");

$i=0;
foreach ($rows as $row) {
  if($i==0) { $i++; continue; }
  echo("<tr>");
  echo("<td>".$row[1]."</td><td>".$row[0]."</td>");
  echo("</tr>");
}
echo "</table></td>";
echo("</tr>");
echo("</table>");

echo("<table>");
echo("<tr>");

$rows = json_decode($localnetsources[0]);

echo "<table><tr>";
echo("<td>Localnet Sources <br/>");
echo "<table class='main'>";
echo("<tr>");
echo("<th>Host</th><th>Bytes In</th>");
echo("</tr>");

$i=0;

foreach ($rows as $row) {
  if($i==0) { $i++; continue; }
  echo("<tr>");
  echo("<td>".$row[1]."</td><td>".$row[0]."</td>");
  echo("</tr>");
}
echo "</table></td>"; 

$rows = json_decode($localnetdests[0]);

echo("<td>Localnet Dests<br/>");
echo "<table class='main'>";
echo("<tr>");
echo("<th>Host</th><th>Bytes Out</th>"); 
echo("</tr>");

$i=0;

foreach ($rows as $row) {
  if($i==0) { $i++; continue; }
  echo("<tr>");
  echo("<td>".$row[1]."</td><td>".$row[0]."</td>");
  echo("</tr>");
}
echo "</table></td>"; 
echo("</tr>");
echo("</table>");
echo "</td></tr></table>";



$rows = json_decode($latest[0]);


echo "<table><tr>";
echo("<td>Latest <br/>");

echo "<table class='main'>";
echo("<tr>");
echo("<th>Time</th>"
."<th>Update Time</th>"
."<th>Src Host</th>"
."<th>Src Port</th>"
."<th>Dest Host</th>"
."<th>Dest Port</th>"
."<th>Protocol</th>"
."<th>Type</th>"
."<th>Len</th>");

echo("</tr>");

$i=0;


//"id", "ptime", "srchost", "srcport", "dsthost", 
//"dstport", "protocol", "ptype", "plen"

foreach ($rows as $row) {
  if($i==0) { $i++; continue; }
  echo("<tr>");
  echo("<td>".$row[1]."</td><td>".$row[2]."</td><td>".$row[3]."</td>");
  echo("<td>".$row[4]."</td><td>".$row[5]."</td>");
  echo("<td>".$row[6]."</td><td>".$row[7]."</td>");
  echo("<td>".$row[8]."</td><td>".$row[9]."</td>");
  echo("</tr>");
}
echo "</table></td>";
echo("</tr>");
echo "</table>";
echo("</td></tr></table>");

$rows = json_decode($sourcesport[0]);

echo "<table><tr>";
echo("<td>Sources Ports <br/>");
echo "<table class='main'>";
echo("<tr>");
echo("<th>Port</th><th>Bytes In</th>");
echo("</tr>");

$i=0;

foreach ($rows as $row) {
  if($i==0) { $i++; continue; }
  echo("<tr>");
  echo("<td>".$row[0]."</td><td>".$row[1]."</td>");
  echo("</tr>");
}
echo "</table></td>"; 

$rows = json_decode($destsport[0]);

echo("<td>Dests Ports<br/>");
echo "<table class='main'>";
echo("<tr>");
echo("<th>Port</th><th>Bytes Out</th>"); 
echo("</tr>");

$i=0;

foreach ($rows as $row) {
  if($i==0) { $i++; continue; }
  echo("<tr>");
  echo("<td>".$row[0]."</td><td>".$row[1]."</td>");
  echo("</tr>");
}
echo "</table></td>"; 
echo("</tr>");
echo("</table>");
echo "</td></tr></table>";


echo("<hr/>Render time: ".round((microtime(true) - $time_start),3)." secs");

?>

</body>
</html>
