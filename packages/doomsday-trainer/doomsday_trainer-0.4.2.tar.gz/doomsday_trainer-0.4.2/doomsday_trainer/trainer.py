"""Doomsday Trainer."""

import argparse
import sys
from .dates import DoomsdayRule, DoomsDate, DoomsWeekday
from .gui import SimpleGui

DEFAULT_START_YEAR = 1800
DEFAULT_END_YEAR = 2099


class DoomsdayTrainer:
    """Doomsday trainer class."""

    def __init__(self, start_year: int, end_year: int) -> None:
        """Init method."""
        self.start_date = DoomsDate(start_year, 1, 1)
        self.end_date = DoomsDate(end_year, 12, 31)
        self.date = self.start_date  # to keep mypy happy
        self.new_date()

    def new_date(self):
        """Set a new random DoomsDate within date interval."""
        self.date = DoomsDate.random(self.start_date, self.end_date)


def main() -> None:
    """Run main code."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--start-year",
        type=int,
        default=DEFAULT_START_YEAR,
        help=f"Start year [{DEFAULT_START_YEAR}]",
    )
    parser.add_argument(
        "--end-year", type=int, default=DEFAULT_END_YEAR, help=f"End year [{DEFAULT_END_YEAR}]"
    )
    args = parser.parse_args()

    if args.start_year > args.end_year:
        print("Error: Start year must be less than or equal to end year.", file=sys.stderr)
        return

    trainer = DoomsdayTrainer(args.start_year, args.end_year)
    gui = SimpleGui(
        date=trainer.date,
        header=f"Generating dates between {trainer.start_date} and {trainer.end_date}",
    )

    # Event loop
    while True:
        event, values = gui.window.read()

        if event in gui.EXIT_EVENTS:
            break

        if event == gui.KEY_DOOMSDAY:
            rule = DoomsdayRule(trainer.date)
            gui.update_result(rule.year_doomsday_string())
            continue

        # Try to create a DoomsWeekday from the event
        answer_doomsweekday = DoomsWeekday.create_from_name(event)

        if answer_doomsweekday is not None:
            if answer_doomsweekday == trainer.date.doomsweekday():
                gui.update_result(f"{trainer.date} is a {event}")
                trainer.new_date()
                gui.update_date(str(trainer.date))
            else:
                gui.update_date(str(trainer.date), error=True)
                gui.update_result(f"{trainer.date} isn't a {event}")

    gui.window.close()
