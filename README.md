# Marketing Attribution
We have 4 different display advertising campaigns. We would like to evaluate how effective each advertising campaign is in generating sales

# Problem Definition
We have (anonymized) data which contains 10000 users who clicked on at least one of the display ads from 4 different campaigns a, b, c, or d. Purchase is indicated by the "Conversion" variable (i.e., equals 1 if there is purchase and 0 otherwise). The `Value` column indicates the revenue in dollars earned from each purchase. The cost per click for each campaign:
* a: 7
* b: 5
* c: 4
* d: 2

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

![HMM](https://raw.githubusercontent.com/nvlinhvn/marketing-attribution/linh-dev/img/HMM.gif)


We would like to build a statistical attribution model to know:
* Which campaign is the most successful in terms of unit sales contributed?
* What is the return on investment for each campaign?
* How would you optimize the spend of a given budget of $1 million across all four campaigns?
