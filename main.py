import tkinter as tk


root = tk.Tk()
root.title("Обработка изображений — вариант 21")
root.geometry("1000x450")
root.resizable(False, False)

left_frame = tk.Frame(root, width=200, padx=10, pady=10)
left_frame.grid(row=0, column=0, sticky="ns")
left_frame.grid_propagate(False)

file_frame = tk.LabelFrame(left_frame, text="Действия с файлом", padx=10, pady=10)
file_frame.pack(fill="x")

btn_load = tk.Button(file_frame, text="Загрузить")
btn_load.pack(fill="x")
btn_save = tk.Button(file_frame, text="Сохранить")
btn_save.pack(fill="x")
btn_save_as = tk.Button(file_frame, text="Сохранить как")
btn_save_as.pack(fill="x")

channel_frame = tk.LabelFrame(left_frame, text="Каналы", padx=10, pady=10)
channel_frame.pack(fill="x")

btn_red = tk.Button(channel_frame, text="Красный")
btn_red.pack(fill="x")
btn_green = tk.Button(channel_frame, text="Зелёный")
btn_green.pack(fill="x")
btn_blue = tk.Button(channel_frame, text="Синий")
btn_blue.pack(fill="x")

func_frame = tk.LabelFrame(left_frame, text="Функции", padx=10, pady=10)
func_frame.pack(fill="x")

btn_neg = tk.Button(func_frame, text="Негатив")
btn_neg.pack(fill="x")
btn_bright = tk.Button(func_frame, text="Яркость")
btn_bright.pack(fill="x")
btn_circle = tk.Button(func_frame, text="Круг")
btn_circle.pack(fill="x")

right_frame = tk.Frame(root, padx=10, pady=10)
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

root.mainloop()
