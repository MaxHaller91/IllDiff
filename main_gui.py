import replicate
import requests
import os
import time

api_token = os.getenv('REPLICATE_API_TOKEN')
if not api_token:
    raise ValueError("Please set the REPLICATE_API_TOKEN environment variable.")

def download_image(url, base_folder="downloaded_images"):
    # Create a unique folder name using the current timestamp
    folder_name = str(int(time.time()))
    folder_path = os.path.join(base_folder, folder_name)

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    image_name = url.split("/")[-1]
    image_path = os.path.join(folder_path, image_name)

    response = requests.get(url)
    if response.status_code == 200:
        with open(image_path, 'wb') as f:
            f.write(response.content)

    return image_path



def run_model(seed, image_url, width, height, prompt, num_outputs, guidance_scale, negative_prompt, qrcode_content, qrcode_bg, num_inference_steps, controlnet_scale):
    output = replicate.run(
        "lucataco/illusion-diffusion-hq:3c64e669051f9b358e748c8e2fb8a06e64122a9ece762ef133252e2c99da77c1",
        input={
            "seed": seed,
            "image": image_url,
            "width": width,
            "height": height,
            "prompt": prompt,
            "num_outputs": num_outputs,
            "guidance_scale": guidance_scale,
            "negative_prompt": negative_prompt,
            "qr_code_content": qrcode_content,
            "qrcode_background": qrcode_bg,
            "num_inference_steps": num_inference_steps,
            "controlnet_conditioning_scale": controlnet_scale
        }
    )
    return output
