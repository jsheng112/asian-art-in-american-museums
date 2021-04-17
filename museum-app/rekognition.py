#Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#PDX-License-Identifier: MIT-0 (For details, see https://github.com/awsdocs/amazon-rekognition-developer-guide/blob/master/LICENSE-SAMPLECODE.)

import boto3
from urllib.request import urlopen 
import base64
def detect_labels(photo):
    tags = []
    conf = []
    try:
        client=boto3.client('rekognition',  aws_access_key_id = ACCESS_KEY, aws_secret_access_key = SECRET_KEY, region_name='us-east-1')
        response = client.detect_labels(Image={'Bytes': urlopen(photo).read()}, MaxLabels = 10)

        for label in response['Labels']:
            tags.append(label['Name'])
            conf.append(round(label['Confidence'], 2))
        return tags, conf
    except Exception as e:
        return tags, conf

def main():
    photo=''
    bucket=''
    label_count, tags =detect_labels(photo)


if __name__ == "__main__":
    main()
