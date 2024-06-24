import tkinter as tk
from tkinter import filedialog
from PIL import Image
import os

def check_input_directory(input_directory):
    if not os.path.exists(input_directory):
        return False, "Error: Input directory does not exist."
    
    if not os.listdir(input_directory):
        return False, "Directory is empty!"

    return True, ""

def create_output_directory(output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

def find_png_files(input_directory):
    png_files = [f for f in os.listdir(input_directory) if f.lower().endswith('.png')]
    return png_files

def compress_image(input_path, output_path, quality=85):
    try:
        img = Image.open(input_path)
        img = img.convert('P', palette=Image.ADAPTIVE, colors=256)
        img.save(output_path, optimize=True, quality=quality)
        return True, f"Compressed {input_path} to {output_path}"
    except Exception as e:
        return False, f"Error compressing {input_path}: {e}"

def update_log(text):
    log_text.set(text)

def browse_input_directory():
    input_directory = filedialog.askdirectory()
    input_entry.delete(0, tk.END)
    input_entry.insert(0, input_directory)

def browse_output_directory():
    output_directory = filedialog.askdirectory()
    output_entry.delete(0, tk.END)
    output_entry.insert(0, output_directory)

def start_compression():
    input_directory = input_entry.get()
    output_directory = output_entry.get()
    quality = quality_slider.get()

    valid_input, error_message = check_input_directory(input_directory)
    if not valid_input:
        update_log(error_message)
        return
    
    create_output_directory(output_directory)
    
    png_files = find_png_files(input_directory)
    if not png_files:
        update_log("No PNG files found in the input directory.")
        return
    
    for png_file in png_files:
        input_path = os.path.join(input_directory, png_file)
        output_path = os.path.join(output_directory, png_file)
        success, message = compress_image(input_path, output_path, quality)
        if success:
            update_log(message)
        else:
            update_log(message)

# Create main window
root = tk.Tk()
root.title("PNG Image Compressor")

# Input directory
input_label = tk.Label(root, text="Input Directory:")
input_label.grid(row=0, column=0, padx=10, pady=5)
input_entry = tk.Entry(root, width=50)
input_entry.grid(row=0, column=1, padx=10, pady=5)
input_button = tk.Button(root, text="Browse", command=browse_input_directory)
input_button.grid(row=0, column=2, padx=5, pady=5)

# Output directory
output_label = tk.Label(root, text="Output Directory:")
output_label.grid(row=1, column=0, padx=10, pady=5)
output_entry = tk.Entry(root, width=50)
output_entry.grid(row=1, column=1, padx=10, pady=5)
output_button = tk.Button(root, text="Browse", command=browse_output_directory)
output_button.grid(row=1, column=2, padx=5, pady=5)

# Quality slider
quality_label = tk.Label(root, text="Quality:")
quality_label.grid(row=2, column=0, padx=10, pady=5)
quality_slider = tk.Scale(root, from_=1, to=100, orient=tk.HORIZONTAL)
quality_slider.set(85)
quality_slider.grid(row=2, column=1, padx=10, pady=5)

# Compress button
compress_button = tk.Button(root, text="Compress", command=start_compression)
compress_button.grid(row=3, column=1, padx=10, pady=10)

# Log
log_text = tk.StringVar()
log_label = tk.Label(root, textvariable=log_text)
log_label.grid(row=4, column=0, columnspan=3, padx=10, pady=5)

root.mainloop()
