import json
import ast
import os
from datetime import datetime as dt
import boto3
import sagemaker
from sagemaker.model_monitor import DefaultModelMonitor
from sagemaker.model_monitor.dataset_format import DatasetFormat


def handler(event, context):
    """
    Parameters
    ----------
    event: dict, required

    context: object, required

    Returns
    ------
    """

    print('Request info:', event)

    # Receive data from prodecure and parse it
    if 's3uri' in event and 'outpath' in event:
        s3uri = event['s3uri']
        outpath = event['outpath']
    else:
        raise Exception('Invoke-Model-Monitor requires s3uri and outpath!!')

    if 'instance_count' in event:
        instance_count = event['instance_count']
    else:
        instance_count = 1

    sagemaker_role = os.environ['sg_role_arn']
    print(sagemaker_role)

    print('point 1')
    default_monitor = DefaultModelMonitor(
        role=sagemaker_role,
        instance_count=instance_count,
        instance_type='ml.m5.xlarge',
        volume_size_in_gb=20,
        max_runtime_in_seconds=3600,
    )

    print('point 2')
    response = default_monitor.suggest_baseline(
        baseline_dataset=s3uri,
        dataset_format=DatasetFormat.csv(header=True),
        output_s3_uri=outpath,
        wait=False,
        logs=False,
    )

    print('point 3')

    # Finish
    return {
        "status": 200,
        "body": "body"
    }