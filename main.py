import tkinter as tk


class ImageProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Обработка изображений")
        self.root.geometry("1200x450")
        self.root.resizable(False, False)

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

        btn_load = tk.Button(file_frame, text="Загрузить")
        btn_load.pack(fill="x")
        btn_save = tk.Button(file_frame, text="Сохранить")
        btn_save.pack(fill="x")
        btn_save_as = tk.Button(file_frame, text="Сохранить как")
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
        right_frame = tk.Frame(self.root, padx=10, pady=10)
        right_frame.grid(row=0, column=1, sticky="ns")

        original_label = tk.Label(
            right_frame,
            text="Оригинал",
            relief="solid",
            width=45,
            height=25,
            bg="#e0e0e0"
        )
        original_label.grid(row=0, column=0)

        result_label = tk.Label(
            right_frame,
            text="Результат",
            relief="solid",
            width=45,
            height=25,
            bg="#e0e0e0"
        )
        result_label.grid(row=0, column=1)


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessorApp(root)
    root.mainloop()