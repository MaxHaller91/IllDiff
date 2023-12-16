import tkinter as tk
from tkinter import messagebox
import main_gui
import threading
from PIL import Image, ImageTk
from tkinter import Canvas, Frame, Scrollbar
from main_gui import time



# Constants for grid layout
MAX_COLUMNS = 3  # Set the maximum number of images per row
image_counter = 0  # To keep track of the number of images added


def submit():
    def run_task():
        seed = int(seed_var.get())
        image_url = image_url_var.get()
        width = int(width_var.get())
        height = int(height_var.get())
        prompt = prompt_var.get()
        guidance_scale = float(guidance_scale_var.get())
        negative_prompt = negative_prompt_var.get()
        qrcode_content = qrcode_content_var.get()
        qrcode_bg = qrcode_bg_var.get()
        num_inference_steps = int(num_inference_steps_var.get())
        controlnet_scale = float(controlnet_scale_var.get())

        # Check if batch processing is enabled
        if batch_processing_var.get():
            total_images = int(total_images_var.get())
            calls_needed = (total_images + 3) // 4

            for _ in range(calls_needed):
                try:
                    current_output = min(4, total_images)  # Adjust number of outputs per call
                    total_images -= current_output

                    output = main_gui.run_model(seed, image_url, width, height, prompt, current_output, guidance_scale, negative_prompt, qrcode_content, qrcode_bg, num_inference_steps, controlnet_scale)
                    if isinstance(output, list):
                        for url in output:
                            image_path = main_gui.download_image(url)
                            root.after(0, lambda path=image_path: display_image(path))

                    if total_images <= 0:
                        break  # Exit the loop if all images are processed

                    time.sleep(2)  # Wait 2 seconds before the next call

                except Exception as e:
                    root.after(0, lambda e=e: messagebox.showerror("Error", str(e)))

        else:
            # Single call with specified number of outputs
            try:
                num_outputs = int(num_outputs_var.get())
                output = main_gui.run_model(seed, image_url, width, height, prompt, num_outputs, guidance_scale, negative_prompt, qrcode_content, qrcode_bg, num_inference_steps, controlnet_scale)
                if isinstance(output, list):
                    for url in output:
                        image_path = main_gui.download_image(url)
                        root.after(0, lambda path=image_path: display_image(path))

            except Exception as e:
                root.after(0, lambda e=e: messagebox.showerror("Error", str(e)))

    threading.Thread(target=run_task).start()





    def display_image(image_path):
        # Use the global keyword to indicate that you want to use the global image_counter
        global image_counter

        # Load the image
        img = Image.open(image_path)
        img.thumbnail((100, 100))  # Resize the image
        img = ImageTk.PhotoImage(img)

        # Calculate the grid position
        row = image_counter // MAX_COLUMNS
        column = image_counter % MAX_COLUMNS

        # Create a label and add the image to the image_container grid
        label = tk.Label(image_container, image=img)
        label.image = img  # Keep a reference
        label.grid(row=row, column=column, padx=5, pady=5)

        # Increment the counter for the next image
        image_counter += 1

        # Update the scrollregion of the canvas after adding the image
        onFrameConfigure(canvas)


root = tk.Tk()
root.title("Image Generation with Replicate")

# Global variable to track if batch processing is enabled
batch_processing_var = tk.BooleanVar(value=False)

# Create frames for input and output
input_frame = Frame(root, bg='red')
output_frame = Frame(root)  # No need for bg color here, as it should be covered by the canvas

input_frame.pack(side=tk.LEFT, fill=tk.Y, expand=False)
output_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# Create the canvas with scrollbars inside the output frame
canvas = Canvas(output_frame)
v_scroll = Scrollbar(output_frame, orient="vertical", command=canvas.yview)
v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
canvas.configure(yscrollcommand=v_scroll.set)

canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# This frame will hold the images inside the canvas
image_container = Frame(canvas)

# Add the image container to the canvas
canvas.create_window((0, 0), window=image_container, anchor="nw")

# Add input widgets to the input_frame...

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

# Add a checkbox to the GUI
batch_processing_check = tk.Checkbutton(root, text="Enable Batch Processing", variable=batch_processing_var)
batch_processing_check.pack()

total_images_var = tk.StringVar(value="4")  # Default to 4 images
tk.Label(root, text="Total Images:").pack()
total_images_entry = tk.Entry(root, textvariable=total_images_var)
total_images_entry.pack()

submit_button = tk.Button(root, text="Submit", command=submit)
submit_button.pack()

result_label = tk.Label(root, text="")
result_label.pack()
def onFrameConfigure(_):
    """Update the scrollregion to encompass the inner frame"""
    canvas.configure(scrollregion=canvas.bbox("all"))
    canvas.update_idletasks()  # Update the canvas immediately

image_container.bind("<Configure>", lambda event: onFrameConfigure(None))
root.mainloop()
