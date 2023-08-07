import tkinter as tk
from tkinter import ttk
from tkinter.colorchooser import askcolor
from tkinter import filedialog
from PIL import Image, ImageDraw

class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Drawing App")

        self.canvas = tk.Canvas(root, bg="white", width=800, height=600)
        self.canvas.pack()

        self.color_button = ttk.Button(root, text="Select Color", command=self.select_color)
        self.color_button.pack()

        self.pencil_button = ttk.Button(root, text="Pencil Tool", command=self.activate_pencil_tool)
        self.pencil_button.pack()

        self.paint_bucket_button = ttk.Button(root, text="Paint Bucket Tool", command=self.activate_paint_bucket_tool)
        self.paint_bucket_button.pack()

        self.save_button = ttk.Button(root, text="Save Image", command=self.save_image)
        self.save_button.pack()

        self.active_tool = None
        self.current_color = "black"

        self.canvas.bind("<Button-1>", self.mouse_down)
        self.canvas.bind("<B1-Motion>", self.mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.mouse_up)

        self.image = Image.new("RGB", (800, 600), "white")
        self.draw = ImageDraw.Draw(self.image)

    def select_color(self):
        color = askcolor()[1]
        if color:
            self.current_color = color

    def activate_pencil_tool(self):
        self.active_tool = "pencil"

    def activate_paint_bucket_tool(self):
        self.active_tool = "paint_bucket"

    def mouse_down(self, event):
        if self.active_tool == "pencil":
            self.prev_x = event.x
            self.prev_y = event.y
        elif self.active_tool == "paint_bucket":
            self.paint_bucket(event.x, event.y, self.current_color)

    def mouse_drag(self, event):
        if self.active_tool == "pencil":
            self.canvas.create_line(self.prev_x, self.prev_y, event.x, event.y, fill=self.current_color, width=2)
            self.draw.line((self.prev_x, self.prev_y, event.x, event.y), fill=self.current_color, width=2)
            self.prev_x = event.x
            self.prev_y = event.y

    def mouse_up(self, event):
        pass

    def paint_bucket(self, x, y, fill_color):
        target_color = self.image.getpixel((x, y))
        width, height = self.image.size
        self.fill_region(x, y, target_color, fill_color, width, height)

    def fill_region(self, x, y, target_color, fill_color, width, height):
        if x < 0 or x >= width or y < 0 or y >= height:
            return
        current_color = self.image.getpixel((x, y))
        if current_color != target_color:
            return
        self.draw.rectangle((x, y, x + 1, y + 1), fill=fill_color)
        self.canvas.create_rectangle(x, y, x + 1, y + 1, fill=fill_color, outline="")
        self.fill_region(x + 1, y, target_color, fill_color, width, height)
        self.fill_region(x - 1, y, target_color, fill_color, width, height)
        self.fill_region(x, y + 1, target_color, fill_color, width, height)
        self.fill_region(x, y - 1, target_color, fill_color, width, height)

    def save_image(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if file_path:
            self.image.save(file_path)

if __name__ == "__main__":
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()
