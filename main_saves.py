import replicate
import requests
import os

# Set your API token
os.environ['REPLICATE_API_TOKEN'] = "r8_PUZ2vkr3yTDfVhAqeecyUr4h0RXK3Dh2MmyrG"

# Function to download and save images
def download_image(url, folder="downloaded_images"):
    # Create folder if it doesn't exist
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Extract image name from URL
    image_name = url.split("/")[-1]

    # Full path for image
    path = os.path.join(folder, image_name)

    # Download and save the image
    response = requests.get(url)
    if response.status_code == 200:
        with open(path, 'wb') as f:
            f.write(response.content)
        print(f"Image saved: {path}")
    else:
        print(f"Failed to download image from {url}")

# Run the Replicate model
output = replicate.run(
  "lucataco/illusion-diffusion-hq:3c64e669051f9b358e748c8e2fb8a06e64122a9ece762ef133252e2c99da77c1",
  input={
    "seed": -1,
    "image": "https://i.imgur.com/FDyeug6.png",  # Your image URL
    "width": 500,
    "border": 1,
    "height": 500,
    "prompt": "Medieval painting",
    "num_outputs": 3,
    "guidance_scale": 7.5,
    "negative_prompt": "bad anatomy, low quality,deformed faces, blurry",
    "qr_code_content": "",
    "qrcode_background": "gray",
    "num_inference_steps": 40,
    "controlnet_conditioning_scale": 1.3
  }
)

# Check if the output is a list of URLs
if isinstance(output, list):
    # Download each image from the list
    for url in output:
        download_image(url)
else:
    print("No images were generated or the output format is not as expected.")
