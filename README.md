# f1-mcp

An MCP server that gives Claude real-time and historical Formula 1 data via the [OpenF1 API](https://openf1.org). Ask Claude about lap times, tyre strategies, race control messages, championship standings, and live telemetry — all in natural language.

## Tools

| Tool | What it does |
|------|-------------|
| `get_latest_session` | Resolves the most recent session — use this first for live data |
| `get_sessions` | Search sessions by year, country, or type (race/quali/practice) |
| `get_meetings` | Search race weekends by year or country |
| `get_drivers` | Driver details (name, team, number) for a session |
| `get_championship_drivers` | Driver championship standings after a race |
| `get_championship_teams` | Constructor standings after a race |
| `get_position` | Track positions throughout a session |
| `get_intervals` | Gap to car ahead and to leader per driver |
| `get_race_control` | Flags, safety car, DRS, penalties, steward decisions |
| `get_laps` | Lap times and sector splits |
| `get_stints` | Tyre compound and lap range per stint |
| `get_pit` | Pit stop laps and durations |
| `get_weather` | Air/track temp, humidity, wind, rainfall |
| `get_car_data` | Speed, RPM, gear, throttle, brake, DRS at ~3.7 Hz |
| `get_team_radio` | Radio transmission timestamps and audio URLs |
| `get_race_summary` | Combined laps + stints + pit stops in one call |

All tools default `session_key` to the most recent session, so you rarely need to look it up manually.

## Requirements

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip

## Installation

```bash
git clone https://github.com/dojo-joo/f1-mcp.git
cd f1-mcp
uv sync
```

## Claude Desktop configuration

Add the following to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "f1": {
      "command": "uv",
      "args": ["run", "--project", "/path/to/f1-mcp", "f1-mcp"],
      "env": {}
    }
  }
}
```

Replace `/path/to/f1-mcp` with the actual path where you cloned the repo.

### Live session data (optional)

The free Community tier covers all historical sessions since 2023 with no authentication required. If you have an OpenF1 sponsor-tier account and want live race data, add your token to the env block:

```json
"env": {
  "OPENF1_API_TOKEN": "your-token-here"
}
```

## Example prompts

```
Who had the fastest lap at the 2024 Monaco Grand Prix?
```
```
Show me Verstappen's tyre strategy from the last race.
```
```
What are the current championship standings?
```
```
Any race control messages in the current session?
```
```
Compare Hamilton and Leclerc's lap times in the last qualifying session.
```

## Data coverage

- All sessions from 2023 onward
- ~3 second delay for live session data (free tier)
- Rate limits: 3 requests/second, 30 requests/minute (free tier)

## License

MIT
