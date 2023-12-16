import replicate
import os
os.environ['REPLICATE_API_TOKEN'] = "r8_PUZ2vkr3yTDfVhAqeecyUr4h0RXK3Dh2MmyrG"

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
    "negative_prompt": "low quality,deformed faces, blurry",
    "qr_code_content": "",
    "qrcode_background": "gray",
    "num_inference_steps": 40,
    "controlnet_conditioning_scale": 1.3
  }
)
print(output)
