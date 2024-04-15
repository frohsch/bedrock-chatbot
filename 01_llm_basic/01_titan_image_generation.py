import base64
import json
import os
import random

import boto3

bedrock_runtime = boto3.client(service_name="bedrock-runtime", region_name="us-east-1")


def save_image(base64_image_data, prompt):
    # 이미지 저장 폴더 생성
    output_folder = "images"
    os.makedirs(output_folder, exist_ok=True)

    # 이미지 파일 경로 생성
    file_path = os.path.join(output_folder, f"{prompt}.png")
    # base64 인코딩된 데이터를 이미지 파일로 변환하여 저장
    with open(file_path, "wb") as file:
        file.write(base64.b64decode(base64_image_data))
    # 이미지 저장 경로를 로깅함
    return file_path


def edit_image(image_path, prompt):
    with open(image_path, "rb") as image_file:
        input_image = base64.b64encode(image_file.read()).decode("utf8")

    body = json.dumps(
        {
            "taskType": "IMAGE_VARIATION",
            "imageVariationParams": {"text": prompt, "images": [input_image]},
        }
    )

    try:
        # 모델을 호출해 이미지 생성
        response = bedrock_runtime.invoke_model(
            body=body,
            modelId="amazon.titan-image-generator-v1",
        )

        # base64 인코딩된 이미지 데이터 추출
        base64_image_data = json.loads(response["body"].read())["images"][0]
        return save_image(base64_image_data, prompt)
    except Exception as e:
        print(f"이미지 생성 중 오류 발생: {e}")
        raise


def generate_image(prompt):
    # 이미지 생성을 위한 난수 시드를 생성
    seed = random.randint(0, 2147483647)
    # 이미지 생성 요청 데이터를 구성함
    body = json.dumps(
        {
            "taskType": "TEXT_IMAGE",
            "textToImageParams": {"text": prompt},
            "imageGenerationConfig": {
                "numberOfImages": 1,
                "quality": "standard",
                "cfgScale": 7.5,
                "height": 512,
                "width": 512,
                "seed": seed,
            },
        }
    )
    try:
        # 모델을 호출해 이미지 생성
        response = bedrock_runtime.invoke_model(
            body=body,
            modelId="amazon.titan-image-generator-v1",
        )

        # base64 인코딩된 이미지 데이터 추출
        base64_image_data = json.loads(response["body"].read())["images"][0]
        return save_image(base64_image_data, prompt)
    except Exception as e:
        print(f"이미지 생성 중 오류 발생: {e}")
        raise


def main():
    # 이미지 생성을 위한 텍스트 프롬프트 설정
    prompt = [
        "Golden Retriever",
        "Golden Retriever as a cartoon",
        "Golden Retriever as a sketch",
        "Golden Retriever scuba diving in the deep sea wearing a mask and flippers",
    ]
    # 이미지를 생성하고 저장
    image_path = generate_image(prompt[0])
    print(f"생성된 이미지 경로: {image_path}")

    # output_folder = 'images'
    # target_image = 'Golden Retriever'
    # file_path = os.path.join(output_folder, f"{target_image}.png")
    # image_path = edit_image(file_path, "Golden Retriever in a play ground")
    # print(f"수정된 이미지 경로: {image_path}")


if __name__ == "__main__":
    main()
