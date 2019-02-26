# qradar2thehive
qradar2thehive python script was created to use TheHive as an incident response platform for the IBM QRadar SIEM.
I made it as simple as possible so that everyone could adapt it to their needs.
It requires a little configuration. All the details are described in the comments of the script.
Any improvement is welcome.
Many thanks to The Hive project team for their outstanding work: https://github.com/TheHive-Project
## Configuration
You need:
- [TheHive4py](https://thehive-project.org/#section_thehive4py)
- TheHive API key
- QRadar API key
- TheHive instance URL
- QRadar IP address
- A local file to save last QRadar Offense ID
- Create custom fields on TheHive with the same internal reference and the same type as the script

Use cron to automate the execution of the script.

# multi_cases_updator
A little script to update a large number of cases.
You have to configure the range of cases id you want to update and of course the attributes you want to modifiy.
I use the script to close a large number of cases when i have false positive from QRadar.
If you want to update a small number of cases you can get samples from TheHive-Project [here](https://github.com/TheHive-Project/TheHive4py/tree/master/samples).
