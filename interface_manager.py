import tkinter as tk
from tkinter.constants import *
from classes import *

async def GrupuScreen():
    root = tk.Tk()
    root.title("Grupas")
    root.geometry("1920x1080")
    group_view = tk.Frame(root)
    group_view.grid(root, column=0, row=0)


async def PlanojumuScreen():
    pass