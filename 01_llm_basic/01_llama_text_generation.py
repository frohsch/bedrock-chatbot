import json

import boto3


def printJson(dataObj):
    print(json.dumps(dataObj, sort_keys=True, indent=4))


bedrock = boto3.client(service_name="bedrock", region_name="us-east-1")

bedrock_runtime = boto3.client(service_name="bedrock-runtime", region_name="us-east-1")
question = "What is the AWS Bedrock?"
body = json.dumps({"prompt": question})
response = bedrock_runtime.invoke_model(body=body, modelId="meta.llama2-13b-chat-v1")
response_body = json.loads(response.get("body").read())
print(response_body["generation"])

# llama 파라미터 시그니처
body = json.dumps(
    {
        "prompt": question,
        "temperature": 0.5,
        "top_p": 0.5,  # vs. topP in titan
        "max_gen_len": 512,
    }
)
