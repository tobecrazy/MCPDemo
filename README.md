# Weekly Report System

This system allows you to create weekly reports that are saved to the `reports` directory with timestamps.

## Setup

1. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Make sure the MCP server is running:
   ```
   python weekly_report_server.py
   ```

## Usage

### Method 1: Direct Python Script

You can create a weekly report by running the `create_weekly_report.py` script:

```
python create_weekly_report.py
```

This script imports the `write_weekly_report` function from `weekly_report_server.py` and calls it with the report content.

### Method 2: MCP Tool (Requires VSCode with Claude extension)

The system is also set up as an MCP server that can be used with the Claude extension in VSCode.

1. The MCP configuration is in `.fastmcp.toml` and `mcp.json`
2. The VSCode extension configuration is in:
   ```
   ~/Library/Application Support/Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json
   ```

When properly configured, you can use the `write_weekly_report` tool from the MCP server to create reports.

## Report Format

Reports are saved in the `reports` directory with filenames like `weekly_report_YYYYMMDD_HHMMSS.txt`.

The recommended format for reports is:

```
Weekly Report - [Date]

Accomplishments:
1. [Accomplishment 1]
2. [Accomplishment 2]
3. [Accomplishment 3]
4. [Accomplishment 4]

Next Steps:
1. [Next Step 1]
2. [Next Step 2]
3. [Next Step 3]
4. [Next Step 4]
```

## Files

- `weekly_report_server.py`: The main server file that defines the `write_weekly_report` function and sets up the MCP server
- `create_weekly_report.py`: A simple script that uses the `write_weekly_report` function to create a report
- `test_weekly_report.py`: A test script for the `write_weekly_report` function
- `reports/`: Directory where reports are saved
