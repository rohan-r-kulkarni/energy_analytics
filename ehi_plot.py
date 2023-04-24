
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os


# %%
#10 states to investigate
#! gas prices are not very relevant - depend a lot on macroeconomic factors
#! clean_coal deprecated, replicated by clean_Coal_gen file

# relevant states = highest producers + highest consumers
producers = {"Texas", "North Dakota", "Wyoming", "Pennsylvania", "Oklahoma", "West Virginia"}
consumers = {"Texas", "California", "New York", "Florida", "Ohio", "Pennsylvania"}
relevstates = list(producers.union(consumers))

# %%
genfiles = pd.Series(os.listdir("clean_data/resp"))
genfiles = genfiles[genfiles.str.contains("clean_")].values

# %%

for i, genfile in enumerate(genfiles):
    
    name = genfile.split("_")[1][:-4]
    if name=="revenue":
        continue 

    gen_data = pd.read_csv("clean_data/resp/" + genfile, index_col=0)
    fig, ax = plt.subplots()

    plotstates = gen_data.columns
    plotstates = plotstates[np.isin(plotstates, relevstates)]
    if len(plotstates) == 0:
        for state in gen_data.columns:
            ax.plot(gen_data[state], label=state)
    else:
        for state in plotstates:
            ax.plot(gen_data[state], label=state)
    
    plt.title(name.capitalize() + " Index by State, Monthly")

    fig.set_size_inches(20,10)
    ax.tick_params(axis='x', labelrotation=90)
    plt.legend()
    plt.xticks(np.arange(0, len(gen_data.index), 6), gen_data.index[::6])
    plt.xlabel("Time")
    plt.ylabel("Index Value")
    plt.savefig("plots/ehi_plots/" + name.lower() + "_plot.png")
    #plt.show()