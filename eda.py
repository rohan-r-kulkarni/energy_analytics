# %%
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
genfiles = pd.Series(os.listdir("clean_data"))
genfiles = genfiles[genfiles.str.contains("_gen.csv")].values

# %%
for i, genfile in enumerate(genfiles):
    
    name = genfile.split("_")[1]
    if name=="solar":
        continue #! the solar data is way too incomplete, disregard

    gen_data = pd.read_csv("clean_data/" + genfile, index_col=0)
    fig, ax = plt.subplots()

    plotstates = gen_data.columns
    plotstates = plotstates[np.isin(plotstates, relevstates)]
    if len(plotstates) == 0:
        for state in gen_data.columns:
            ax.plot(gen_data[state], label=state)
    else:
        for state in plotstates:
            ax.plot(gen_data[state], label=state)
    
    plt.title(name.capitalize() + " Generation by State, Monthly")

    fig.set_size_inches(20,10)
    ax.tick_params(axis='x', labelrotation=90)
    plt.legend()
    plt.xticks(np.arange(0, len(gen_data.index), 6), gen_data.index[::6])
    plt.xlabel("Time")
    plt.ylabel("Net Generation, Thousand MWh")
    plt.savefig("plots/eda/gross/" + name.lower() + "_gen_plot.png")
    #plt.show()



# %%
## do per capita by dividing by population over time

population = pd.read_csv("clean_data/clean_population.csv", index_col=0)

# %%
# the per capita graphs look very different!
for i, genfile in enumerate(genfiles):
    
    name = genfile.split("_")[1]
    if name=="solar":
        continue

    gen_data = pd.read_csv("clean_data/" + genfile, index_col=0)
    fig, ax = plt.subplots()

    plotstates = gen_data.columns
    plotstates = plotstates[np.isin(plotstates, relevstates)]


    common_dates = pd.DataFrame(gen_data.index).merge(pd.DataFrame(population.index), how="inner").values.flatten()
    gen_data_percapita = gen_data.loc[common_dates, :].divide(population.loc[common_dates, :])

    if len(plotstates) == 0:
        for state in gen_data_percapita.columns:
            ax.plot(gen_data_percapita[state], label=state)
    else:
        for state in plotstates:
            ax.plot(gen_data_percapita[state], label=state)
    
    plt.title(name.capitalize() + " Generation by State Per Capita, Monthly")

    fig.set_size_inches(20,10)
    ax.tick_params(axis='x', labelrotation=90)
    plt.legend()
    plt.xticks(np.arange(0, len(gen_data_percapita.index), 6), gen_data_percapita.index[::6])
    plt.xlabel("Time")
    plt.ylabel("Net Generation Per Capita, Thousand MWh")
    plt.savefig("plots/eda/percapita/" + name.lower() + "_gen_percapita_plot.png")
    #plt.show()


# %%


# %%
# Hypothesis: states with more fossil fuel consumption will have more electricity sold but harsher environmental impact
# There is a tradeoff between high cost of renewables; fossil fuels cheaper but have higher environmental cost
# since fossil fuels are cheaper, more electricity will be sold?

# Given time series consumption/generation of various fuels, we want to predict electricity sales + environmental impact

# Policy makers can use the model to predict how much electricity will be sold/environmental health in the future
# dependent on the trend of energy generation by sector
# how much they want to control that tradeoff is a user-defined parameter

# Why per capita? States with higher populations will have more electricity sold, more energy generated,
# more environmental impact just because they have more people. Remove this effect by normalizing by population

# Correlation vs. causation: obvious correlation between electricity sold (demand) and generated (supply).
# we can assert that environmental impact can be attributed to energy generation because that's the main source
# of pollution (hence the energy crisis) [not just new factories, more cows so more methane, etc.]


# %%


# %%



