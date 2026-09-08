# Amul chocolate whey protein — stock notifier

Pings a Telegram chat when **Amul Chocolate Whey Protein (34 g)** comes back in
stock in the **30-sachet** or **60-sachet** pack, for pincode **560100**.

Runs on a GitHub Actions cron (`.github/workflows/amul-stock.yml`), roughly
every 10 minutes. No server, no database.

## Setup

### 1. Create a Telegram bot

1. Message [@BotFather](https://t.me/BotFather) and send `/newbot`.
2. Follow the prompts; it replies with a token like `123456789:AAE...`.
3. Send your new bot any message (it can't message you until you do).
4. Get your chat ID — open this in a browser, replacing `<TOKEN>`:
   `https://api.telegram.org/bot<TOKEN>/getUpdates`
   Look for `"chat":{"id":123456789`. That number is your chat ID (negative for groups).

### 2. Add repository secrets

**Settings → Secrets and variables → Actions → Secrets → New repository secret**

| Secret | Value |
| --- | --- |
| `TELEGRAM_BOT_TOKEN` | the token from BotFather |
| `TELEGRAM_CHAT_ID` | the chat ID from `getUpdates` |

### 3. (Optional) Override pincode or store

Under the **Variables** tab of the same page:

| Variable | Default | Notes |
| --- | --- | --- |
| `AMUL_PINCODE` | `560100` | Used to look up your regional substore |
| `AMUL_STORE` | *(unset)* | Substore alias, e.g. `karnataka`. Set this only if the pincode lookup fails — it skips the lookup entirely |

### 4. Enable it

Scheduled workflows **only run from the repository's default branch**. The cron
won't fire while this lives on a feature branch — merge to `main` first.

Then trigger a manual run to confirm the wiring: **Actions → Amul protein stock
watch → Run workflow**, with **force_notify** ticked. You should get a Telegram
message even if the packs are out of stock — that proves the token, chat ID and
store resolution all work. Untick it afterwards.

## How it works

Amul's stock is **regional**. The shop maps your pincode to a "substore" and
reports availability per substore, so the script must set the store preference
*before* asking about products:

1. `GET /` and `GET /api/1/entity/ms.homepage` — mint session cookies
2. `GET /api/1/entity/ms.substore` — resolve pincode → substore alias
3. `PUT /entity/ms.settings/_/setPreferences` — pin the session to that substore
4. `GET /api/1/entity/ms.products?q={"alias":"…"}` — read each target SKU

A pack counts as buyable when `available` is truthy **and** `inventory_quantity`
is above zero (`available` alone can lag a sell-out).

### Alerts fire once per restock

The previous result is kept in `.amul-state/state.json`, persisted between runs
via the Actions cache. Only an **out-of-stock → in-stock transition** sends a
message, so a pack that stays in stock for three hours produces one alert, not
eighteen. When it sells out the state resets and the next restock alerts again.

### If Amul renames a SKU

Targets are matched by URL alias. If an alias stops resolving, the script falls
back to scanning the whole protein category and matching on name
(`chocolate` + `pack of 30|60 sachets`), so a rename degrades rather than breaks.

## Local use

```bash
pip install -r .tools/amul-notify/requirements.txt

# Check stock and print, without messaging Telegram:
python .tools/amul-notify/check_stock.py --dry-run

# Inspect the raw API response (use this if field names change):
python .tools/amul-notify/check_stock.py --dry-run --dump

# Run the offline logic tests:
python .tools/amul-notify/test_logic.py
```

## Known limitations

- **Cron timing is best-effort.** GitHub can delay scheduled runs by 10–30+
  minutes under load. Amul protein is known to sell out within minutes of a
  restock, so this will sometimes miss one. For tighter coverage, run
  `check_stock.py` from a local cron as well.
- **Scheduled workflows auto-disable after 60 days** with no repository
  activity. GitHub emails you first; re-enable from the Actions tab.
- **The API is undocumented and unofficial.** Amul can change field names or
  endpoints without notice. If the job starts failing, run it with `dump: true`
  and compare the JSON against `is_available()` in `check_stock.py`.
- Availability is only as accurate as the substore lookup. If alerts look wrong
  for your area, set `AMUL_STORE` explicitly.
