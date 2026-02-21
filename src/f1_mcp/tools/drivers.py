"""Tools for drivers and championship standings."""

from mcp.server.fastmcp import FastMCP

from f1_mcp.client import fetch, fetch_latest_session_key


def register(mcp: FastMCP) -> None:

    @mcp.tool()
    async def get_drivers(
        session_key: int | None = None,
        driver_number: int | None = None,
        name_acronym: str | None = None,
    ) -> list[dict]:
        """Get driver information for a session.

        Returns details including full name, team, driver number, country code,
        and headshot URL.

        Args:
            session_key: Session identifier. Defaults to the latest session.
            driver_number: Filter to a specific driver by their race number,
                e.g. 44 for Hamilton, 1 for Verstappen.
            name_acronym: Three-letter driver acronym, e.g. "HAM", "VER", "LEC".
        """
        if session_key is None:
            session_key = await fetch_latest_session_key()
        return await fetch("drivers", {
            "session_key": session_key,
            "driver_number": driver_number,
            "name_acronym": name_acronym,
        })

    @mcp.tool()
    async def get_championship_drivers(
        session_key: int | None = None,
    ) -> list[dict]:
        """Get the driver championship standings after a race session.

        Returns each driver's points total and championship position.
        Only available for race sessions (not practice or qualifying).

        Args:
            session_key: Session identifier for a completed race.
                Defaults to the latest session.
        """
        if session_key is None:
            session_key = await fetch_latest_session_key()
        return await fetch("championship_drivers", {"session_key": session_key})

    @mcp.tool()
    async def get_championship_teams(
        session_key: int | None = None,
    ) -> list[dict]:
        """Get the constructor (team) championship standings after a race session.

        Returns each team's points total and championship position.
        Only available for race sessions (not practice or qualifying).

        Args:
            session_key: Session identifier for a completed race.
                Defaults to the latest session.
        """
        if session_key is None:
            session_key = await fetch_latest_session_key()
        return await fetch("championship_teams", {"session_key": session_key})
