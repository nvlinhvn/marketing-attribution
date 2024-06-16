# Marketing Attribution
We have 4 different display advertising campaigns. We would like to evaluate how effective each advertising campaign is in generating sales

# Problem Definition
We have (anonymized) data which contains 10000 users who clicked on at least one of the display ads from 4 different campaigns a, b, c, or d. Purchase is indicated by the "Conversion" variable (i.e., equals 1 if there is purchase and 0 otherwise). The `Value` column indicates the revenue in dollars earned from each purchase. The cost per click for each campaign:
* a: 2.75
* b: 2.5
* c: 3
* d: 3

The order of clicks is as indicated in the data. Data example:

<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: left;">
      <th>user_id</th>
      <th>click_1</th>
      <th>click_2</th>
      <th>click_3</th>
      <th>click_4</th>
      <th>click_5</th>
      <th>Conversion</th>
      <th>Value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>001</th>
      <td>a</td>
      <td>b</td>
      <td>NaN</td>
      <td>d</td>
      <td>NaN</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>002</th>
      <td>c</td>
      <td>c</td>
      <td>a</td>
      <td>b</td>
      <td>a</td>
      <td>1</td>
      <td>100</td>
    </tr>
  </tbody>
</table>
</div>


We would like to build a statistical attribution model to know:
* Which campaign is the most successful in terms of unit sales contributed?
* What is the return on investment for each campaign?
* How would you optimize the spend of a given budget of $1 million across all four campaigns?

# Hidden Markov Model

We model the user's click sequence as a Markov Chain, where each state represents a campaign or a conversion state. 
The Markov Chain captures the transition probabilities between different states, allowing us to analyze the user's journey from initial ad clicks to potential conversion.

![HMM](https://raw.githubusercontent.com/nvlinhvn/marketing-attribution/linh-dev/img/HMM.gif)

(Source: setosa.io)

### Building States
We define the following states in our Markov Chain:
* Campaign states: 'a', 'b', 'c', 'd'
* Null state: 'Null' (representing no click)
* Conversion states: 0 (no conversion), 1 (conversion)
Based on frequency, we can calculate the transition probabilities (when a state changes from one to another, or when a state remains). An example can be illustrated below:

![HMM](https://raw.githubusercontent.com/nvlinhvn/marketing-attribution/linh-dev/img/HMM.png)
  
