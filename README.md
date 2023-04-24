# Environmental Impact and Industrial Revenue vs. Energy Generation
A Predictive Analytics Approach On Time Series

We investigate per capita energy generation, key environmental health factors (water quality, air quality, drought severity), and per capita revenue from electricity sales monthly time series data from 2001-2022 for certain states in the United States, attempting to illuminate how industrial patterns have affected economic development and/or disturbed local environments.

How to use this repository:
- The raw data is in the ```raw_data``` and ```env_health_index``` directories, imported CSVs from various sources.
- The ```data_cleaning``` directory contains three files:
  - ```energy_cleaning.py``` cleans the energy generation data by sector (coal, biomass, wind, etc.). This is saved in ```clean_data```.
  - ```resp_cleaning.py``` cleans the air, water, and drought data for use for the Environmental Health Index (EHI) and the energy revenue data for use in the response variable creation. This is saved in ```clean_data/resp```.
- EDA and visualization of the data is done with ```eda.py``` and ```ehi_plot.py``` and saved in the ```plots``` directory.
- STL decompositions of the time series is done with ```stl.R``` and saved in ```plots```.
- The main models are created and run in ```reg_models.R```, with results being saved in ```plots``` and ```results```.

Built with ```R```, ```python```, and ```jupyter```.

Rohan R. Kulkarni, Rojeen Farkhoor, Jasmine Cui, Spencer Austin
Prof. Adam Elmachtoub
Business Analytics Final Project - Spring 2023
