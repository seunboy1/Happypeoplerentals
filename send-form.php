<?php
// Happy People Rentals — form handler for Hostinger (PHP mail()).
// Receives JSON from the Quote and Contact forms and emails it to the inbox below.

header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Headers: Content-Type');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') { http_response_code(204); exit; }
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
  http_response_code(405);
  echo json_encode(['ok' => false, 'error' => 'Method not allowed']);
  exit;
}

// ---- SETTINGS -------------------------------------------------------------
$TO      = 'info@happypeoplerentals.ca';                 // where enquiries land
$FROM    = 'website@happypeoplerentals.ca';              // must be a mailbox on your Hostinger domain
// ---------------------------------------------------------------------------

$raw  = file_get_contents('php://input');
$data = json_decode($raw, true);
if (!is_array($data)) { $data = $_POST; }

// Honeypot: bots fill hidden fields, humans do not.
if (!empty($data['company'])) { echo json_encode(['ok' => true]); exit; }

$clean = function ($v) {
  $v = is_array($v) ? implode(', ', $v) : (string) $v;
  return trim(str_replace(["\r", "\n", "%0a", "%0d"], ' ', strip_tags($v)));
};

$formType = $clean($data['form'] ?? 'Website');
$name     = $clean($data['name'] ?? '');
$email    = $clean($data['email'] ?? '');

if ($name === '' || !filter_var($email, FILTER_VALIDATE_EMAIL)) {
  http_response_code(422);
  echo json_encode(['ok' => false, 'error' => 'Please provide a name and a valid email address.']);
  exit;
}

$labels = [
  'phone' => 'Phone', 'date' => 'Event date', 'type' => 'Event type',
  'guests' => 'Guests', 'location' => 'Location', 'package' => 'Package',
  'games' => 'Games requested', 'subject' => 'Subject', 'notes' => 'Notes',
  'message' => 'Message',
];

$lines = ["Form: $formType", "Name: $name", "Email: $email"];
foreach ($labels as $key => $label) {
  if (isset($data[$key]) && $clean($data[$key]) !== '') {
    $lines[] = $label . ': ' . $clean($data[$key]);
  }
}
$lines[] = 'Sent: ' . date('Y-m-d H:i:s');
$lines[] = 'IP: ' . ($_SERVER['REMOTE_ADDR'] ?? 'unknown');

$subject = ($formType === 'Quote request')
  ? 'Quote request — ' . $name
  : 'Website message — ' . $name;

$headers  = "From: Happy People Rentals <$FROM>\r\n";
$headers .= "Reply-To: $name <$email>\r\n";
$headers .= "Content-Type: text/plain; charset=UTF-8\r\n";

$sent = @mail($TO, $subject, implode("\n", $lines), $headers);

if ($sent) {
  echo json_encode(['ok' => true]);
} else {
  http_response_code(500);
  echo json_encode(['ok' => false, 'error' => 'Mail could not be sent. Please call 343-558-5631.']);
}
