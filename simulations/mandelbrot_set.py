import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from helpers import get_file_name


def mandelbrot(
    width=800,
    height=600,
    max_iter=200,
    step=25,
    x_min=-2.5,
    x_max=1.0,
    y_min=-1.2,
    y_max=1.2,
):
    x = np.linspace(x_min, x_max, width)
    y = np.linspace(y_min, y_max, height)
    C = x[None, :] + 1j * y[:, None]

    Z = np.zeros_like(C)
    escaped = np.zeros(C.shape, dtype=bool)
    escape_iter = np.full(C.shape, max_iter)

    frames = []

    for i in range(max_iter):
        Z[~escaped] = Z[~escaped] ** 2 + C[~escaped]

        newly_escaped = (Z.real**2 + Z.imag**2 > 4) & (~escaped)
        escape_iter[newly_escaped] = i
        escaped[newly_escaped] = True

        # capture frame
        if (i + 1) % step == 0 or i == max_iter - 1:
            frames.append(escape_iter.copy())

    return frames


frames = mandelbrot(max_iter=200, step=5)

cols = 4
rows = (len(frames) + cols - 1) // cols

fig, ax = plt.subplots(figsize=(6, 4))
im = ax.imshow(frames[0], origin="lower", cmap="inferno")
ax.axis("off")


def update(frame):
    im.set_data(frame)
    return (im,)


anim = FuncAnimation(fig, update, frames=frames, interval=200, blit=True)

anim.save(get_file_name("mandelbrot_set", extension="gif"), fps=1)
