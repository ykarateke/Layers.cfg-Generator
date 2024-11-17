import os
import random
import tkinter as tk
from tkinter import filedialog, messagebox

def generate_unique_color(existing_colors):
    """Generate a unique RGB color."""
    while True:
        color = tuple(random.randint(0, 255) for _ in range(3))  # Create as a tuple
        if color not in existing_colors:
            existing_colors.add(color)
            return color

def create_layers_cfg():
    folder_path = input_folder_var.get()

    if not folder_path:
        messagebox.showerror("Error", "Please select the folder containing .rvmat files!")
        return

    output_file_path = os.path.join(folder_path, "layers.cfg")

    # Find all .rvmat files in the folder
    rvmat_files = [f for f in os.listdir(folder_path) if f.endswith(".rvmat")]

    if not rvmat_files:
        messagebox.showerror("Error", "No .rvmat files found in the selected folder!")
        return

    layers_cfg_content = "class layers\n{\n"
    legend_content = ""

    # Set to keep track of existing colors
    existing_colors = set()

    for rvmat in rvmat_files:
        # Extract the class name from the file name
        class_name = os.path.splitext(rvmat)[0]

        # Generate a unique color
        rgb_color = generate_unique_color(existing_colors)

        # Remove drive letter
        full_path = os.path.join(folder_path, rvmat)
        _, rel_path = os.path.splitdrive(full_path)
        formatted_path = rel_path.lstrip("\\").replace("\\", "/")  # Format the path

        # Create layers content
        layers_cfg_content += f"""
    class {class_name} 
    {{
        texture="#(argb,8,8,3)color(0.5,0.5,0.5,1)";
        material="{formatted_path}";
    }};
"""

        # Create legend content
        legend_content += f"\t\t{class_name}[]={{{{{rgb_color[0]},{rgb_color[1]},{rgb_color[2]}}}}}; // Color RGB Code: {''.join([hex(c)[2:].zfill(2) for c in rgb_color])}\n"

    layers_cfg_content += "};\n"

    # Add picture path to the legend class
    legend_picture_path = os.path.join(folder_path, "legend.png")
    _, legend_rel_path = os.path.splitdrive(legend_picture_path)
    formatted_legend_path = legend_rel_path.lstrip("\\").replace("\\", "/")

    legend_content = f"""
class legend 
{{
    picture="{formatted_legend_path}";
    class colors 
    {{
{legend_content}
    }};
}};
"""

    # Combine layers.cfg content
    final_content = layers_cfg_content + legend_content

    # Save layers.cfg
    try:
        with open(output_file_path, "w", encoding="utf-8") as cfg_file:
            cfg_file.write(final_content)
        messagebox.showinfo("Success", f"layers.cfg file successfully created: {output_file_path}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while creating layers.cfg:\n{e}")

# Tkinter GUI
root = tk.Tk()
root.title("Layers.cfg Generator")
root.geometry("600x200")

# Folder containing .rvmat files
tk.Label(root, text="Folder Containing .rvmat Files:").pack(pady=10, anchor="w")
input_folder_var = tk.StringVar()
tk.Entry(root, textvariable=input_folder_var, width=50).pack(padx=10)
tk.Button(root, text="Browse", command=lambda: input_folder_var.set(filedialog.askdirectory())).pack(pady=5)

# Generate layers.cfg button
tk.Button(root, text="Generate layers.cfg", command=create_layers_cfg, bg="green", fg="white").pack(pady=20)

# Run the application
root.mainloop()
