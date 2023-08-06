#!/usr/bin/env python3

import click
import os
import requests
import sys
from time import sleep

from tpcli.exceptions import *

UPLOAD_QUEUE = []
FAILED = {}
RETRIES=1
WAITTIME=10


def good_response(code):
    if code in [200,204]:
        return True
    return False

def scan_for_files(target):
    myfiles = []

    if os.path.isdir(target):
        entries = os.walk(target)
        for e in entries:
            (dirname, subdirs, files) = e
            # all all files in this dir
            myfiles.extend([os.path.join(dirname, x) for x in files])
            # scan through the subdirs recursively
            for d in subdirs:
                myfiles.extend(scan_for_files(os.path.join(dirname, d)))
    elif os.path.isfile(target):
        myfiles.append(target)
    else:
        raise Exception("Unknown filetype included.. {0}... skipping".format(target))

    return myfiles


def get_presigned_url(url, token, upload_file):
    retries = RETRIES
    waittime = WAITTIME
    headers = {"X-tuxput-token": token}
    full_url = url + "/" + upload_file
    while( retries > 0):
        retries -= 1

        print("sending req to {0}/{1} -- attempt {2}/{3}".format(url, upload_file,retries, RETRIES))
        resp = requests.post(full_url, headers=headers)

        print("<- got response {0}".format(resp.status_code))

        # if successful, we can just duck out
        if good_response(resp.status_code):
            return resp

        # can't login, so.. bad token.  Let's bail.
        if resp.status_code == 401:
            print("Raising UnknownTokenError")
            raise UnknownTokenError
        # we don't have permission for this upload.
        elif resp.status_code == 403:
            print("Raising NoAuthorizationError")
            raise NoAuthorizationError
        # file already exists
        elif resp.status_code == 409:
            print("Raising FileConflictError")
            raise FileConflictError

        # Any other problem is most likely an internal server error
        # or a another transient problem... hang out for a second and
        # try it again
        print("Failed to upload {0} ({1})... will retry in {2}s".format(upload_file, resp.status_code, WAITTIME))
        retries -= 1
        sleep(WAITTIME)

    # If we get here, then we've failed all retries and still haven't been
    # successful.  Let's return the last response and let the caller figure it
    # out
    return resp


def do_s3_upload(presigned, upload_file):
    print("Inside do_s3_upload()...")
    files = {}
    files["file"] = (upload_file, open(upload_file, "rb"))
    pdata = presigned.json()

    resp = requests.post(pdata["url"], data=pdata["fields"], files=files)
    print("<- returned {0}".format(resp.status_code))
    return resp


@click.command()
@click.argument("url", nargs=1)
@click.argument("targets", nargs=-1)
@click.option("--dry-run", "-n", default=False)
@click.option("--token", "-t", required=True, type=str)
@click.option("--sign-only", "-s", default=False, is_flag=True)
def tuxput_cli(url, targets, dry_run, token, sign_only):

    if token is None:
        print("Error: no token specified")

    # collect the files we'll be uploading
    for t in targets:
        UPLOAD_QUEUE.extend(scan_for_files(t))

    for f in UPLOAD_QUEUE:
        print("-- {0}".format(f))
        if dry_run:
            continue

        presigned = None
        try:
            presigned = get_presigned_url(url, token, f)
            if not good_response(presigned.status_code):
                # server errors that the timeout/retry couldn't resolve.  Log
                # the fail and move on.
                FAILED[f] = "Failed to get presigned URL '{0}' with code {1}... skipping".format(f, presigned.status_code)
                continue
        except requests.exceptions.ConnectionError as e:
            # server's not there, so don't bother with the rest
            print("ERROR: Unable to contact server: {0}".format(e))
            sys.exit(1)
        except UnknownTokenError as e:
            # token is invalid, so no point trying to upload the others
            print("ERROR: invalid token")
            sys.exit(1)
        except FileConflictError as e:
            FAILED[f] = "ERROR: file '{0}' already exists".format(f)
            continue
        except NoAuthorizationError as e:
            # Not necessarily fatal.  Log the fail and move on.
            FAILED[f] = "No authorization to get presigned url for '{0}'".format(f)
            continue

        print("INFO: past presigned... prepping do_s3_upload")
            
        if sign_only:
            continue

        if presigned is not None:
            upload = do_s3_upload(presigned, f)
            if not good_response(upload.status_code):
                FAILED[f] = "Failed to upload to AWS: {0}: {1}".format(upload.status_code, upload.text)

        # Finally, let's review all the uploads and list out any failures
    for x in FAILED:
        print("{0} - {1}".format(x, FAILED[x]))

# TODO possibly in version 2.0?
# --tar/-T tar up files in targets list into one file and upload
# --zip/-Z zip up file in targets list into one file and upload
# --pre/-p pre-run command
# --post/-P post-run command
# --exclude/-x  exclude file or pattern from the targets list


if __name__ == "__main__":
    tuxput_cli(auto_envvar_prefix="TUXPUT_CLI")
