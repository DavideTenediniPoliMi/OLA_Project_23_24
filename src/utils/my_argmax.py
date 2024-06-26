import numpy as np


def my_argmax(x: np.ndarray) -> int:
    """
    Same as np.argmax but if there is a tie pick a random index.

    Args:
        x (np.ndarray): numpy array

    Returns:
        int: index of the element with the maximum value (ties broken randomly)
    """
    idxes = np.argwhere(x == np.max(x)).flatten()
    return np.random.choice(idxes)
