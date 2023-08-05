"""GUI code."""
try:
    import PySimpleGUI as sg  # type: ignore
except ModuleNotFoundError as e:
    if e.name in ["tkinter", "_tkinter"]:
        raise SystemExit("Error: The tkinter package is not properly installed on your computer.")
    else:
        raise SystemExit(f"Error: Could not import module '{e.name}'.")
from .dates import DoomsWeekday

THEME = "Gray Gray Gray"
WINDOW_TITLE = "Doomsday Trainer"

FONT_TEXT_DATE = ("Helvetica", 70, "bold")
FONT_TEXT_INFO = ("Helvetica", 14, "italic")
FONT_BUTTON_WEEKDAY = ("Helvetica", 12, "bold")
FONT_BUTTON_ACTION = ("Helvetica", 12)


class SimpleGui:
    """GUI class."""

    KEY_EXIT = "-EXIT-"
    KEY_DOOMSDAY = "-DOOMSDAY-"
    KEY_DATE = "-DATE-"
    KEY_RESULT = "-RESULT-"

    EXIT_EVENTS = (sg.WIN_CLOSED, KEY_EXIT)

    def __init__(self, date="", header="") -> None:
        """Initialise GUI."""
        self.date = date
        self.header = header
        sg.theme(THEME)
        self.window = sg.Window(WINDOW_TITLE, self.layout())

    def layout(self):
        """Return layout for GUI."""
        row_info_header = [
            sg.Push(),
            sg.Text(
                self.header,
                font=FONT_TEXT_INFO,
                pad=(5, 5),
            ),
            sg.Push(),
        ]

        row_date_label = [
            sg.Push(),
            sg.Text(
                self.date,
                key=self.KEY_DATE,
                font=FONT_TEXT_DATE,
                pad=(5, 15),
            ),
            sg.Push(),
        ]

        row_layout_buttons = []

        for day in DoomsWeekday.names_iso_order():
            row_layout_buttons.append(sg.Button(day, font=FONT_BUTTON_WEEKDAY))

        row_last_result = [
            sg.Push(),
            sg.Text(font=FONT_TEXT_INFO, key=self.KEY_RESULT, pad=(5, 5)),
            sg.Push(),
        ]

        row_exit_button = [
            sg.Push(),
            sg.Button("Doomsday", key=self.KEY_DOOMSDAY, font=FONT_BUTTON_ACTION),
            sg.Button("Exit", key=self.KEY_EXIT, font=FONT_BUTTON_ACTION),
            sg.Push(),
        ]

        return [
            row_info_header,
            row_date_label,
            row_layout_buttons,
            row_last_result,
            row_exit_button,
        ]

    def update_date(self, value: str, error=False):
        """Update date label."""
        text_color = "Black"

        if error:
            text_color = "Red"

        self.window[self.KEY_DATE].update(value, text_color=text_color)

    def update_result(self, value: str):
        """Update result text."""
        self.window[self.KEY_RESULT].update(value)
