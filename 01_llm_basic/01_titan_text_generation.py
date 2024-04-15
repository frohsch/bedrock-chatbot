import json  # JSON 데이터를 다루기 위한 모듈을 임포트

import boto3  # AWS 서비스를 이용하기 위한 boto3 라이브러리 임포트


# JSON 데이터를 예쁘게 출력하는 함수
def printJson(dataObj):
    print(
        json.dumps(dataObj, sort_keys=True, indent=4)
    )  # JSON 객체를 정렬하여 들여쓰기를 포함해 출력


# boto3 사용을 위해서 access key id와 secret key가 필요
# bedrock = boto3.client(aws_access_key_id='INPUT YOUR KEY',
#                       aws_secret_access_key='INPUT YOUR KEY')
# Cloud9 EC2는 credential이 설정되어 있으므로 생략 가능

# AWS Bedrock 서비스 클라이언트 생성, 지정된 리전에서 Bedrock 서비스에 접근
bedrock = boto3.client(service_name="bedrock", region_name="us-east-1")

# 특정 파운데이션 모델에 대한 정보를 가져옴, 여기서는 'amazon.titan-tg1-large' 모델
titan = bedrock.get_foundation_model(modelIdentifier="amazon.titan-tg1-large")
# printJson(titan)

# 아래 코드로 모든 FM을 확인할 수 있음
# fms = bedrock.list_foundation_models()
# printJson(fms)


# Bedrock runtime
# boto3.client(service_name='bedrock'): bedrock에 대한 정보 조회를 위한 클라이언트
# Bedrock Runtime 서비스 클라이언트 생성, 모델 실행을 위해 사용
bedrock_runtime = boto3.client(service_name="bedrock-runtime", region_name="us-east-1")

# 질문을 모델에 입력으로 제공하기 위한 JSON 바디 생성
question = "What is the AWS Bedrock?"
body = json.dumps({"inputText": question})  # 질문 텍스트를 JSON 형식으로 인코딩

# 모델을 실행하여 질문에 대한 응답을 가져옴
response = bedrock_runtime.invoke_model(body=body, modelId="amazon.titan-tg1-large")

# 응답 바디에서 결과를 추출하고 JSON으로 파싱
response_body = json.loads(response.get("body").read())
print("default setting: ", response_body["results"][0]["outputText"])

# 세부 설정을 포함한 복잡한 JSON 바디 예시, 텍스트 생성 설정 포함
# 여기서는 온도(creativity control), topP(filtering parameter), 최대 토큰 수 등을 설정
question = "Tell me something about generative AI"
body = json.dumps(
    {
        "inputText": question,
        "textGenerationConfig": {
            "temperature": 0,
            "topP": 0.01,
            "maxTokenCount": 128,
        },
    }
)


# 설정된 파라미터를 사용하여 모델을 다시 실행하고 결과를 출력
response = bedrock_runtime.invoke_model(body=body, modelId="amazon.titan-tg1-large")
response_body = json.loads(response.get("body").read())
print("\n\nto be deterministic: ", response_body["results"][0]["outputText"])


body = json.dumps(
    {
        "inputText": question,
        "textGenerationConfig": {
            "temperature": 1,
            "topP": 1,
            "maxTokenCount": 128,
        },
    }
)

# 설정된 파라미터를 사용하여 모델을 다시 실행하고 결과를 출력
response = bedrock_runtime.invoke_model(body=body, modelId="amazon.titan-tg1-large")
response_body = json.loads(response.get("body").read())
print("\n\nto be random: ", response_body["results"][0]["outputText"])
