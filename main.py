import time
from copy import deepcopy
from threading import Thread, Event

from tkinter import Tk, Button, Label, Frame

class Board(Tk):
    def __init__(self, ROWS = 25, COLS = 25):
        super().__init__()

        self.ROWS = ROWS
        self.COLS = COLS

        self.DEAD_CELL = 'lightgray'
        self.ALIVE_CELL = 'gray'

        self.title('Game of Life')
        self.resizable(False, False)
        
        self.cells_frame = Frame(self, bg = 'white', relief = 'sunken')
        self.cells_frame.pack()

        self.cell_labels = []
        self.cell_values = []

        self.stop_event = None

        for i in range(self.ROWS):
            row_cells = []
            row_values = []

            for j in range(self.COLS):
                cell = Label(self.cells_frame, text = '', width = 2, relief = 'raised', bg = self.DEAD_CELL)
                cell.grid(row = i, column = j)
                cell.bind('<Button-1>', lambda event, cell = cell, i = i, j = j: self.toggle_label(event, cell, i, j))

                row_cells.append(cell)
                row_values.append(False)
            
            self.cell_labels.append(row_cells)
            self.cell_values.append(row_values)
        
        self.control_frame = Frame(self)
        self.control_frame.pack()

        self.start_btn = Button(self.control_frame, text = 'Start', command = self.start_gen_thread)
        self.start_btn.pack(side = 'left')

        self.clear_btn = Button(self.control_frame, text = 'Clear', command = self.clear_cells)
        self.clear_btn.pack(side = 'right')

        self.next_gen_btn = Button(self.control_frame, text = 'Next', command = self.calc_next_gen)
        self.next_gen_btn.pack(side = 'right')

        self.update_idletasks()

        self.root_width, self.root_height = tuple(map(int, self.geometry().split('+')[0].split('x')))

        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()

        self.x = ((self.screen_width // 2) - (self.root_width // 2))
        self.y = ((self.screen_height // 2) - (self.root_height // 2))

        self.geometry(f'{self.root_width}x{self.root_height}+{self.x}+{self.y}')

        self.mainloop()
    
    def toggle_label(self, event, cell, i, j):
        if self.stop_event is None:
            color = self.DEAD_CELL if cell.cget('bg') == self.ALIVE_CELL else self.ALIVE_CELL
            cell.config(bg = color)

            self.cell_values[i][j] = not self.cell_values[i][j]
    
    def is_safe(self, i, j):
        return 0 <= i < self.ROWS and 0 <= j < self.COLS
    
    def count_neighbors(self, i, j):
        neighbor_count = 0

        for x in range(-1, 2):
            for y in range(-1, 2):
                if x == 0 and y == 0:
                    continue

                I, J = i + x, j + y

                if self.is_safe(I, J) and self.cell_values[I][J]:
                    neighbor_count += 1
        
        return neighbor_count
    
    def calc_next_gen(self):
        next_gen_values = deepcopy(self.cell_values)

        for i in range(self.ROWS):
            for j in range(self.COLS):
                neighbor_count = self.count_neighbors(i, j)

                if self.cell_values[i][j]:
                    if neighbor_count < 2 or neighbor_count > 3:
                        next_gen_values[i][j] = False
                
                else:
                    if neighbor_count == 3:
                        next_gen_values[i][j] = True
        
        self.cell_values = deepcopy(next_gen_values)

        for i in range(self.ROWS):
            for j in range(self.COLS):
                color = self.ALIVE_CELL if self.cell_values[i][j] else self.DEAD_CELL
                self.cell_labels[i][j].config(bg = color)
    
    def start_gen(self):
        while self.stop_event is not None:
            next_gen_values = deepcopy(self.cell_values)

            for i in range(self.ROWS):
                for j in range(self.COLS):
                    neighbor_count = self.count_neighbors(i, j)

                    if self.cell_values[i][j]:
                        if neighbor_count < 2 or neighbor_count > 3:
                            next_gen_values[i][j] = False
                    
                    else:
                        if neighbor_count == 3:
                            next_gen_values[i][j] = True
            
            self.cell_values = deepcopy(next_gen_values)

            for i in range(self.ROWS):
                for j in range(self.COLS):
                    color = self.ALIVE_CELL if self.cell_values[i][j] else self.DEAD_CELL
                    self.cell_labels[i][j].config(bg = color)
    
    def clear_cells(self):
        for i in range(self.ROWS):
            for j in range(self.COLS):
                self.cell_labels[i][j].config(bg = self.DEAD_CELL)
                self.cell_values[i][j] = False
    
    def start_gen_thread(self):
        if self.stop_event is None:
            self.start_btn.config(text = 'Stop')
            self.clear_btn['state'] = 'disabled'
            self.next_gen_btn['state'] = 'disabled'

            self.stop_event = Event()

            Thread(target = self.start_gen).start()
        
        else:
            self.stop_event.set()
            self.stop_event = None

            self.start_btn.config(text = 'Start')
            self.clear_btn['state'] = 'normal'
            self.next_gen_btn['state'] = 'normal'

if __name__ == '__main__':
    Board()