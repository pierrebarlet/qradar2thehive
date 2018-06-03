# Security-Tools
Tools for security teams.

# qradar2thehive
qradar2thehive python script was created to use TheHive as an incident response platform for the IBM QRadar SIEM.
I made it as simple as possible so that everyone could adapt it to their needs.
It requires a little configuration. All the details are described in the comments of the script.
Any improvement is welcome.
Many thanks to The Hive project team for their outstanding work: https://github.com/TheHive-Project
## Configuration
You need:
- TheHive API key
- QRadar API key
- A local file to save last QRadar Offense ID
- QRadar IP address
- [TheHive4py](https://thehive-project.org/#section_thehive4py)
- TheHive instance URL

Use cron to automate the execution of the script.

