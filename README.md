# Accuweather web scraping

Welcome to my repository!

This is a web scraping project where I take the data from [Accuweather](https://accuweather.com/) and extract the information about the lowest and highest temperatures from the current day and the next nine days from Mexico's cities and some popular places.

The output CSV (or JSON) has the follow column structure:
* name: The name of the city or the popular place
* state: The name of the state where the place belongs to
* weather: This column is a list of dictionaries with the fileds:
    * day: Day in format MM/DD
    * low_temp: The lowest recorded (or predicted) temperature
    * high_temp: Same as above but the highest one

In this repo you can find one CSV file with the information of 32 different Mexico's states (the information was taken on May 30, 2024)