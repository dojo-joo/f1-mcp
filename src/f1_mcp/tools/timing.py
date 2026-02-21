"""Tools for live timing: position, intervals, and race control."""

from mcp.server.fastmcp import FastMCP

from f1_mcp.client import fetch, fetch_latest_session_key


def register(mcp: FastMCP) -> None:

    @mcp.tool()
    async def get_position(
        session_key: int | None = None,
        driver_number: int | None = None,
    ) -> list[dict]:
        """Get driver track positions throughout a session.

        Returns timestamped position records showing each driver's running order.
        Useful for tracking overtakes and position changes in real time.

        Args:
            session_key: Session identifier. Defaults to the latest session.
            driver_number: Filter to a single driver, e.g. 1 for Verstappen.
        """
        if session_key is None:
            session_key = await fetch_latest_session_key()
        return await fetch("position", {
            "session_key": session_key,
            "driver_number": driver_number,
        })

    @mcp.tool()
    async def get_intervals(
        session_key: int | None = None,
        driver_number: int | None = None,
    ) -> list[dict]:
        """Get time gaps between drivers during a session.

        Returns the interval to the car ahead and the gap to the leader
        for each driver, updated throughout the session. Essential for
        understanding race strategy and DRS train situations.

        Args:
            session_key: Session identifier. Defaults to the latest session.
            driver_number: Filter to a single driver.
        """
        if session_key is None:
            session_key = await fetch_latest_session_key()
        return await fetch("intervals", {
            "session_key": session_key,
            "driver_number": driver_number,
        })

    @mcp.tool()
    async def get_race_control(
        session_key: int | None = None,
        driver_number: int | None = None,
        category: str | None = None,
        flag: str | None = None,
    ) -> list[dict]:
        """Get race control messages for a session.

        Covers flags (yellow, red, chequered), safety car / virtual safety car
        deployments, DRS enabled/disabled zones, penalties, and steward
        decisions. Indispensable for following a live race weekend.

        Args:
            session_key: Session identifier. Defaults to the latest session.
            driver_number: Filter messages relating to a specific driver.
            category: Message category, e.g. "Flag", "SafetyCar", "Drs",
                      "ChequeredFlag", "Other".
            flag: Flag colour filter, e.g. "YELLOW", "RED", "GREEN",
                  "SAFETY CAR", "VIRTUAL SAFETY CAR".
        """
        if session_key is None:
            session_key = await fetch_latest_session_key()
        return await fetch("race_control", {
            "session_key": session_key,
            "driver_number": driver_number,
            "category": category,
            "flag": flag,
        })
