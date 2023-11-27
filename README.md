# Commands

## Screenshot
```
screenshot
```

## Keylogger
```bash
# the keylogger will run in 5 minutes by default
keylog
# add argument -t (replace TIME with time to execute in second) to execute for custom time:
keylog -t TIME
# add argument -l to receive typed text on the server instead of list of keys
keylog -l
# add argument -both to receive both the list of keys and the text
keylog -both
# example
keylog -t 500 -both
```

## Application interaction
To list apps on computer:
```bash
# list running apps
app list
# add argument -all to list all apps (available to the server, both running and not running)
app list -all
# add argument -path to list the path to the app
app list -path
# Using both
app list -all -path
```

To start/execute an app:
```bash
# in case you have the path to the app
app -open PATH_TO_APP
# in case the app name is available to this system
app -open APP_NAME
```

To end/stop a running app:
```bash
app -end APP_NAME
```

## Process interactions
To list running processes:
```bash
proc list
```
To end/stop a running proccess:
```bash
proc -end PROCESS_NAME
```

## Power options
To shutdown the server:
```
shutdown
```

To restart the server:
```
restart
```

To logout the server:
```
logout
```