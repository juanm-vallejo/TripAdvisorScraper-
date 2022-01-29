# TripAdvisor Scraper

Get a database from TripAdvisor fast and easily. This scraper is designed for restaurants information, but not for the comments. It's suitable for such use cases as scraping TripAdvisor name, emails, addresses, prices, kitchen, punctuation and many more attributes of the restaurants on TripAdvisor.

# Input - TripAdvisor

You have to provide the link of the city you are interested as an input, and you can filter by kitchen speciality in the variable "typeFood", please check to write it just as in Tripadvisor. 


# Output --

You will get a CSV file with the following dictionary as columns:
```
{'CompanyName': , 
'Cusine': , 
'Importance': , 
'Address': , 
'PhoneNumber': , 
'Website': , 
'NumReviews': , 
'Overall': , 
'PriceRange': , 
'Prices': , 
'Puntuation': 
}
```
# How does the TripAdvisor Scraper Work?

The project was cretaed based in the [Requests library](https://docs.python-requests.org/en/latest/#), and the [Selenium](https://selenium-python.readthedocs.io/) library. It works with the two libraries to get the better of each.


This is one of the firsts scrappers I do, I am totally open to listen ideas, or any kind of criticism that can help me learn. 
