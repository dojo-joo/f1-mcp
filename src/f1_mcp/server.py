"""F1 MCP Server — entry point."""

from mcp.server.fastmcp import FastMCP

from f1_mcp.tools import drivers, sessions, summary, telemetry, timing

mcp = FastMCP(
    name="f1-mcp",
    instructions=(
        "You have access to real-time and historical Formula 1 data via the "
        "OpenF1 API. Use get_latest_session to anchor all live queries. "
        "For race analysis, prefer get_race_summary as your starting point. "
        "Telemetry (get_car_data) returns high-frequency data — always filter "
        "by driver_number and lap_number to keep responses manageable."
    ),
)

sessions.register(mcp)
drivers.register(mcp)
timing.register(mcp)
telemetry.register(mcp)
summary.register(mcp)


def main() -> None:
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
