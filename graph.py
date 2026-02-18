import matplotlib.pyplot as plt
import numpy as np

colors = ['green','red','orange']
def plot(results,vals):
    plt.bar(results,vals,color=colors)
    plt.title("Results")
    plt.show()

def graph_money(money,len):
    x = range(len)
    values = np.array(money)
    plt.plot(x,np.where(values>0,values,np.nan),color='green')
    plt.plot(x,np.where(values<=0,values,np.nan),color = 'red')
    plt.axhline(0)
    plt.xlabel("Game")
    plt.ylabel("Net Total")
    plt.title('Net Totals Over Time')
    plt.show()