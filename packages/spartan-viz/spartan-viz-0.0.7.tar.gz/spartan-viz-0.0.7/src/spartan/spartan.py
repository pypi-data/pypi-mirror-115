
import matplotlib as mpl
import matplotlib.pyplot as plt
    
def init():
    '''Read style file to set base spartan style.'''

    print("Setting default spartan style....")
    plt.style.use("spartan.mplstyle")


def change_defaults(context = "default"):
    '''Allow the user to customize the base style, including:
       * contexts,
       * more coming soon...
       '''

    print("Your context is set to:", context)

    if context == "poster":
        # mpl.rcParams['axes.labelsize'] = 30
        mpl.rcParams['xtick.labelsize'] = 24
        mpl.rcParams['ytick.labelsize'] = 24
        mpl.rcParams['grid.color'] = '#888888'
        mpl.rcParams['lines.linewidth'] = 3.8

    elif context == "projection":
        mpl.rcParams['xtick.labelsize'] = 20
        mpl.rcParams['ytick.labelsize'] = 20
        mpl.rcParams['lines.linewidth'] = 3.0

    elif context == "monitor":
        mpl.rcParams['xtick.labelsize'] = 12
        mpl.rcParams['ytick.labelsize'] = 12
        mpl.rcParams['lines.linewidth'] = 2.2

    elif context == "web_meeting":
        mpl.rcParams['xtick.labelsize'] = 16
        mpl.rcParams['ytick.labelsize'] = 16
        mpl.rcParams['lines.linewidth'] = 2.8

    elif context == "publication":
        mpl.rcParams['xtick.labelsize'] = 14
        mpl.rcParams['ytick.labelsize'] = 14
        mpl.rcParams['lines.linewidth'] = 2.0
