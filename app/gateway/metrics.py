import time


class Metrics:

    @staticmethod
    def start_timer() -> float:
        return time.perf_counter()

    @staticmethod
    def elapsed_ms(start_time: float) -> float:
        return round(
            (time.perf_counter() - start_time) * 1000,
            2,
        )