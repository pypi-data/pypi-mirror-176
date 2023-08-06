def MoveWindow(DaWindow, x, y):
    curX = DaWindow.winfo_x()
    curY = DaWindow.winfo_y()
    DaWindow.geometry(f'+{curX + x}+{curY + y}')
    DaWindow.update_idletasks()
def ChangeSize(DaWindow, width, height):
    DaWindow.geomatry(f'{width}x{height}')
    DaWindow.update_idletasks()