# servarr_custom_format_search
Search and list out all Sonarr and/or Radarr files that have a specified custom format with optional email alerts.

Useful for finding every file that has a custom format you want to replace, like 'Upscaled'.

## Dependencies
[Pyarr](https://github.com/totaldebug/pyarr)


## Example Usage
```
# List out offenders in terminal
./servarr_list_upscaled.py --radarr-apikey 12345678901234567890123456789012 --sonarr-apikey abcdefghijklmnopqrstuvwxyzabcdef
# Email list of offenders
./servarr_list_upscaled.py --custom-format "x265 (HD)" --radarr-apikey 12345678901234567890123456789012 --sonarr-apikey abcdefghijklmnopqrstuvwxyzabcdef -q -e example@example.com
```

## Usage
```
./servarr_custom_format_search.py -h
usage: servarr_custom_format_search.py [-h] [--radarr-host RADARR_HOST] [--sonarr-host SONARR_HOST]
                                       [--radarr-apikey RADARR_APIKEY] [--sonarr-apikey SONARR_APIKEY]
                                       [--custom-format CUSTOM_FORMAT] [-e EMAIL] [-l LOGFILE] [-q] [--debug]

Process Servarr libraries and check for upgrades.

options:
  -h, --help            show this help message and exit
  --radarr-host RADARR_HOST
                        Set the Radarr host, default is "http://127.0.0.1:7878/"
  --sonarr-host SONARR_HOST
                        Set the Sonarr host, default is "http://127.0.0.1:8989/"
  --radarr-apikey RADARR_APIKEY
                        Set the Radarr API key, required for Radarr processing
  --sonarr-apikey SONARR_APIKEY
                        Set the Sonarr API key, required for Sonarr processing
  --custom-format CUSTOM_FORMAT
                        Set the custom format to search for, default is "Upscaled"
  -e EMAIL, --email EMAIL
                        Set the email address to send alerts to, using mailx
  -l LOGFILE, --logfile LOGFILE
                        Set the log file, leaving blank disables logging to file, if using email requires a
                        logfile or will use /tmp/servarr.log
  -q, --quiet           Enable quiet output, hides the start and end messages
  --debug               Enable debug output
```

## Testing
Tested on
- Ubuntu 24.04 LTS
- Python 3.12
- Sonarr 4.0.17
- Radarr 6.0.4
- Pyarr 5.2.0
 
## Contributing
Posting this on Github to share with the community as I have seen forum posts asking for this functionality. I do not intend to add Lidarr or Readarr functionality but will gladly accept PRs.
