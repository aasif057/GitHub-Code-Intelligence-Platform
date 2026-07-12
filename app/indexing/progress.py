from dataclasses import dataclass


@dataclass
class ProgressTracker:

    total: int

    current: int = 0

    task: str = ""

    def start(
        self,
        task: str,
    ):

        self.task = task
        self.current = 0

        print(f"\n{task}")
        print("-" * 60)

    def update(
        self,
        amount: int,
    ):

        self.current += amount

        percent = (
            self.current / self.total
        ) * 100

        print(
            f"\r"
            f"[{self.current}/{self.total}] "
            f"{percent:5.1f}% ",
            end="",
            flush=True,
        )

    def finish(self):

        print("\nDone.\n")