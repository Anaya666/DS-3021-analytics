#lab dataset2.py
import pandas as pd 
import numpy as np 

hotel_data = pd.read_csv("/Users/anayanath/rainbow/DS-3021-analytics/data/hotels.csv")
print(hotel_data)

## Question 1:
#What is the relationship between lead time - that is, how early a guest books their stay before check in date, and 
#liklihood of cancellation 

lead_max = hotel_data["lead_time"].max()
print(lead_max)
lead_min = hotel_data["lead_time"].min()
print(lead_min)
#Pseudocode
#1-group by lead times 
#2-group by cancellation liklihood where 0 means not cancelled and 1 means cancelled 
#3-within each lead time, compute the number and percentage of cancellations (0s)
#4-calculate the lead time range with the highest cancellation liklihood 

#step 1 
hotel_data["lead_time"] = pd.to_numeric(hotel_data["lead_time"])
bins = [-1, 100, 200, 300, 400, 500, 600, 700, 800]
labels = ["0-100 days", "100-200 days", "200-300 days", "300-400 days", "400-500 days", "500-600 days", "600-700 days", "700-800 days"]
hotel_data["lead_time1"] = pd.cut(hotel_data["lead_time"], bins=bins, labels=labels)
sorted_output = hotel_data[["lead_time", "lead_time1"]].sort_values(by="lead_time", ascending=True)
print(sorted_output.tail(10))

lead_time_counts = hotel_data["lead_time1"].value_counts()
print(lead_time_counts)
#the result gives the number of bookings made within the range of labeled dates 

#step 2 
is_canceled_counts = hotel_data.groupby("is_canceled").size()
print(is_canceled_counts)

#step 3 
lead_canceled_table = hotel_data.groupby(["lead_time1", "is_canceled"]).size().unstack()
print(lead_canceled_table)

#calculating the percent of cancellations within each lead time day range 
lead_canceled_percent = lead_canceled_table.div(lead_canceled_table.sum(axis=1), axis=0) * 100

# Display the percentage table
print(lead_canceled_percent)

#step 4 
highest_canceled_lead_time = lead_canceled_percent.idxmax(axis=1)
print(highest_canceled_lead_time)
#Analysis 
#This data indicates that lead times between 0-100 days, 200-300 days, and 700-800 days 
#likely to not cancel 
#amongst the remaining lead times, the lead time for which a guest is most liklely to cancel is indicated by 
#100% which is 600-700 days before they check into the hotel 



#Another question I want to explore in this dataset is:
#Question 2: Which meal plans are most popular among guests from different countries 

#Pseudocode
#1-group dataset by meal plans 
#2-group dataset by guests from each country 
#3-within each country, compute the percentage of meal plans 
#4-find the most common meal plan per country 

#step 1 
#printing unique values within meal:
print(hotel_data["meal"].unique())
meal_counts = hotel_data.groupby("meal").size().reset_index(name="count")
print(meal_counts)

#step 2 
country_counts = hotel_data.groupby("country").size().reset_index(name="count")
print(country_counts)

#step 3 
meal_country_counts = hotel_data.groupby(["country", "meal"]).size().reset_index(name="count")
print(meal_country_counts)
total_country_counts = meal_country_counts.groupby("country")["count"].transform("sum")
meal_country_counts["percentage"] = (meal_country_counts["count"] / total_country_counts) * 100
print("\nMeal plan percentages within each country:")
print(meal_country_counts.sort_values(by=["country", "percentage"], ascending=[True, False]).head(20))





