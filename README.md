# marketing-attribution
We have 4 different display advertising campaigns. We would like to evaluate how effective each advertising campaign is in generating sales

# Problem Definition
We have (anonymized) data which contains 10000 users who clicked on at least one of the display ads from campaigns A, B, C, or D. Purchase is indicated by the "Conversion" variable (i.e., equals 1 if there is purchase and 0 otherwise). The `Value` column indicates the revenue in dollars earned from each purchase. The cost per click for each campaign:
* A: 7
* B: 5
* C: 4
* D: 2

The order of clicks is as indicated in the data. Data example:

user_id | click_1 | click_2 | click_3 | click_4 | click_5 | Conversion | Value |
00001   |    a    |    b    |   NaN   |    d    |    NaN  |     0      |  0    |
00002   |    c    |    c    |    a    |    b    |    a    |     1      |  10   |

We would like to build a statistical attribution model to know:
* Which campaign is the most successful in terms of unit sales contributed?
* What is the return on investment for each campaign?
* How would you optimize the spend of a given budget of $1 million across all four campaigns?
