# COMCscraper

# Jared Randall

This is package has been built to scrape the website, Check Out My Cards (COMC). COMC is an online marketplace for buying and selling sports cards, trading cards, and other collectibles.

This package is strictly built for end users who wish to scrape data for personal use.

Please be considerate of COMC servers when using COMCscraper.

# Installation
---

You can install the package by entering the following command in terminal:

<code> pip install COMCscraper</code>

Then import the module using this function:

<code> import COMCscraper as comc</code>
---

# User-End Functions

---

### getSportsCards(sport, sort, attributes) ###

Returns a dataframe containing 100 results based on the sport, sort and attributes provided.

* Card: Full Title of the card as listed on COMC (E.g. 2015-16 Upper Deck - UD Canvas #C270)
* Year: Year or Season in which card was produced (E.g. 2015-16) 
* Player: Name of the Player as listed on COMC  (E.g. Program of Excellence - Connor McDavid)
* Player (Clean): Name of the player striped of other dimensions (E.g. Connor McDavid)
* Lowest Price: The lowest price the card is being sold for on COMC (E.g. 2230.28)
* Season: Different from Year dimension to more closly align with COMC's filtering (E.g. 2015)
* Serial #/: If applicable, shows the number of cards produced for cards that are serial numbered (E.g. 10)
* Set: Official name of set including year and brand (E.g. 2015-16 Upper Deck)
* Brand: Producer or product line of the set (E.g. Upper Deck)
* Card #: Card Number within Set; either Base or Subset (E.g. C270)
* Subset: Name of subset; value of 'Base' if part of main set (E.g. UD Canvas)
* Attributes: If attributes value is passed, then column contains attributes used in search (E.g. RC)

Example:

getSportsCards("hockey", "sl", "RC")

This example would search lowest priced ('sl') hockey ('hockey') cards featuring rookies ('RC').

---

### getTradingCards("POKER", "", "") ###

Returns a dataframe containing 100 results based on the trading card, sort and attributes provided.

* Card: Full Title of the card as listed on COMC (E.g. 2015-16 Upper Deck - UD Canvas #C270)
* Year: Year or Season in which card was produced (E.g. 2015-16) 
* Title: Name of the Poker player or character as listed on COMC  (E.g. Program of Excellence - Connor McDavid)
* Title (Clean): Name of the player or character striped of other dimensions (E.g. Connor McDavid)
* Lowest Price: The lowest price the card is being sold for on COMC (E.g. 2230.28)
* Season: Different from Year dimension to more closly align with COMC's filtering (E.g. 2015)
* Serial #/: If applicable, shows the number of cards produced for cards that are serial numbered (E.g. 10)
* Set: Official name of set including year and brand (E.g. 2015-16 Upper Deck)
* Brand: Producer or product line of the set (E.g. Upper Deck)
* Card #: Card Number within Set; either Base or Subset (E.g. C270)
* Subset: Name of subset; value of 'Base' if part of main set (E.g. UD Canvas)
* Attributes: If attributes value is passed, then column contains attributes used in search (E.g. RC)

Example:

getTradingCards("Star Wars", "sd", "AUTO")

This example would search autographed ('AUTO') Star Wards ('Star Wars') cards with the largest discount ('sd').

# Comments, Questions, or Concerns.

---

If you should have any comments, questions or concerns about COMCscraper, please do not hesitate to email me at jaredtroyrandall@gmail.com.

If you have any requests, please feel free to send them my way as well :)