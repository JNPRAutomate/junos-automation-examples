The Config Consistency Checker is a simple python script that detects differences between Junos config files located in a given directory (in “set notation”).  The output of the script lists any line of config that exists in one config file and doesn’t exist in another, and includes the frequency of how often that line appeared in all the other files.  You can specify a minimum threshold such that the output will only list lines of config missing in a given router that occurred at least that percentage of other routers.  For example, a threshold of 90 means the output will only contain missing config lines that appeared in at least 90% of the other routers.  You can also specify config hierarchies that the script should ignore.

For best results, use this script to compare only routers of the same role (eg, core only, edge only, peering only).  Mixing different router roles in the same directory will likely lead to many false positives, as it is usually expected to have significant differences between routers in the different roles.

Usage:

> python config_parser.py input-directory outputfile

The goal of this project is to determine the extent to which config inconsistencies and drift occur in real networks, and how best to detect such anomalies with minimal false positives.  As such, we’d love to know what issues you find, how useful this script is, and any ideas for further enhancement.  Please send this feedback to lenny@juniper.net.
