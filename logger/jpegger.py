import os
from datetime import datetime as dt
from typing import Self

import matplotlib.pyplot as plt
from matplotlib.figure import Figure


class JPEGger:
    folder_created: bool = False

    # Prevent instantiation
    def __new__(cls) -> Self:
        raise RuntimeError(f"{cls} should not be instantiated")

    @staticmethod
    def init(path_to_folder: str = "") -> None:
        JPEGger.path = os.path.join(
            path_to_folder,
            "my_jpegger",
            str(dt.now().strftime("%Y%m%d-%H%M%S")),
        )

    @staticmethod
    def lazy_init() -> None:
        os.mkdir(JPEGger.path)
        JPEGger.folder_created = True

    @staticmethod
    def save_jpg(fig: Figure, name: str) -> None:
        if not JPEGger.folder_created:
            JPEGger.lazy_init()
        fig.savefig(os.path.join(JPEGger.path, name))
        plt.close(fig)
