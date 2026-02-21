"""Tools for telemetry, tyre strategy, and track conditions."""

from mcp.server.fastmcp import FastMCP

from f1_mcp.client import fetch, fetch_latest_session_key

# Cap high-frequency endpoints to avoid flooding the context window
_CAR_DATA_LIMIT = 100


def register(mcp: FastMCP) -> None:

    @mcp.tool()
    async def get_laps(
        session_key: int | None = None,
        driver_number: int | None = None,
        lap_number: int | None = None,
    ) -> list[dict]:
        """Get lap times and sector data for a session.

        Returns each lap's duration, sector times, pit-in/out flags, and
        whether the lap set a personal or overall fastest time. Ideal for
        pace analysis and comparing drivers across a stint.

        Args:
            session_key: Session identifier. Defaults to the latest session.
            driver_number: Filter to a single driver, e.g. 44 for Hamilton.
            lap_number: Filter to a specific lap number.
        """
        if session_key is None:
            session_key = await fetch_latest_session_key()
        return await fetch("laps", {
            "session_key": session_key,
            "driver_number": driver_number,
            "lap_number": lap_number,
        })

    @mcp.tool()
    async def get_stints(
        session_key: int | None = None,
        driver_number: int | None = None,
        stint_number: int | None = None,
        compound: str | None = None,
    ) -> list[dict]:
        """Get tyre stint data for a session.

        Returns each stint's compound, lap range, and tyre age. Use this to
        reconstruct tyre strategies and compare undercut/overcut windows.

        Args:
            session_key: Session identifier. Defaults to the latest session.
            driver_number: Filter to a single driver.
            stint_number: Filter to a specific stint number (1 = first stint).
            compound: Tyre compound filter — "SOFT", "MEDIUM", "HARD",
                      "INTERMEDIATE", or "WET".
        """
        if session_key is None:
            session_key = await fetch_latest_session_key()
        return await fetch("stints", {
            "session_key": session_key,
            "driver_number": driver_number,
            "stint_number": stint_number,
            "compound": compound,
        })

    @mcp.tool()
    async def get_pit(
        session_key: int | None = None,
        driver_number: int | None = None,
        lap_number: int | None = None,
    ) -> list[dict]:
        """Get pit stop data for a session.

        Returns pit stop lap, pit lane duration, and stop number per driver.
        Combine with get_stints to analyse full tyre strategies.

        Args:
            session_key: Session identifier. Defaults to the latest session.
            driver_number: Filter to a single driver.
            lap_number: Filter to stops made on a specific lap.
        """
        if session_key is None:
            session_key = await fetch_latest_session_key()
        return await fetch("pit", {
            "session_key": session_key,
            "driver_number": driver_number,
            "lap_number": lap_number,
        })

    @mcp.tool()
    async def get_weather(
        session_key: int | None = None,
    ) -> list[dict]:
        """Get weather conditions sampled throughout a session.

        Returns air and track temperatures, humidity, wind speed/direction,
        rainfall flag, and pressure. Useful for understanding grip levels
        and tyre degradation context.

        Args:
            session_key: Session identifier. Defaults to the latest session.
        """
        if session_key is None:
            session_key = await fetch_latest_session_key()
        return await fetch("weather", {"session_key": session_key})

    @mcp.tool()
    async def get_car_data(
        session_key: int | None = None,
        driver_number: int | None = None,
        lap_number: int | None = None,
    ) -> list[dict]:
        """Get car telemetry sampled at ~3.7 Hz during a session.

        Returns speed, RPM, gear, throttle %, brake state, and DRS status.
        Results are capped at 100 samples — use lap_number to focus on a
        specific lap and avoid large payloads.

        Args:
            session_key: Session identifier. Defaults to the latest session.
            driver_number: Filter to a single driver (strongly recommended).
            lap_number: Filter to a specific lap to keep the response manageable.
        """
        if session_key is None:
            session_key = await fetch_latest_session_key()
        return await fetch("car_data", {
            "session_key": session_key,
            "driver_number": driver_number,
            "lap_number": lap_number,
        })

    @mcp.tool()
    async def get_team_radio(
        session_key: int | None = None,
        driver_number: int | None = None,
    ) -> list[dict]:
        """Get team radio message metadata for a session.

        Returns timestamps and audio URLs for team radio transmissions.
        Useful for understanding strategy calls, driver feedback, and
        race incidents as they happened.

        Args:
            session_key: Session identifier. Defaults to the latest session.
            driver_number: Filter to a single driver.
        """
        if session_key is None:
            session_key = await fetch_latest_session_key()
        return await fetch("team_radio", {
            "session_key": session_key,
            "driver_number": driver_number,
        })
