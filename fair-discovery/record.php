<?php
header("Content-Type: application/json");

$data = json_decode(file_get_contents("php://input"), true);
if (!$data || !isset($data["path"]) || !isset($data["score"])) {
  http_response_code(400);
  echo json_encode(["error" => "Invalid data"]);
  exit;
}

$file = __DIR__ . "/discovery.json";
$log = file_exists($file) ? json_decode(file_get_contents($file), true) : [
  "site" => $_SERVER["HTTP_HOST"],
  "pages" => []
];

$path = $data["path"];
$score = $data["score"];

$found = false;
foreach ($log["pages"] as &$page) {
  if ($page["url"] === $path) {
    $page["score"] += $score;
    $found = true;
    break;
  }
}
if (!$found) {
  $log["pages"][] = ["url" => $path, "score" => $score];
}

file_put_contents($file, json_encode($log, JSON_PRETTY_PRINT));
echo json_encode(["status" => "ok"]);
?>