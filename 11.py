import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import numpy as np

def calculate_bezier(points, t):
    n = len(points) - 1
    while len(points) > 1:
        points = [(1 - t) * np.array(points[i]) + t * np.array(points[i + 1]) for i in range(len(points) - 1)]
    return points[0]

def calculate_bezier_steps(points, t_values):
    curve_points = []
    steps = []
    for t in t_values:
        intermediate_steps = [np.array(points)]
        temp_points = points.copy()
        while len(temp_points) > 1:
            temp_points = [(1 - t) * np.array(temp_points[i]) + t * np.array(temp_points[i + 1]) for i in range(len(temp_points) - 1)]
            intermediate_steps.append(temp_points)
        curve_points.append(temp_points[0])
        steps.append(intermediate_steps)
    return np.array(curve_points), steps

def draw_curve():
    try:
        raw_points = entry_points.get()
        points = [tuple(map(float, p.split(','))) for p in raw_points.split(';')]
        t_steps = int(entry_steps.get())
        if t_steps <= 0:
            raise ValueError("Количество шагов должно быть больше нуля.")
        
        curve_points = []
        t_values = np.linspace(0, 1, t_steps)
        for t in t_values:
            curve_points.append(calculate_bezier(points, t))

        curve_points = np.array(curve_points)
        points = np.array(points)

        plt.figure(figsize=(8, 6))
        plt.plot(points[:, 0], points[:, 1], 'ro-', label='Контрольные точки')
        plt.plot(curve_points[:, 0], curve_points[:, 1], 'b-', label='Кривая Безье')
        plt.legend()
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('Квадратичная кривая Безье')
        plt.grid(True)
        plt.show()
    except Exception as e:
        messagebox.showerror("Ошибка", str(e))

def draw_cubic_bezier():
    try:
        raw_points = entry_points.get()
        points = [tuple(map(float, p.split(','))) for p in raw_points.split(';')]
        t_steps = int(entry_steps.get())
        if t_steps <= 0:
            raise ValueError("Количество шагов должно быть больше нуля.")

        t_values = np.linspace(0, 1, t_steps)
        curve_points, steps = calculate_bezier_steps(points, t_values)
        points = np.array(points)

        plt.figure(figsize=(8, 6))
        plt.plot(points[:, 0], points[:, 1], 'ro-', label='Контрольные точки')
        plt.plot(curve_points[:, 0], curve_points[:, 1], 'b-', label='Кубическая кривая Безье')

        for t_idx, t in enumerate(t_values):
            for step in steps[t_idx]:
                step = np.array(step)
                plt.plot(step[:, 0], step[:, 1], 'g--', alpha=0.5)

        plt.legend()
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('Кубическая кривая Безье с промежуточными вершинами')
        plt.grid(True)
        plt.show()
    except Exception as e:
        messagebox.showerror("Ошибка", str(e))

def draw_chaikin():
    try:
        raw_points = entry_points.get()
        points = [tuple(map(float, p.split(','))) for p in raw_points.split(';')]
        iterations = int(entry_steps.get())
        if iterations < 0:
            raise ValueError("Количество итераций должно быть неотрицательным.")

        subdivided_points = chaikin_subdivide(points, iterations)
        subdivided_points = np.array(subdivided_points)
        points = np.array(points)

        plt.figure(figsize=(8, 6))
        plt.plot(points[:, 0], points[:, 1], 'ro-', label='Контрольные точки')
        plt.plot(subdivided_points[:, 0], subdivided_points[:, 1], 'g-', label='Кривая Чайкина')
        plt.legend()
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('Кривая Чайкина')
        plt.grid(True)
        plt.show()
    except Exception as e:
        messagebox.showerror("Ошибка", str(e))

def chaikin_subdivide(points, iterations):
    for _ in range(iterations):
        new_points = []
        for i in range(len(points) - 1):
            p0, p1 = np.array(points[i]), np.array(points[i + 1])
            new_points.append(0.75 * p0 + 0.25 * p1)
            new_points.append(0.25 * p0 + 0.75 * p1)
        points = new_points
    return points

root = tk.Tk()
root.title("Генератор кривых и поверхностей")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack()

label_points = tk.Label(frame, text="Контрольные точки:")
label_points.grid(row=0, column=0, sticky="e")
entry_points = tk.Entry(frame, width=50)
entry_points.insert(0, "0,0; 2,4; 4,4; 6,0")
entry_points.grid(row=0, column=1)

label_steps = tk.Label(frame, text="Количество шагов:")
label_steps.grid(row=1, column=0, sticky="e")
entry_steps = tk.Entry(frame, width=20)
entry_steps.insert(0, "10")
entry_steps.grid(row=1, column=1, sticky="w")

button_draw_bezier = tk.Button(frame, text="Построить кривую Безье", command=draw_curve)
button_draw_bezier.grid(row=5, column=0, padx=5, pady=5)

button_draw_chaikin = tk.Button(frame, text="Построить кривую Чайкина", command=draw_chaikin)
button_draw_chaikin.grid(row=5, column=1, padx=5, pady=5)

button_draw_cubic_bezier = tk.Button(frame, text="Построить кубическую кривую Безье", command=draw_cubic_bezier)
button_draw_cubic_bezier.grid(row=5, column=2, padx=5, pady=5)

root.mainloop()
