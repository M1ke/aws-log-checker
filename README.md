# AWS CloudWatch logger extended

The AWS logger is a useful tool to aggregate system logs in to cloudwatch.

It requires a configuration file to be written which targets specific directories or files and places them in to a log group.

Unfortunately if you want to aggregate multiple logs in the same directory, these will merge in to a single log stream. In many cases it would be more preferable to have a separate stream for each file, with the group representing a directory.

This script is designed to be run on a schedule where a set of log directories are specified in a CSV file along with directory specific settings. Each time it runs it checks the directories specified, and builds a list of files. If the list of files has changed the configuration file is rewritten and the logging service is restarted.

## Setup

Rename `awslogs.conf.sample` to `awslogs.conf` and add any settings you want as default (e.g. syslog).

Rename `list.csv.sample` to `list.csv` and add your own directories and related settings.