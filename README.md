# A5.2 - Programming Exercise 2

## Overview

**TC470.10**

**A01793023 - Jorge Luis Arroyo Chavelas**

Here is the code to run a program to compute sales. The input data of this are a catalogue json and a sales json. The program reads both fles and merge them together to generate a table with the total sales on detail by product.

## Usage

The program is invoked with the following command

``` bash
python computeSales.py priceCatalogue.json salesRecord.json
```

``` bash
python3 computeSales.py ./TC2/TC1.ProductList.json ./TC1/TC1.Sales.json 

----------------------------------------------------
Product                        |        Total Sales
----------------------------------------------------
Rustic breakfast               |              63.96
Sandwich with salad            |              112.4
Raw legums                     |             359.31
Fresh stawberry                |             142.95
Pears juice                    |              58.47
Green smoothie                 |             388.96
Cuban sandwiche                |              203.5
Hazelnut in black ceramic bowl |             191.45
Tomatoes                       |              52.06
Plums                          |              76.72
Fresh blueberries              |             147.07
Corn                           |             257.45
French fries                   |              54.96
Ground beef meat burger        |              46.92
Cherry                         |               57.4
Homemade bread                 |             104.88
Smoothie with chia seeds       |              75.78
Peaches on branch              |              51.24
Pesto with basil               |              36.38
----------------------------------------------------
Grand Total                                 2481.86
----------------------------------------------------


Time elapsed: 0.0011019706726074219
```
