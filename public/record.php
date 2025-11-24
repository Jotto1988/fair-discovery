<?php
header("Content-Type: application/json");
session_start(); // Start session to track unique visitors per browser session

try {
    // 1. Get Incoming Data
    $input = file_get_contents("php://input");
    $data = json_decode($input, true);
    
    // Basic validation
    if (!$data || !isset($data["path"]) || !isset($data["score"])) {
        http_response_code(400);
        echo json_encode(["error" => "Invalid data"]);
        exit;
    }

    $file = __DIR__ . "/discovery.json";
    
    // 2. Open File with LOCK (Prevents data corruption)
    $fp = fopen($file, 'c+');
    if (!flock($fp, LOCK_EX)) {
        throw new Exception("Could not lock file");
    }

    // Read current data
    $fileSize = filesize($file);
    $jsonContent = $fileSize > 0 ? fread($fp, $fileSize) : "{}";
    $log = json_decode($jsonContent, true);

    // Initialize structure if missing
    if (!isset($log["visitors"])) {
        $log["visitors"] = [
            "current_week_start" => date("Y-m-d"),
            "week_1" => 0, "week_2" => 0, "week_3" => 0, "week_4" => 0
        ];
    }

    // ---------------------------------------------------------
    // LOGIC A: Weekly Rotation (Sat/Mon Logic)
    // ---------------------------------------------------------
    $lastStart = strtotime($log["visitors"]["current_week_start"]);
    $now = time();
    $daysSince = ($now - $lastStart) / (60 * 60 * 24);

    // If it's been more than 7 days, OR if it's Monday (1) and we haven't reset yet
    $isMonday = (date('N') == 1); 
    
    if ($daysSince >= 7 || ($isMonday && $daysSince >= 1)) {
        // Shift Data (Rolling History)
        $log["visitors"]["week_4"] = $log["visitors"]["week_3"];
        $log["visitors"]["week_3"] = $log["visitors"]["week_2"];
        $log["visitors"]["week_2"] = $log["visitors"]["week_1"];
        $log["visitors"]["week_1"] = 0; // Reset current week
        
        // Set new start date
        $log["visitors"]["current_week_start"] = date("Y-m-d");
    }

    // ---------------------------------------------------------
    // LOGIC B: Count Unique Visitor (High Accuracy)
    // ---------------------------------------------------------
    $score = (int)$data["score"];
    
    if (!isset($_SESSION['counted_visitor']) && $score > 0) {
        $log["visitors"]["week_1"]++;
        $_SESSION['counted_visitor'] = true;
    }

    // ---------------------------------------------------------
    // LOGIC C: Update Page Engagement
    // ---------------------------------------------------------
    $path = filter_var($data["path"], FILTER_SANITIZE_URL);
    
    $found = false;
    foreach ($log["pages"] as &$page) {
        if ($page["url"] === $path) {
            $page["score"] += $score;
            $found = true;
            break;
        }
    }
    // Auto-Discovery: If page not found, add it.
    if (!$found) {
        $log["pages"][] = ["url" => $path, "score" => $score];
    }

    // 3. Save and Unlock
    ftruncate($fp, 0); // Clear file
    rewind($fp);
    fwrite($fp, json_encode($log, JSON_PRETTY_PRINT));
    flock($fp, LOCK_UN);
    fclose($fp);

    echo json_encode(["status" => "ok"]);

} catch (Exception $e) {
    http_response_code(500);
    echo json_encode(["error" => $e->getMessage()]);
}
?>