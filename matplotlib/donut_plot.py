# Libraries
import numpy as np
import matplotlib.pyplot as plt


def full_donut():
    """Make data: I have 3 groups and 7 subgroups"""
    group_names = ['groupA', 'groupB', 'groupC']
    group_size = [12, 11, 30]
    subgroup_names = ['A.1', 'A.2', 'A.3', 'B.1', 'B.2', 'C.1', 'C.2', 'C.3', 'C.4', 'C.5']
    subgroup_size = [4, 3, 5, 6, 5, 10, 5, 5, 4, 6]

    # Create colors
    a, b, c = [plt.cm.Blues, plt.cm.Reds, plt.cm.Greens]

    # First Ring (outside)
    fig, ax = plt.subplots()
    ax.axis('equal')
    mypie, _ = ax.pie(group_size, radius=1.3, labels=group_names, colors=[a(0.6), b(0.6), c(0.6)])
    plt.setp(mypie, width=0.3, edgecolor='white')

    # Second Ring (Inside)
    mypie2, _ = ax.pie(subgroup_size, radius=1.3 - 0.3, labels=subgroup_names, labeldistance=0.7,
                       colors=[a(0.5), a(0.4), a(0.3), b(0.5), b(0.4), c(0.6), c(0.5), c(0.4), c(0.3), c(0.2)])
    plt.setp(mypie2, width=0.4, edgecolor='white')
    plt.margins(0, 0)


def curvelet_plot(scales):
    # Create colors
    a, b, c = [plt.cm.Blues, plt.cm.Reds, plt.cm.Greens]

    # Set up plot
    fig, ax = plt.subplots()
    ax.axis('equal')

    mypies = []
    for scale in range(1, scales + 1):
        group_size = [30, 30, 30]
        subgroup_size = 10 * np.ones([9])
        print(len(subgroup_size))

        # First Ring (outside)
        mypie, _ = ax.pie(group_size, radius=scale, colors=[a(0.6), b(0.6), c(0.6)])
        plt.setp(mypie, width=1, edgecolor='white')

        # # Second Ring (Inside)
        # mypie2, _ = ax.pie(subgroup_size, radius=1,
        #                    colors=[a(0.5), a(0.4), a(0.3), b(0.5), b(0.4), c(0.6), c(0.5), c(0.4), c(0.3), c(0.2)])
        # plt.setp(mypie2, width=1, edgecolor='white')
        plt.margins(0, 0)


if __name__ == '__main__':
    curvelet_plot(2)
    # show it
    plt.show()
