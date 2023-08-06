# -*- coding: utf-8 -*-

from flask import (
    Flask,
    redirect,
    render_template,
    request,
    jsonify,
)
from werkzeug.wrappers import Response
from tuxput.filters import datetimeformat, file_name, folder_name
from tuxput.resources import s3_server
from tuxput.config import TuxConfig
from fnmatch import fnmatch

__version__ = "0.0.2"


def create_app():
    app = Flask(__name__, instance_relative_config=True, static_folder="static")

    config = TuxConfig()
    print("Setting s3_handler to {0}".format(config.S3_BUCKET))
    s3_handler = s3_server(bucket=config.S3_BUCKET, region=config.S3_REGION)

    print("Setting auth_handler to {0}".format(config.AUTH_BUCKET))
    auth_handler = s3_server(bucket=config.AUTH_BUCKET, region=config.S3_REGION)

    # checks that the token exists in our passwd file.  If not, we return None
    def get_authorizations(token):
        authorizations = auth_handler.select_from_object(config.AUTH_FILE, token)
        return authorizations

    def check_authorizations(url, authorizations):
        # be aware that there could be multiple entries for the same token
        # but with different path patterns, so the select could return multiple
        # results.  Let's set this up so we will search through all of them
        # and return true on the first successful match.
        for x in authorizations:
            if fnmatch(url, x):
                return True

        # still here?  Then it's a fail
        return False

    @app.context_processor
    def add_site_name():
        return {"SITE_TITLE": config.SITE_TITLE}

    @app.context_processor
    def add_app_version():
        return {"VERSION": __version__}

    @app.route("/upload/<path:path>", methods=["POST"])
    def upload(path=""):
        """ Attempt to upload an object. """
        token = request.headers.get("X-tuxput-token")

        print("path set to {0}".format(path))

        print("Checking for auths on token: {0}".format(token))
        authorizations = get_authorizations(token)
        # if token is not valid, return a 401
        if len(authorizations) < 1:
            return "Forbidden: token not found\n", 401 

        if not check_authorizations(path, authorizations):
            return (
                "Forbidden: token does not have authorization to write to {0}\n".format(
                    path
                ),
                403,
            )

        if path == "" or path == "/":
            return "Forbidden: you must specify a key to upload the object", 403

        real_path = config.S3_PATH(path)
        print("real_path set to {0}".format(real_path))

        # If the url is to a specific object, serve it.
        if s3_handler.key_exists(real_path):
            if not config.ALLOW_UPLOAD_OVERWRITE:
                return "Conflict: the key '{0}' already exists".format(path), 409

            # sneaky pete tried to overwrite the passwd file.. reuse previous
            # error so we don't confirm this the auth file
            if real_path is config.AUTH_FILE:
                return "Conflict: the key '{0}' already exists".format(path), 409

        return s3_handler.create_signed_url(real_path)

    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def default_get(path):
        return "Request refused, this site is for upload only\n", 200

    return app
