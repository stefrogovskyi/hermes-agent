<?php
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Methods: GET, POST, OPTIONS");
header("Access-Control-Allow-Headers: Content-Type");
header("Content-Type: application/json; charset=utf-8");

if ($_SERVER["REQUEST_METHOD"] === "OPTIONS") {
    exit(0);
}

$agent = isset($_GET["agent"]) ? preg_replace("/[^a-z0-9_-]/i", "", $_GET["agent"]) : "hermes";
if (!$agent) $agent = "hermes";

$db_file = __DIR__ . "/kanban_store_" . $agent . ".json";

function load_data($file, $agent) {
    if (file_exists($file)) {
        $txt = file_get_contents($file);
        $json = json_decode($txt, true);
        if (is_array($json) && isset($json["cards"])) {
            return $json;
        }
    }
    return [
        "updated_at" => date("c"),
        "agent" => $agent,
        "columns" => [
            "todo" => "📋 TODO / BACKLOG",
            "in_progress" => "⚡ IN PROGRESS",
            "recurring" => "🔄 RECURRING / CRON",
            "completed" => "✅ COMPLETED / DONE"
        ],
        "cards" => []
    ];
}

function save_data($file, $data) {
    $data["updated_at"] = date("c");
    file_put_contents($file, json_encode($data, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE));
}

$input = json_decode(file_get_contents("php://input"), true);
if (is_array($input) && isset($input["agent"])) {
    $agent = preg_replace("/[^a-z0-9_-]/i", "", $input["agent"]);
    $db_file = __DIR__ . "/kanban_store_" . $agent . ".json";
}

$data = load_data($db_file, $agent);

if ($_SERVER["REQUEST_METHOD"] === "POST" && is_array($input)) {
    $action = isset($input["action"]) ? $input["action"] : "";

    if ($action === "move_card") {
        $card_id = $input["card_id"] ?? "";
        $new_col = $input["new_column_id"] ?? "";
        foreach ($data["cards"] as &$card) {
            if ($card["id"] === $card_id) {
                $card["column_id"] = $new_col;
                save_data($db_file, $data);
                echo json_encode(["status" => "ok", "action" => "move_card", "card_id" => $card_id, "new_column_id" => $new_col]);
                exit;
            }
        }
    }
}

echo json_encode($data, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
