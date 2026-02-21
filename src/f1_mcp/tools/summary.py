"""Compound tools that combine multiple OpenF1 endpoints into rich summaries."""

import asyncio

from mcp.server.fastmcp import FastMCP

from f1_mcp.client import fetch, fetch_latest_session_key


def register(mcp: FastMCP) -> None:

    @mcp.tool()
    async def get_race_summary(
        session_key: int | None = None,
        driver_number: int | None = None,
    ) -> dict:
        """Get a comprehensive race summary combining laps, stints, and pit stops.

        Fetches lap times, tyre stints, and pit stop data in parallel and
        returns them as a unified dict. Optionally scoped to a single driver
        for targeted analysis (e.g. tyre strategy, pace over stints).

        Without a driver filter this gives a full-field overview — useful for
        identifying the fastest laps, most aggressive strategies, and
        who pitted when.

        Args:
            session_key: Session identifier. Defaults to the latest session.
            driver_number: Scope to a single driver for focused analysis.
                           When omitted, data for all drivers is returned.

        Returns:
            {
                "session_key": int,
                "driver_number": int | None,
                "laps": [...],      # lap times and sector splits
                "stints": [...],    # tyre compounds and lap ranges
                "pit_stops": [...], # pit stop laps and durations
            }
        """
        if session_key is None:
            session_key = await fetch_latest_session_key()

        params = {
            "session_key": session_key,
            "driver_number": driver_number,
        }
        # Strip None so the API doesn't receive empty params
        clean = {k: v for k, v in params.items() if v is not None}

        laps, stints, pit_stops = await asyncio.gather(
            fetch("laps", clean),
            fetch("stints", clean),
            fetch("pit", clean),
        )

        return {
            "session_key": session_key,
            "driver_number": driver_number,
            "laps": laps,
            "stints": stints,
            "pit_stops": pit_stops,
        }
