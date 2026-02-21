"""Tools for sessions and meetings."""

from mcp.server.fastmcp import FastMCP

from f1_mcp.client import fetch, fetch_latest_session_key


def register(mcp: FastMCP) -> None:

    @mcp.tool()
    async def get_latest_session() -> dict:
        """Get the most recent F1 session (practice, qualifying, sprint, or race).

        Returns full session metadata including session_key, which is required
        by most other tools. Call this first when you want live or recent data.
        """
        data = await fetch("sessions", {"order_by": "-date_start", "limit": 1})
        return data[0] if data else {}

    @mcp.tool()
    async def get_sessions(
        year: int | None = None,
        country_name: str | None = None,
        session_type: str | None = None,
        circuit_short_name: str | None = None,
    ) -> list[dict]:
        """Search for F1 sessions with optional filters.

        Args:
            year: Championship year, e.g. 2024.
            country_name: Country name, e.g. "Monaco", "Italy", "United Kingdom".
            session_type: One of "Practice 1", "Practice 2", "Practice 3",
                          "Sprint", "Sprint Qualifying", "Qualifying", "Race".
            circuit_short_name: Short circuit name, e.g. "monza", "spa", "silverstone".

        Returns a list of sessions ordered by most recent first.
        """
        return await fetch("sessions", {
            "year": year,
            "country_name": country_name,
            "session_type": session_type,
            "circuit_short_name": circuit_short_name,
        })

    @mcp.tool()
    async def get_meetings(
        year: int | None = None,
        country_name: str | None = None,
        meeting_name: str | None = None,
    ) -> list[dict]:
        """Search for F1 race weekends (meetings).

        A meeting groups all sessions for a single Grand Prix weekend.

        Args:
            year: Championship year, e.g. 2024.
            country_name: Country of the race, e.g. "Monaco", "Bahrain".
            meeting_name: Partial or full meeting name, e.g. "British Grand Prix".
        """
        return await fetch("meetings", {
            "year": year,
            "country_name": country_name,
            "meeting_name": meeting_name,
        })
