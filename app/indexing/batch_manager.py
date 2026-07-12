from typing import Iterator, TypeVar

T = TypeVar("T")


class BatchManager:

    @staticmethod
    def create_batches(
        items: list[T],
        batch_size: int,
    ) -> Iterator[list[T]]:

        for i in range(
            0,
            len(items),
            batch_size,
        ):

            yield items[
                i : i + batch_size
            ]