from __future__ import print_function
import matplotlib.pyplot as plt
import time
from daqhats import mcc128, HatIDs, HatError
from daqhats_utils import select_hat_device

READ_ALL_AVAILABLE = -1

CURSOR_BACK_2 = '\x1b[2D'
ERASE_TO_END_OF_LINE = '\x1b[0K'

def main():

    try:

        address = select_hat_device(HatIDs.MCC_128)
        hat = mcc128(address)

        print('\nSelected MCC 128 HAT device at address', address)

        try:
            input('\nPress ENTER to continue ...')
        except (NameError, SyntaxError):
            pass

        run(hat)

    except (HatError, ValueError) as err:
        print('\n', err)


def read_data(hat):

    tstart = time.time()
    while True:
        t = time.time() - tstart
        a1 = hat.a_in_read(0)
        a2 = hat.a_in_read(1)
        yield t, a1, a2

def run(hat, niter=1000):

    fig, ax = plt.subplots(1, 1)
    ax.set_aspect('equal')
    ax.set_xlim(0, 255)
    ax.set_ylim(0, 255)
    ax.hold(True)
    rd = read_data(hat)
    t, y1, y2 = rd.next()

    plt.show(False)
    plt.draw()

    background = fig.canvas.copy_from_bbox(ax.bbox)

    angle1points = ax.plot(t, y1, 'b')
    angle2points = ax.plot(t, y2, 'r')
    tic = time.time()

    while True:

        # update the xy data
        t, y1, y2 = rd.next()
        angle1points.set_data(t, y1)
        angle2points.set_data(t, y2)

        # restore background
        fig.canvas.restore_region(background)

        # redraw just the points
        ax.draw_artist(angle1points)
        ax.draw_artist(angle2points)

        # fill in the axes rectangle
        fig.canvas.blit(ax.bbox)

    plt.close(fig)