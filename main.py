import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from PIL import Image, ImageTk
import cv2
import numpy as np


class ImageProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Обработка изображений")
        self.root.geometry("1200x450")

        self.current_image = None
        self.current_image_path = None
        self.result_image = None
        self.display_image = None

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
        btn_camera = tk.Button(file_frame, text="Сделать снимок с веб-камеры", command=self.capture_from_camera)
        btn_camera.pack(fill="x")

    def _create_channel_frame(self, parent):
        channel_frame = tk.LabelFrame(parent, text="Каналы", padx=10, pady=10)
        channel_frame.pack(fill="x")

        btn_red = tk.Button(channel_frame, text="Красный", command=lambda: self.apply_channel('red'))
        btn_red.pack(fill="x")
        btn_green = tk.Button(channel_frame, text="Зелёный", command=lambda: self.apply_channel('green'))
        btn_green.pack(fill="x")
        btn_blue = tk.Button(channel_frame, text="Синий", command=lambda: self.apply_channel('blue'))
        btn_blue.pack(fill="x")
        btn_reset = tk.Button(channel_frame, text="Сбросить", command=self.reset_display)
        btn_reset.pack(fill="x")

    def _create_func_frame(self, parent):
        func_frame = tk.LabelFrame(parent, text="Функции", padx=10, pady=10)
        func_frame.pack(fill="x")

        btn_neg = tk.Button(func_frame, text="Негатив", command=self.apply_negative)
        btn_neg.pack(fill="x")
        btn_bright = tk.Button(func_frame, text="Яркость", command=self.change_brightness)
        btn_bright.pack(fill="x")
        btn_circle = tk.Button(func_frame, text="Круг")
        btn_circle.pack(fill="x")
        btn_reset = tk.Button(func_frame, text="Сбросить изменения", command=self.reset_result)
        btn_reset.pack(fill="x")

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
            self.display_image = self.current_image.copy()
            self._update_display()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить изображение:\n{str(e)}")

    def capture_from_camera(self):
        try:
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                messagebox.showerror("Ошибка", "Не удалось открыть веб-камеру")
                return

            captured_image = None
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    messagebox.showerror("Ошибка", "Не удалось захватить изображение с веб-камеры")
                    break

                cv2.imshow("Camera - press SPACE to capture or ESC to exit", frame)
                
                key = cv2.waitKey(1) & 0xFF
                if key == 32:
                    captured_image = frame.copy()
                    break
                elif key == 27:
                    break

            cap.release()
            cv2.destroyAllWindows()

            if captured_image is not None:
                frame_rgb = cv2.cvtColor(captured_image, cv2.COLOR_BGR2RGB)
                self.current_image = Image.fromarray(frame_rgb)
                self.current_image_path = None
                self.result_image = self.current_image.copy()
                self.display_image = self.current_image.copy()
                self._update_display()
        except Exception as e:
            cv2.destroyAllWindows()
            messagebox.showerror("Ошибка", f"Не удалось получить изображение с веб-камеры:\n{str(e)}")

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

    def apply_channel(self, channel):
        if self.current_image is None:
            return

        self.display_image = self.current_image.copy()

        if self.display_image.mode != 'RGB':
            self.display_image = self.display_image.convert('RGB')

        r, g, b = self.display_image.split()
        
        if channel == 'red':
            self.display_image = Image.merge('RGB', (r, Image.new('L', r.size, 0), Image.new('L', r.size, 0)))
        elif channel == 'green':
            self.display_image = Image.merge('RGB', (Image.new('L', g.size, 0), g, Image.new('L', g.size, 0)))
        elif channel == 'blue':
            self.display_image = Image.merge('RGB', (Image.new('L', b.size, 0), Image.new('L', b.size, 0), b))

        self._update_display()

    def apply_negative(self):
        if self.result_image is None:
            return

        img_array = np.array(self.result_image)
        img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
        neg_bgr = cv2.bitwise_not(img_bgr)
        neg_rgb = cv2.cvtColor(neg_bgr, cv2.COLOR_BGR2RGB)
        self.result_image = Image.fromarray(neg_rgb)

        self._update_display()

    def change_brightness(self):
        if self.current_image is None:
            return

        brightness = tk.simpledialog.askinteger(
            "Изменение яркости",
            "Введите значение яркости (-255 до 255):",
            parent=self.root,
            minvalue=-255,
            maxvalue=255
        )

        if brightness is None:
            return

        img_array = np.array(self.result_image)
        img_hsv = cv2.cvtColor(img_array, cv2.COLOR_RGB2HSV).astype(np.float32)

        img_hsv[:, :, 2] = np.clip(img_hsv[:, :, 2] + brightness, 0, 255)

        img_hsv = img_hsv.astype(np.uint8)
        img_rgb = cv2.cvtColor(img_hsv, cv2.COLOR_HSV2RGB)
        self.result_image = Image.fromarray(img_rgb)

        self._update_display()

    def reset_display(self):
        if self.current_image is not None:
            self.display_image = self.current_image.copy()
            self._update_display()

    def reset_result(self):
        if self.result_image is not None:
            result = messagebox.askokcancel(
                "Подтверждение",
                "Вы хотите сбросить изменения?"
            )
            if result:
                self.result_image = self.current_image.copy()
                self._update_display()

    def _update_display(self):
        if self.current_image is None:
            return

        self._display_image(self.original_label, self.display_image)

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
