import hydroeval as he
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def plot_ts_cum(x,y1,y2,ylabel):

    """

    Parameters
    ----------
    x : TYPE
        DESCRIPTION.
    y1 : TYPE
        DESCRIPTION.
    y2 : TYPE
        DESCRIPTION.
    ylabel : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """ 
    
    # Time step
    dt = pd.Timedelta(x.values[1]-x.values[0])/np.timedelta64(1,'s')
    
    # Cummulative values
    Y1 = np.cumsum(y1)*dt
    Y2 = np.cumsum(y2)*dt
    
    # Total volume [%]
    V1 = 100
    V2 = int(Y2.values[-1]/Y1.values[-1]*100)
    
    # Cumulative plot
    plt.plot(x,Y1,label='simulation',marker='.',color='grey',alpha=0.5)
    plt.plot(x,Y2,label='reference',color='blue')
    plt.legend(loc='upper right')
    plt.ylabel(ylabel)
    plt.text(0.03,0.96, '$V_{sim}$ = '+str(V1)+' %'+'\n$V_{ref}$ = '+str(V2)+' %',
             verticalalignment='top',transform=plt.gca().transAxes,
             bbox=dict(facecolor='white',edgecolor='lightgrey',linewidth=1))