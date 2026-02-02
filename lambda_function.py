import json
import boto3
import os

s3 = boto3.client("s3")
eks = boto3.client("eks")

def lambda_handler(event, context):
    # ---- Read CodePipeline artifact ----
    job = event["CodePipeline.job"]
    artifact = job["data"]["inputArtifacts"][0]
    location = artifact["location"]["s3Location"]

    bucket = location["bucketName"]
    key = location["objectKey"]

    obj = s3.get_object(Bucket=bucket, Key=key)
    data = json.loads(obj["Body"].read().decode("utf-8"))

    image_uri = data["imageUri"]
    print("Image URI:", image_uri)

    # ---- Discover EKS cluster ----
    cluster_name = os.environ["CLUSTER_NAME"]
    region = os.environ["CLUSTER_REGION"]

    cluster = eks.describe_cluster(name=cluster_name)["cluster"]

    print("EKS endpoint:", cluster["endpoint"])
    print("EKS status:", cluster["status"])

    ca_data = cluster["certificateAuthority"]["data"]
    print("CA data length:", len(ca_data))

    return {
        "statusCode": 200,
        "body": "EKS cluster discovery succeeded"
    }

