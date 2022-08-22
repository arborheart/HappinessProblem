# Importing necessary packages.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Opening necessary files
year15 = pd.read_excel(r"C:\Users\lynne\Pictures\happiness\2015.xlsx")
year16 = pd.read_excel(r"C:\Users\lynne\Pictures\happiness\2016.xlsx")
year17 = pd.read_excel(r"C:\Users\lynne\Pictures\happiness\2017.xlsx")
year18 = pd.read_excel(r"C:\Users\lynne\Pictures\happiness\2018.xlsx")
year19 = pd.read_excel(r"C:\Users\lynne\Pictures\happiness\2019.xlsx")
suicide = pd.read_excel(r"C:\Users\lynne\Pictures\happiness\suicide.xlsx")

# Joining happiness statistics into one frame.
# Used inner join to make sure that only countries with data for each year were included.
merged_1516 = pd.merge(year15, year16, on="Country")
merged_1718 = pd.merge(year17, year18, on="Country")
merged_pre19 = pd.merge(merged_1516, merged_1718, on="Country")
merged_happiness = pd.merge(merged_pre19, year19, on="Country")

# Remove any columns that aren't dealing with happiness score or country.
merged_happiness = merged_happiness.loc[:, [x for x in merged_happiness.columns if x.startswith(('Score', 'Country'))]]

# Properly label columns by year.
merged_happiness = merged_happiness.rename(columns={"Score_x_x": "Happiness_2015", "Score_y_x": "Happiness_2016", "Score_x_y": "Happiness_2017", "Score_y_y": "Happiness_2018", "Score": "Happiness_2019"})

# Moving onto the suicide data...
# Properly label columns.
suicide = suicide.rename(columns={2015: "Suicide_2015", 2016: "Suicide_2016", 2017: "Suicide_2017", 2018: "Suicide_2018", 2019: "Suicide_2019"})

# Drop all columns with data earlier than 2015. Drop all rows that show only male or only female data.
suicide = suicide.iloc[:, :7]
suicide = suicide[suicide["Sex"].str.contains("Male|Female") == False]

# The standard deviation is present in each column of the suicide data, which will prevent us from doing calculations on it.
# Splitting those columns...
suicide[["Suicide_2015", "SD_2015"]] = suicide["Suicide_2015"].str.split(expand=True)
suicide[["Suicide_2016", "SD_2016"]] = suicide["Suicide_2016"].str.split(expand=True)
suicide[["Suicide_2017", "SD_2017"]] = suicide["Suicide_2017"].str.split(expand=True)
suicide[["Suicide_2018", "SD_2018"]] = suicide["Suicide_2018"].str.split(expand=True)
suicide[["Suicide_2019", "SD_2019"]] = suicide["Suicide_2019"].str.split(expand=True)

# Using inner join to merge all data based on shared countries.
merged_all = pd.merge(merged_happiness, suicide, on="Country")

# Making sure all data is of the appropriate type.
merged_all = merged_all.astype({'Suicide_2015': 'float', 'Suicide_2016': 'float', 'Suicide_2017': 'float', 'Suicide_2018': 'float', 'Suicide_2019': 'float', 'Happiness_2015': 'float', 'Happiness_2016': 'float', 'Happiness_2017': 'float', 'Happiness_2018': 'float', 'Happiness_2019': 'float'})


# Ensuring all data is present...
# print(merged_all.isnull().sum())
# print(np.where(merged_all == ''))
# Both return nothing of concern when run. We're all set!

# The data has all been merged and cleaned. Now, onto the actual calculations.
# As a reminder, we're wondering what correlation there is between happiness score and suicide, if any.

# Making columns for the averages of the relevant data.
merged_all["Suicide_Average"] = sum([merged_all.Suicide_2015, merged_all.Suicide_2016, merged_all.Suicide_2017, merged_all.Suicide_2018, merged_all.Suicide_2019])/5
merged_all["Happiness_Average"] = sum([merged_all.Happiness_2015, merged_all.Happiness_2016, merged_all.Happiness_2017, merged_all.Happiness_2018, merged_all.Happiness_2019])/5

# Calculating their correlation, mean, and standard deviation!
print("Correlation:", merged_all.Happiness_Average.corr(merged_all.Suicide_Average))
print("Average Happiness Score:", np.mean(merged_all.Happiness_Average))
print("Happiness Score Standard Deviation:", np.std(merged_all.Happiness_Average))
print("Average Rate of Suicide:", np.mean(merged_all.Suicide_Average))
print("Suicide Rate Standard Deviation:", np.std(merged_all.Suicide_Average))

# Their correlation is -.14, but let's take a look at a visualization...
# Setting graph to be a scatter plot, setting data points to be gray for contrast.
plt.scatter(merged_all.Happiness_Average, merged_all.Suicide_Average, color="grey")

# Calculating trend line.
z = np.polyfit(merged_all.Happiness_Average, merged_all.Suicide_Average, 1)
p = np.poly1d(z)

# Labeling.
plt.title('Correlation Between Happiness Score and Suicide Rate')
plt.xlabel('Happiness Score')
plt.ylabel('Suicide Rate')

# Setting axes to start at 0 for clarity of data.
plt.xlim([0, max(merged_all.Happiness_Average)+1])
plt.ylim([0, max(merged_all.Suicide_Average)+1])

# And there we have it!
plt.plot(merged_all.Happiness_Average, p(merged_all.Happiness_Average))
plt.show()
