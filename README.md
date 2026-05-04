# wildix-user-config-exporter

A Python scraper that extracts full user feature configurations from a **Wildix WMS** PBX system via its internal WebGUI.

## What it does

1. Fetches all user UIDs from the ACL PBX endpoint (paginated, 20 per request)
2. For each UID, scrapes the user feature page (`features_user.php`)
3. Parses and extracts ~40 configuration fields per user
4. Outputs a structured JSON-like dictionary keyed by UID

## Extracted fields

| Field | Description |
|---|---|
| `reject` | Reject all calls |
| `ucf` | No-answer forward |
| `bcf` | Busy forward |
| `fcf` | Forced forward |
| `cw` | Call waiting |
| `timeout` | Timeout forward |
| `mext` | Mobility extension |
| `mext_conf` | Mobility confirmation |
| `email_notify` | Email notifications |
| `sms_notify` | SMS notifications |
| `ring` | Ringtone |
| `shared_voicemail` | Shared voicemail box |
| `hotline` | Hotline destination |
| `delay_hotline` | Hotline delay |
| `cwtone` | Call waiting tone |
| `road` | Ring active device only |
| `unread_messages_via_email` | Unread messages via email |
| `twofactor` | Two-factor authentication |
| `phonebook_lp` / `phonebook_rp` | Phonebook (available/selected) |
| `datetime_format` | Date/time format |
| `datetime_is24h` | 24h clock |
| `popup_url` | Popup URL |
| `open_popup_incoming_calls_when` | Popup trigger (incoming) |
| `open_popup_outgoing_calls_when` | Popup trigger (outgoing) |
| `fkeys` | Function keys |
| `defstatus` | Default presence status |
| `LcallGroupsWhitelist` / `RcallGroupsWhitelist` | Contact center groups |
| `CALLCENTER_MODE` | Call center mode |
| `statusSync` | Status sync |
| `LcallGroups` / `RcallGroups` | Call groups |
| `fax_options_*` | Fax configuration |
| `callgroups` / `pickupgroups` | Call/pickup groups |
| `custom_identities` | Custom identities |
| `LROSTER` / `RROSTER` | Roster (available/selected) |

## Requirements

```
requests
beautifulsoup4
```

Install with:

```bash
pip install -r requirements.txt
```

## Configuration

Edit the following variables directly in `main.py` before running:

```python
ip = "10.10.20.2"          # WMS host IP
cookies = {"PHPSESSID": "your_session_id_here"}
# pbxSerial in the request URL
```

> The session cookie must belong to an **admin** account. Obtain it from your browser after logging into the Wildix WebGUI.

## Usage

```bash
python main.py
```

Output is printed to stdout as a Python dictionary. Redirect to file if needed:

```bash
python main.py > output.json
```

## Notes

- Tested on Wildix WMS with `pbxSerial` format `22110000XXXX`
- The scraper hits `features_user.php?userid={uid}&admin=1` — requires admin privileges
- No rate limiting is applied; add `time.sleep()` if the PBX throttles requests
- `Accept-Language` header is intentionally omitted as it has no effect on attribute-based parsing
