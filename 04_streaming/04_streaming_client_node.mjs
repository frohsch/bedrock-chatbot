import axios from "axios";

const API_ENDPOINT = "YOUR LAMBDA FUNCTION";
const body = { prompt: "대한민국의 수도에 대해 node설명해" };

async function postData() {
  try {
    const response = await axios.post(API_ENDPOINT, body, {
      responseType: "stream",
    });

    response.data.on("data", (chunk) => {
      // logic to process stream data
      process.stdout.write(chunk.toString());
    });

    response.data.on("end", () => {
      console.log("\n\n");
      console.log("Job Done!");
    });
  } catch (error) {
    console.error(error);
  }
}

postData();
