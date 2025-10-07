import os
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

# load env
load_dotenv()
print("Loaded API key:", os.getenv("HF_API_KEY"))


client = InferenceClient(api_key=os.environ["HF_API_KEY"])

image = client.text_to_image(
    prompt="A couple in front of burj khalifa",
    model="black-forest-labs/FLUX.1-dev"
)

# Save the generated image
image.save("generated_image.png")