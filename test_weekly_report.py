from weekly_report_server import write_weekly_report

# Test content
content = """Weekly Report - March 30, 2024

Accomplishments:
1. Set up MCP server
2. Created weekly report functionality
3. Tested file writing capabilities

Next Steps:
1. Add more features
2. Improve error handling
3. Add user authentication"""

# Call the function
result = write_weekly_report(content)
print("Result:", result) 