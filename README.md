# Weekly Report System

The Weekly Report System is designed to facilitate the creation and management of weekly reports, which are stored in the `reports` directory with timestamps for easy tracking.

## Setup

To get started with the Weekly Report System, follow these steps:

1. **Install Dependencies:**
   Ensure you have all the necessary Python packages by running:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the MCP Server:**
   Start the MCP server to enable report creation:
   ```bash
   python weekly_report_server.py
   ```

## Usage

The system offers two methods for creating weekly reports:

### Method 1: Direct Python Script

Create a weekly report by executing the `create_weekly_report.py` script:
```bash
python create_weekly_report.py
```
This script utilizes the `write_weekly_report` function from `weekly_report_server.py` to generate the report content.

### Method 2: MCP Tool (Requires VSCode with Claude Extension)

Leverage the MCP server functionality with the Claude extension in VSCode:

1. **MCP Configuration:**
   Ensure the MCP settings are correctly configured in `.fastmcp.toml` and `mcp.json`.

2. **VSCode Extension Configuration:**
   Verify the extension settings in:
   ```
   ~/Library/Application Support/Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json
   ```

Once configured, use the `write_weekly_report` tool from the MCP server to create reports directly within VSCode.

## Report Format

Reports are stored in the `reports` directory with filenames formatted as `weekly_report_YYYYMMDD_HHMMSS.txt`.

The recommended structure for reports is as follows:

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

## Project Files

- **`weekly_report_server.py`:** The core server file that defines the `write_weekly_report` function and sets up the MCP server.
- **`create_weekly_report.py`:** A script that calls the `write_weekly_report` function to generate a report.
- **`test_weekly_report.py`:** A testing script for validating the `write_weekly_report` function.
- **`reports/`:** The directory where all generated reports are saved.

## Additional Information

For further assistance or inquiries, please refer to the project's documentation or contact the development team.
