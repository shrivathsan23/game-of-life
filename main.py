import time
from threading import Thread, Event

from tkinter import Tk, Button, Label, Frame

class State:
    DEAD_CELL = 'lightgray'
    ALIVE_CELL = 'gray'

class Cell(Label):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.config(bg = State.DEAD_CELL)
        self.state = False
    
    def toggle_state(self):
        self.config(bg = State.DEAD_CELL if self.cget('bg') == State.ALIVE_CELL else State.ALIVE_CELL)
        self.state = not self.state
    
    def get_state(self):
        return self.state
    
    def set_state(self, state):
        if self.state != state:
            self.toggle_state()

class Board(Tk):
    def __init__(self, ROWS = 25, COLS = 25):
        super().__init__()

        self.ROWS = ROWS
        self.COLS = COLS
        
        self.title('Game of Life')
        self.resizable(False, False)

        self.cells_frame = Frame(self, bg = 'white', relief = 'sunken')
        self.cells_frame.pack()

        self.cells = [[None for j in range(self.COLS)] for i in range(self.ROWS)]
        self.stop_event = None

        for i in range(self.ROWS):
            for j in range(self.COLS):
                cell = Cell(self.cells_frame, text = '', width = 2, relief = 'raised')
                
                cell.grid(row = i, column = j)
                cell.bind('<Button-1>', lambda event, cell = cell: self.toggle_cell(cell))
                
                self.cells[i][j] = cell
        
        self.control_frame = Frame(self)
        self.control_frame.pack()

        self.start_btn = Button(self.control_frame, text = 'Start', command = self.start_gen_thread)
        self.start_btn.pack(side = 'left')

        self.clear_btn = Button(self.control_frame, text = 'Clear', command = self.clear_cells)
        self.clear_btn.pack(side = 'right')

        self.next_gen_btn = Button(self.control_frame, text = 'Next', command = self.calc_next_gen)
        self.next_gen_btn.pack(side = 'right')

        self.update_idletasks()
        self.geometry(f'{self.winfo_reqwidth()}x{self.winfo_reqheight()}+10+10')

        self.mainloop()
    
    def toggle_cell(self, cell):
        if self.stop_event is None:
            cell.toggle_state()
    
    def is_safe(self, i, j):
        return 0 <= i < self.ROWS and 0 <= j < self.COLS
    
    def count_neighbors(self, i, j):
        neighbor_count = 0

        for x in range(-1, 2):
            for y in range(-1, 2):
                if x == 0 and y == 0:
                    continue

                new_i, new_j = i + x, j + y

                if self.is_safe(new_i, new_j) and self.cells[new_i][new_j].get_state():
                    neighbor_count += 1
        
        return neighbor_count
    
    def calc_next_gen(self):
        next_gen_values = [[self.cells[i][j].get_state() for j in range(self.COLS)] for i in range(self.ROWS)]

        for i in range(self.ROWS):
            for j in range(self.COLS):
                neighbor_count = self.count_neighbors(i, j)

                if self.cells[i][j].get_state():
                    if neighbor_count < 2 or neighbor_count > 3:
                        next_gen_values[i][j] = False
                
                else:
                    if neighbor_count == 3:
                        next_gen_values[i][j] = True
        
        [[self.cells[i][j].set_state(next_gen_values[i][j]) for j in range(self.COLS)] for i in range(self.ROWS)]
    
    def start_gen(self):
        while self.stop_event is not None:
            self.calc_next_gen()
            time.sleep(0.025)
    
    def clear_cells(self):
        [[self.cells[i][j].set_state(False) for j in range(self.COLS)] for i in range(self.ROWS)]
    
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
    Board(35, 76)