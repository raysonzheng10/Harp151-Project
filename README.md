# Harp151-Project
Rayson Zheng, Trinity Jin, Jomin Zhang

## Description
For our HARP 151 Final Project at Binghamton University, we decided to make a program that compiles movie reviews from 4 separate platforms: Youtube, Rotten Tomatoes, TMDB, and Google Reviews. These reviews were sorted by Vader Sentiment Analysis, a third party Python library. These were all compiled into a GUI made from Tkinter.

For Rotten Tomatoes and Google Reviews, we used Selenium to manually scrape their reviews. For TMDB and Youtube, we used their respective APIs to get their reviews.

To run the program, simply run main.py

## More Details
The repository is broken down into a few parts.
- The images folder contains images for icons and posters.
- The Scrapers folder contains the APIs/Selenium Webscrapers we built to grab the actual movie reviews.
- Prototype.py is a outdated file that represents our first prototype.
- tkint_helper.py is a helper file for main.py that manages some helper functions.
- VaderSentiment.py contains all Vader Sentiment related code.

## Dependencies
- vaderSentiment (https://github.com/cjhutto/vaderSentiment)
- Selenium
- Youtube API
- TMDB API
- Tkinter

## Future Improvements
- Better runtime; the webscraping for Rotten Tomatoes can probably be optimized, currently it runs quite slowly comapred to the other platforms
- Additional Platforms; including reviews on platforms such as Metacritic, IMDB, etc.
- Better GUI; more designated icons (ie. showing YouTube logo when looking at Youtube reviews)
- Better sorted reviews; include functions/methods to sort movie reviews by keywords, rating, length, etc.
- Better search functionality; creating some sort of autocomplete search, and or showing related results