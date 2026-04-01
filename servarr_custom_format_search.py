#!/usr/bin/env python3
"""
This tool will scan your Servarr libraries for a specific custom format and output a list
"""
# Changelog
from __future__ import print_function
import os
import argparse
import json
import logging
import subprocess
import sys
import time
from pyarr import RadarrAPI
from pyarr import SonarrAPI


def process_radarr(args):
    """Process Radarr"""
    logging.info("Starting to process Radarr")
    send_mail = False
    radarr = RadarrAPI(args.radarr_host, args.radarr_apikey)
    movies_list = radarr.get_movie()
    movies_count = len(movies_list)
    logging.debug("Movie count is "+ str(movies_count))
    for movies_counter, movie in enumerate(movies_list):
        logging.debug("Working on " + movie['cleanTitle'] + " :: movie " + str(movies_counter + 1) + " of " + str(movies_count))
        if 'movieFile' in movie:
            if 'id' in movie['movieFile']:
                movie_file_data = radarr.get_movie_file(movie['movieFile']['id'])
                if 'customFormats' in movie_file_data:
                    for foobar, custom_format in enumerate(movie_file_data['customFormats']):
                        if args.custom_format in custom_format:
                            logging.warning(str(custom_format) + "    " + str(movie_file_data['path']))
                            send_mail = True
                        if args.custom_format in custom_format['name']:
                            logging.warning(str(custom_format['name']) + "    " + str(movie_file_data['path']))
                            send_mail = True
        logging.debug(json.dumps(movie, indent=4))
        #sys.exit()
    logging.info("Finished processing Radarr")
    return send_mail


def process_sonarr(args):
    """Process Sonarr"""
    logging.info("Starting to process Sonarr")
    send_mail = False
    sonarr = SonarrAPI(args.sonarr_host, args.sonarr_apikey)
    series_list = sonarr.get_series()
    series_count = len(series_list)
    for series_counter, series in enumerate(series_list):
        episode_list = sonarr.get_episode(series['id'], series=True)
        for episode_counter, episode in enumerate(episode_list):
            if 'episodeFileId' in episode:
                # episodeFileId can be zero for files not monitored and not downloaded
                if episode['episodeFileId'] != 0:
                    episode_file_data = sonarr.get_episode_file(episode['episodeFileId'])
                    if 'customFormats' in episode_file_data:
                        for foobar, custom_format in enumerate(episode_file_data['customFormats']):
                            if args.custom_format in custom_format:
                                logging.warning(str(custom_format) + "    " + str(episode_file_data['path']))
                                send_mail = True
                            if args.custom_format in custom_format['name']:
                                logging.warning(str(custom_format['name']) + "    " + str(episode_file_data['path']))
                                send_mail = True
    logging.info("Finished processing Sonarr")
    return send_mail


def check_positive(value):
    """Verify positive integer value"""
    try:
        ivalue = int(value)
        if ivalue <= 0:
            raise argparse.ArgumentTypeError("%s is an invalid positive int value" % value)
    except:
        raise argparse.ArgumentTypeError(f"Expected integer, got {value}")
    return ivalue



def main():
    """The true main function."""
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description='\033[1;33mProcess Servarr libraries and check for upgrades.\033[1;0m'
        )
    parser.add_argument('--radarr-host',          dest='radarr_host',                               default='http://127.0.0.1:7878/',         help='Set the Radarr host, default is "http://127.0.0.1:7878/"')
    parser.add_argument('--sonarr-host',          dest='sonarr_host',                               default='http://127.0.0.1:8989/',         help='Set the Sonarr host, default is "http://127.0.0.1:8989/"')
    parser.add_argument('--radarr-apikey',        dest='radarr_apikey',                             default=None,                             help='Set the Radarr API key, required for Radarr processing')
    parser.add_argument('--sonarr-apikey',        dest='sonarr_apikey',                             default=None,                             help='Set the Sonarr API key, required for Sonarr processing')
    parser.add_argument('--custom-format',        dest='custom_format',                             default='Upscaled',                       help='Set the custom format to search for, default is "Upscaled"')
    parser.add_argument('-e','--email',           dest='email',                                     default=None,                             help='Set the email address to send alerts to, using mailx')
    parser.add_argument('-l','--logfile',         dest='logfile',                                   default=None,                             help='Set the log file, leaving blank disables logging to file, if using email requires a logfile or will use /tmp/servarr.log')
    parser.add_argument('-q','--quiet',           dest='quiet',                action='store_true', default=False,                            help='Enable quiet output, hides the start and end messages')
    parser.add_argument('--debug',                dest='debug',                action='store_true', default=False,                            help='Enable debug output')
    args = parser.parse_args()
    cleanup_logfile = False
    if args.email and not args.logfile:
        cleanup_logfile = True
        args.logfile = '/tmp/servarr.log'
        if os.path.isfile(args.logfile):
            os.remove(args.logfile)
    if args.debug:
        if args.logfile:
            logging.basicConfig(level=logging.DEBUG, filename=args.logfile, format="[%(levelname)8s] %(message)s")
        else:
            logging.basicConfig(level=logging.DEBUG,                        format="[%(levelname)8s] %(message)s")
    elif args.quiet:
        if args.logfile:
            logging.basicConfig(level=logging.WARNING, filename=args.logfile, format="[%(levelname)8s] %(message)s")
        else:
            logging.basicConfig(level=logging.WARNING,                        format="[%(levelname)8s] %(message)s")
    else:
        if args.logfile:
            logging.basicConfig(level=logging.INFO,  filename=args.logfile, format="[%(levelname)8s] %(message)s")
        else:
            logging.basicConfig(level=logging.INFO,                         format="[%(levelname)8s] %(message)s")

    if args.radarr_apikey is None and args.sonarr_apikey is None:
        logging.error("No API keys not provided, exiting.")
        return 1
    send_mail_radarr = False
    send_mail_sonarr = False
    if args.radarr_apikey is not None:
        send_mail_radarr = process_radarr(args)
    if args.sonarr_apikey is not  None:
        send_mail_sonarr = process_sonarr(args)
    if (send_mail_radarr or send_mail_sonarr) and args.email:
        subprocess.run(["mailx -s \"Custom format " + args.custom_format + " found in servarr\" " + args.email + " < " + args.logfile], shell=True)
    if cleanup_logfile:
        os.remove(args.logfile)

    return 0


if __name__ == '__main__':
    main()

