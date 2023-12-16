import replicate
import requests
import os
import time
os.environ['REPLICATE_API_TOKEN'] = "r8_PUZ2vkr3yTDfVhAqeecyUr4h0RXK3Dh2MmyrG"

def download_image(url, folder="downloaded_images"):
    if not os.path.exists(folder):
        os.makedirs(folder)
    timestamp = int(time.time())
    image_name = f"{timestamp}_{url.split('/')[-1]}"
    path = os.path.join(folder, image_name)
    response = requests.get(url)
    if response.status_code == 200:
        with open(path, 'wb') as f:
            f.write(response.content)
    return path  # Return the path directly


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
