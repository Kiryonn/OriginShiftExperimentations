import tkinter as tk

from interface_script import Interface
from res.scripts.Vectors import Vector2i
from res.scripts.interface.constants import BASE_MAZE_SIZE
from res.scripts.signals import Signal


def spinbox_vcmd(text: str) -> bool:
    return text.isdigit() or text == ''


class ControlPanel(tk.Frame):
    def __init__(self, master: Interface):
        super(ControlPanel, self).__init__(master)
        spinbox_cnf = {
            "width": 3
        }

        self.__step_label = tk.Label(self, text='Steps')
        self.__step_spinbox = tk.Spinbox(
            self, spinbox_cnf,
            from_=1, to=1000, width=4
        )
        self.__step_button = tk.Button(self, text='➤')
        self.__size_label = tk.Label(self, text='Size')
        self.__x_spinbox = tk.Spinbox(
            self, spinbox_cnf,
            from_=3, to=100,
            textvariable=tk.IntVar(value=BASE_MAZE_SIZE.x)
        )
        self.__y_spinbox = tk.Spinbox(
            self, spinbox_cnf,
            from_=3, to=100,
            textvariable=tk.IntVar(value=BASE_MAZE_SIZE.y)
        )
        self.__path_button_variable = tk.BooleanVar()
        self.__path_button = tk.Checkbutton(
            self, text='Show Solution', justify='center', anchor='center', variable=self.__path_button_variable
        )
        self.__save_image_button = tk.Button(self, text="Save Image")

        self.__step_label.pack(side='left', padx=(5, 0))
        self.__step_spinbox.pack(side='left', padx=(5, 0))
        self.__step_button.pack(side='left', padx=(5, 0))
        self.__size_label.pack(side='left', padx=(20, 0))
        self.__x_spinbox.pack(side='left', padx=(5, 0))
        self.__y_spinbox.pack(side='left', padx=(5, 0))
        self.__path_button.pack(side='left', padx=(20, 0))
        self.__save_image_button.pack(side='left', padx=(5, 0))

        self.__step_spinbox['validate'] = "all"
        self.__x_spinbox['validate'] = "all"
        self.__y_spinbox['validate'] = "all"

        """
		%d = Type of action (1=insert, 0=delete, -1 for others)
		%i = index of char string to be inserted/deleted, or -1
		%P = value of the entry if the edit is allowed
		%s = value of entry prior to editing
		%S = the text string being inserted or deleted, if any
		%v = the type of validation that is currently set
		%V = the type of validation that triggered the callback (key, focusin, focusout, forced)
		%W = the tk name of the widget
		"""
        self.spinbox_vcmd = self.register(spinbox_vcmd)
        vcmd = self.spinbox_vcmd, '%P'
        self.__step_spinbox['validatecommand'] = vcmd
        self.__x_spinbox['validatecommand'] = vcmd
        self.__y_spinbox['validatecommand'] = vcmd

        self.__x_spinbox["command"] = self.__on_maze_size_changed
        self.__y_spinbox["command"] = self.__on_maze_size_changed
        self.__path_button["command"] = self.__on_path_toggled
        self.__step_button["command"] = self.__on_step_clicked
        self.__save_image_button['command'] = self.__on_save_image_button_pressed

        self.__x_spinbox.bind(
            "<FocusOut>", lambda e: self.__on_maze_size_changed())
        self.__y_spinbox.bind(
            "<FocusOut>", lambda e: self.__on_maze_size_changed())

        self.on_maze_size_changed = Signal()
        self.on_step_clicked = Signal()
        self.on_path_toggled = Signal()
        self.on_save_image_button_pressed = Signal()

        self.last_maze_size: Vector2i = BASE_MAZE_SIZE

    def __on_step_clicked(self) -> None:
        nb_steps = int(self.__step_spinbox.get())
        self.on_step_clicked.emit(nb_steps)

    def __on_maze_size_changed(self) -> None:
        x, y = self.last_maze_size
        new_x, new_y = self.__x_spinbox.get(), self.__y_spinbox.get()
        if new_x:
            inx = int(new_x)
            if self.__x_spinbox.cget('from') <= inx <= self.__x_spinbox.cget('to'):
                x = inx
        if new_y:
            iny = int(new_y)
            if self.__y_spinbox.cget('from') <= iny <= self.__y_spinbox.cget('to'):
                y = iny
        new_size = Vector2i(x, y)
        if new_size == self.last_maze_size:
            return
        self.last_maze_size = new_size
        self.on_maze_size_changed.emit(new_size)

    def __on_path_toggled(self) -> None:
        is_toggled = self.__path_button_variable.get()
        self.on_path_toggled.emit(is_toggled)

    def __on_save_image_button_pressed(self):
        self.on_save_image_button_pressed.emit()
