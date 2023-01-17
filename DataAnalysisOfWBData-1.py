#!/usr/bin/env python
# coding: utf-8

import wbdata
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
 
#set up the countries I want
countries = ["CL","UY","BR"]
 
#set up the indicator I want (just build up the dict if you want more than one)
indicators = {'NY.GNP.PCAP.CD':'GNI per Capita',
              'SP.POP.TOTL':'Total Population',
              'EN.ATM.CO2E.SF.KT':'CO2 emissions from solid fuel consumption (kt)',
              'AG.LND.FRST.ZS':'Forest area (% of land area)',
              'AG.LND.ARBL.ZS':'Arable land (% of land area)',
              'AG.LND.AGRI.ZS':'Agricultural land (% of land area)'
             }

#grab indicators above for countires above and load into data frame
df = wbdata.get_dataframe(indicators, country=countries, convert_date=False)

#df is "pivoted", pandas' unstack fucntion helps reshape it into something plottable
dfu = df.unstack(level=0)

# a matplotlib plot of GNI per Capita with legend, labels and a title
dfu["GNI per Capita"].plot() 
plt.legend(loc='best') 
plt.title("GNI Per Capita ($USD, Atlas Method)") 
plt.xlabel('Date')
plt.ylabel('GNI Per Capita ($USD, Atlas Method')

# matplotlib plot of Total Population increase over time
dfu["Total Population"].plot() 
plt.legend(loc='best') 
plt.title("Population") 
plt.xlabel('Date') 
plt.ylabel('Change in population')

#slicing of data based on country
brazil=df.loc['Brazil']
chile=df.loc['Chile']
uruguay=df.loc['Uruguay']

#Bar plot 
fig, ax = plt.subplots()

# Add a bar for the Brazil "CO2 emissions from solid fuel consumption (kt)" column mean/std
ax.bar("Brazil",
       brazil["CO2 emissions from solid fuel consumption (kt)"].mean(),
       yerr=brazil["CO2 emissions from solid fuel consumption (kt)"].std()
      )

# Add a bar for the Chile "CO2 emissions from solid fuel consumption (kt)" column mean/std
ax.bar("Chile",
       chile["CO2 emissions from solid fuel consumption (kt)"].mean(),
       yerr=chile["CO2 emissions from solid fuel consumption (kt)"].std()
      )

# Label the y-axis
ax.set_ylabel("CO2 emissions from solid fuel consumption (kt)")

plt.show()

#scatter plot to show correlation
fig, ax = plt.subplots()

# Add data: "co2", "relative_temp" as x-y, index as color
ax.scatter(brazil["CO2 emissions from solid fuel consumption (kt)"],
           brazil["Total Population"],
           color='b'
          )
ax.scatter(chile["CO2 emissions from solid fuel consumption (kt)"],
           chile["Total Population"],
           color='r'
          )
# Set the x-axis label to "CO2 (ppm)"
ax.set_xlabel("CO2 emissions from solid fuel consumption (kt)")

# Set the y-axis label to "Relative temperature (C)"
ax.set_ylabel("Total Population")

plt.show()

# Change in Forest area of Brazil
brazil["Forest area (% of land area)"].plot().invert_xaxis() 
plt.legend(loc='best') 
plt.title("Change in Forest area of Brazil") 
plt.xlabel('Date')
plt.ylabel('Forest area (% of land area)')
plt.show()

#plot of change in forests over time for all three countries
dfu["Forest area (% of land area)"].plot() 
plt.legend(loc='best') 
plt.title("Change in Forest of all three countries") 
plt.xlabel('Date')
plt.ylabel('Forest area (% of land area)')
plt.show()

# generating pairwise correlation for brazil
corr = brazil.corr()

# Displaying dataframe as an heatmap 
# with diverging colourmap as coolwarm
plt.figure(figsize = (15,8))
ax = sns.heatmap(corr, 
                 annot = True,
                 square=True,
                 cmap ='coolwarm'
                )
ax.set_xticklabels(ax.get_xticklabels(),
                   rotation = 90
                  )
plt.show()

# Emphesis on correlation between "CO2 emissions from solid fuel consumption (kt)" and "Forest area (% of land area)"
sns.lmplot(x="CO2 emissions from solid fuel consumption (kt)",
           y="Forest area (% of land area)",
           data=brazil,
           ci=None
          )
plt.show()