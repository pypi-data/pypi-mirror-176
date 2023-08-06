# -*- coding: utf-8 -*-

import boto3
import botocore.exceptions
import json


class s3_server:
    def __init__(self, bucket, region):
        self.bucket = bucket
        self.region = region
        self.client = boto3.client("s3", region_name=region)

    def key_exists(self, key):
        """Try to fetch the metadata for an object. If the object does not
        exist, head_object will raise an exception. Returns True if the
        object exists
        """
        try:
            head = self.client.head_object(Bucket=self.bucket, Key=key)
            if head.get("ContentLength") == 0:
                # Disregard empty objects
                return False
        except (
            botocore.exceptions.ParamValidationError,
            botocore.exceptions.ClientError,
        ):
            return False
        return True

    def create_signed_url(self, key):
        return self.client.generate_presigned_post(self.bucket, key, ExpiresIn=90)

    def select_from_object(self, authfile, token):
        print("Checking in {0} for token {1}".format(authfile, token))

        if not self.key_exists(authfile):
            print("ERROR: authfile doesn't exist!!")

        authorizations = []

        response = self.client.select_object_content(
            Bucket=self.bucket,
            Key=authfile,
            ExpressionType="SQL",
            Expression=
            """SELECT path from S3Object s where token = '{0}'""".format(token),
            InputSerialization={
                "CompressionType": "NONE",
                "CSV": {
                    "FileHeaderInfo": 'USE',
                    "RecordDelimiter": '\n',
                    "FieldDelimiter": ',',
                },
            },
            OutputSerialization={ "JSON": {} }
        )

        for event in response["Payload"]:
            print(str(event))
            if 'Records' in event:
                result = json.loads(event['Records']['Payload'].decode('utf-8'))
                authorizations.append(result['path'])

        return authorizations
