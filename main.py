import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk


class ImageProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Обработка изображений")
        self.root.geometry("1200x450")

        self.current_image = None
        self.current_image_path = None
        self.result_image = None

        self._create_left_frame()
        self._create_right_frame()

    def _create_left_frame(self):
        left_frame = tk.Frame(self.root, width=200, padx=10, pady=10)
        left_frame.grid(row=0, column=0, sticky="ns")
        left_frame.grid_propagate(False)

        self._create_file_frame(left_frame)
        self._create_channel_frame(left_frame)
        self._create_func_frame(left_frame)

    def _create_file_frame(self, parent):
        file_frame = tk.LabelFrame(parent, text="Действия с файлом", padx=10, pady=10)
        file_frame.pack(fill="x")

        btn_load = tk.Button(file_frame, text="Загрузить", command=self.load_image)
        btn_load.pack(fill="x")
        btn_save = tk.Button(file_frame, text="Сохранить", command=self.save_image)
        btn_save.pack(fill="x")
        btn_save_as = tk.Button(file_frame, text="Сохранить как", command=self.save_image_as)
        btn_save_as.pack(fill="x")
        btn_camera = tk.Button(file_frame, text="Сделать снимок с веб-камеры")
        btn_camera.pack(fill="x")

    def _create_channel_frame(self, parent):
        channel_frame = tk.LabelFrame(parent, text="Каналы", padx=10, pady=10)
        channel_frame.pack(fill="x")

        btn_red = tk.Button(channel_frame, text="Красный")
        btn_red.pack(fill="x")
        btn_green = tk.Button(channel_frame, text="Зелёный")
        btn_green.pack(fill="x")
        btn_blue = tk.Button(channel_frame, text="Синий")
        btn_blue.pack(fill="x")

    def _create_func_frame(self, parent):
        func_frame = tk.LabelFrame(parent, text="Функции", padx=10, pady=10)
        func_frame.pack(fill="x")

        btn_neg = tk.Button(func_frame, text="Негатив")
        btn_neg.pack(fill="x")
        btn_bright = tk.Button(func_frame, text="Яркость")
        btn_bright.pack(fill="x")
        btn_circle = tk.Button(func_frame, text="Круг")
        btn_circle.pack(fill="x")

    def _create_right_frame(self):
        right_frame = tk.Frame(self.root, pady=10)
        right_frame.grid(row=0, column=1, sticky="ns")

        original_container = tk.LabelFrame(right_frame, text="Оригинал", width=450, height=420, padx=10, pady=10)
        original_container.grid(row=0, column=0, padx=10)
        original_container.grid_propagate(False)

        result_container = tk.LabelFrame(right_frame, text="Результат", width=450, height=420, padx=10, pady=10)
        result_container.grid(row=0, column=1)
        result_container.grid_propagate(False)

        self.original_label = tk.Label(
            original_container,
            bg="#e0e0e0"
        )
        self.original_label.pack(fill="both", expand=True, padx=2, pady=2)

        self.result_label = tk.Label(
            result_container,
            bg="#e0e0e0"
        )
        self.result_label.pack(fill="both", expand=True, padx=2, pady=2)

    def load_image(self):
        file_path = filedialog.askopenfilename(
            title="Выберите изображение",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff")]
        )
        if not file_path:
            return

        try:
            self.current_image = Image.open(file_path)
            self.current_image_path = file_path
            self.result_image = self.current_image.copy()
            self._update_display()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить изображение:\n{str(e)}")

    def save_image(self):
        if self.result_image is None:
            messagebox.showwarning("Предупреждение", "Нет изображения для сохранения")
            return

        if self.current_image_path:
            try:
                self.result_image.save(self.current_image_path)
                messagebox.showinfo("Успех", "Изображение сохранено")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить изображение:\n{str(e)}")
        else:
            self.save_image_as()

    def save_image_as(self):
        if self.result_image is None:
            messagebox.showwarning("Предупреждение", "Нет изображения для сохранения")
            return

        file_path = filedialog.asksaveasfilename(
            title="Сохранить изображение как",
            defaultextension=".png",
            filetypes=[
                ("PNG files", "*.png"),
                ("JPEG files", "*.jpg *.jpeg"),
                ("BMP files", "*.bmp"),
                ("All files", "*.*")
            ]
        )
        if not file_path:
            return

        try:
            self.result_image.save(file_path)
            self.current_image_path = file_path
            messagebox.showinfo("Успех", "Изображение сохранено")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить изображение:\n{str(e)}")

    def _update_display(self):
        if self.current_image is None:
            return

        self._display_image(self.original_label, self.current_image)

        if self.result_image is not None:
            self._display_image(self.result_label, self.result_image)

    def _display_image(self, label, image):
        container_width = 440
        container_height = 400

        orig_width, orig_height = image.size

        scale = min(container_width / orig_width, container_height / orig_height)
        new_width = int(orig_width * scale)
        new_height = int(orig_height * scale)

        resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

        photo = ImageTk.PhotoImage(resized_image)

        label.config(image=photo)
        label.image = photo

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessorApp(root)
    root.mainloop()
