import {
  BedrockRuntimeClient,
  InvokeModelWithResponseStreamCommand,
} from "@aws-sdk/client-bedrock-runtime";

// Bedrock runtime 생성
const modelId = "anthropic.claude-3-haiku-20240307-v1:0";
const bedrockRuntime = new BedrockRuntimeClient({ region: "us-east-1" });

const invokeModelWithResponseStream = async (prompt, responseStream) => {
  const body = {
    anthropic_version: "bedrock-2023-05-31",
    max_tokens: 1000,
    messages: [
      {
        role: "user",
        content: [{ type: "text", text: prompt }],
      },
    ],
  };

  // Stream Response 호출을 위한 명령어 생성
  const command = new InvokeModelWithResponseStreamCommand({
    contentType: "application/json",
    body: JSON.stringify(body),
    modelId: modelId,
  });
  // 명령어 전송을 통해 FM 호출
  const apiResponse = await bedrockRuntime.send(command);

  let completeMessage = "";
  // Decode and process the response stream
  for await (const item of apiResponse.body) {
    const chunk = JSON.parse(new TextDecoder().decode(item.chunk.bytes));
    const chunk_type = chunk.type;

    if (chunk_type === "content_block_delta") {
      const text = chunk.delta.text;
      completeMessage = completeMessage + text;
      responseStream.write(text);
      console.log(text);
    }
  }

  // Return the final response
  return completeMessage;
};

export const handler = awslambda.streamifyResponse(
  async (event, responseStream, context) => {
    console.log(`event: ${JSON.stringify(event)}`);

    const { method, path } = event.requestContext.http;
    if (method === "POST" && path === "/") {
      const body = JSON.parse(event.body);
      const prompt = body.prompt;
      console.log(">>>>>>>>>>>> prompt: ", prompt);
      responseStream.setContentType("text/plain");
      await invokeModelWithResponseStream(prompt, responseStream);
      responseStream.end();
    } else {
      responseStream.end();
    }
  }
);
