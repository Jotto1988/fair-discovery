<?php
header("Content-Type: application/json");

try {
  $data = json_decode(file_get_contents("php://input"), true);
  if (!$data || !isset($data["path"]) || !isset($data["score"]) || !is_numeric($data["score"])) {
    http_response_code(400);
    echo json_encode(["error" => "Invalid or missing data"]);
    exit;
  }

  $file = __DIR__ . "/discovery.json";
  $log = file_exists($file) ? json_decode(file_get_contents($file), true) : [
    "site" => "intpanelshop.co.za",
    "pages" => []
  ];

  $path = filter_var($data["path"], FILTER_SANITIZE_URL);
  $score = (int)$data["score"];

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

  if (!file_put_contents($file, json_encode($log, JSON_PRETTY_PRINT))) {
    http_response_code(500);
    echo json_encode(["error" => "Failed to save data"]);
    exit;
  }

  echo json_encode(["status" => "ok"]);
} catch (Exception $e) {
  http_response_code(500);
  echo json_encode(["error" => "Server error: " . $e->getMessage()]);
}
?>