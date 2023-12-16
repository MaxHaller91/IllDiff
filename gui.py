import tkinter as tk
from tkinter import messagebox
import main_gui
import threading

def submit():
    def run_task():
        seed = int(seed_var.get())
        image_url = image_url_var.get()
        width = int(width_var.get())
        height = int(height_var.get())
        prompt = prompt_var.get()
        num_outputs = int(num_outputs_var.get())
        guidance_scale = float(guidance_scale_var.get())
        negative_prompt = negative_prompt_var.get()
        qrcode_content = qrcode_content_var.get()
        qrcode_bg = qrcode_bg_var.get()
        num_inference_steps = int(num_inference_steps_var.get())
        controlnet_scale = float(controlnet_scale_var.get())

        try:
            output = main_gui.run_model(seed, image_url, width, height, prompt, num_outputs, guidance_scale, negative_prompt, qrcode_content, qrcode_bg, num_inference_steps, controlnet_scale)
            if isinstance(output, list):
                for url in output:
                    result = main_gui.download_image(url)
                    # Update GUI with result (this needs to be done in the main thread)
                    root.after(0, lambda: result_label.config(text=result))
        except Exception as e:
            # Show error message
            root.after(0, lambda: messagebox.showerror("Error", str(e)))

    # Run the task in a separate thread
    threading.Thread(target=run_task).start()

root = tk.Tk()
root.title("Image Generation with Replicate")

# Variables with default values
seed_var = tk.StringVar(value="-1")
image_url_var = tk.StringVar(value="https://i.imgur.com/FDyeug6.png")
width_var = tk.StringVar(value="500")
height_var = tk.StringVar(value="500")
prompt_var = tk.StringVar(value="Medieval painting")
num_outputs_var = tk.StringVar(value="3")
guidance_scale_var = tk.StringVar(value="7.5")
negative_prompt_var = tk.StringVar(value="low quality,deformed faces, blurry")
qrcode_content_var = tk.StringVar(value="")
qrcode_bg_var = tk.StringVar(value="gray")
num_inference_steps_var = tk.StringVar(value="40")
controlnet_scale_var = tk.StringVar(value="1.3")

# Entry widgets with default values
tk.Label(root, text="Seed:").pack()
seed_entry = tk.Entry(root, textvariable=seed_var)
seed_entry.pack()

tk.Label(root, text="Image URL:").pack()
image_url_entry = tk.Entry(root, textvariable=image_url_var)
image_url_entry.pack()

tk.Label(root, text="Width:").pack()
width_entry = tk.Entry(root, textvariable=width_var)
width_entry.pack()

tk.Label(root, text="Height:").pack()
height_entry = tk.Entry(root, textvariable=height_var)
height_entry.pack()

tk.Label(root, text="Prompt:").pack()
prompt_entry = tk.Entry(root, textvariable=prompt_var)
prompt_entry.pack()

tk.Label(root, text="Number of Outputs:").pack()
num_outputs_entry = tk.Entry(root, textvariable=num_outputs_var)
num_outputs_entry.pack()

tk.Label(root, text="Guidance Scale:").pack()
guidance_scale_entry = tk.Entry(root, textvariable=guidance_scale_var)
guidance_scale_entry.pack()

tk.Label(root, text="Negative Prompt:").pack()
negative_prompt_entry = tk.Entry(root, textvariable=negative_prompt_var)
negative_prompt_entry.pack()

tk.Label(root, text="QR Code Content:").pack()
qrcode_content_entry = tk.Entry(root, textvariable=qrcode_content_var)
qrcode_content_entry.pack()

tk.Label(root, text="QR Code Background:").pack()
qrcode_bg_entry = tk.Entry(root, textvariable=qrcode_bg_var)
qrcode_bg_entry.pack()

tk.Label(root, text="Number of Inference Steps:").pack()
num_inference_steps_entry = tk.Entry(root, textvariable=num_inference_steps_var)
num_inference_steps_entry.pack()

tk.Label(root, text="ControlNet Conditioning Scale:").pack()
controlnet_scale_entry = tk.Entry(root, textvariable=controlnet_scale_var)
controlnet_scale_entry.pack()

submit_button = tk.Button(root, text="Submit", command=submit)
submit_button.pack()

result_label = tk.Label(root, text="")
result_label.pack()

root.mainloop()
