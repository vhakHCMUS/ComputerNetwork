# Commands

## Screenshot
```
screenshot
```

## Keylogger
```bash
# The keylogger will run in 5 minutes by default
keylog
# Add argument -t (replace TIME with time to execute in second):
keylog -t TIME
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
```

To start/execute an app:
```bash
# in case you have the path to the app
app PATH_TO_APP
# in case the app name is available to this system
app APP_NAME
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