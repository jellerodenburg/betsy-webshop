# Betsy Webshop

Betsy Webshop is a database management system for a fictional marketplace where users can buy and sell products.

### Dependencies:
#### Python
Betsy Webshop was developed and tested with Python version 3.9.9

#### Rich
Betsy Webshop uses the 'Rich' Python library.  
See [Rich installation instructions](https://rich.readthedocs.io/en/stable/introduction.html) for system requirements and how to install Rich.  
SuperPy was developed and tested with Rich version 10.16.2 (latest stable version as of January 2022).

### Features summary:

| option                   | description                                       |
| ------------------------ | ------------------------------------------------- |
| [`buy`](#buy)            | adds a product to the list of bought products     |
| [`sell`](#sell)          | logs that a product has been sold                 |
| [`pull`](#pull)          | pulls products by expiration date                 |
| [`sales`](#sales)        | generates a sales report with revenue and profit  |
| [`inventory`](#inventory)| shows the inventory on a particular date          |
| [`setdate`](#setdate)    | sets the date that the program perceives as today |
| [`help`](#help)          | shows the argparse (built in) help message        |


# Demo
For a demonstration in your terminal, please run the main.py file:
```
python main.py
```

