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
* Campaign states: `a`, `b`, `c`, `d`
* Null state: `Null` (representing no click)
* Conversion states: 0 (no conversion), 1 (conversion)

Based on frequency, we can calculate the transition probabilities (when a state changes from one to another, or when a state remains). An example can be illustrated below:

![HMM](https://raw.githubusercontent.com/nvlinhvn/marketing-attribution/linh-dev/img/HMM.png)

# Removal Effects
To determine the contribution of each campaign to the conversions and revenue, we calculate the removal effect of each campaign. The removal effect measures the impact of removing a campaign from the Markov Chain on the overall conversion probability.
For each campaign, we remove it from the Markov Chain by setting the transition probabilities from the removed campaign to other states and from other states to the removed campaign to 0. We then calculate the conversion probability without the removed campaign and compare it to the original conversion probability. The difference between the two probabilities gives us the removal effect of that campaign.

Let $P$ be the transition probability matrix of the Markov Chain, and $P_{\text{removed}}^{(i)}$ be the modified transition probability matrix with campaign $i$ removed.
The conversion probability with all campaigns is given by:
$$P(\text{conversion}) = P(X_t = 1 | X_0 = \text{start})$$
The conversion probability without campaign $i$ is given by:
$$P(\text{conversion}{\text{removed}}^{(i)}) = P(X_t = 1 | X_0 = \text{start}, P{\text{removed}}^{(i)})$$
The removal effect of campaign $i$ is calculated as:
$$\text{Removal Effect}(i) = P(\text{conversion}) - P(\text{conversion}_{\text{removed}}^{(i)})$$
where:

$X_t$ represents the state of the Markov Chain at time step $t$
$X_0$ represents the initial state of the Markov Chain
$P(X_t = 1 | X_0 = \text{start})$ denotes the probability of reaching the conversion state (state 1) starting from the initial state
$P(X_t = 1 | X_0 = \text{start}, P_{\text{removed}}^{(i)})$ denotes the probability of reaching the conversion state starting from the initial state, with campaign $i$ removed from the Markov Chain

# Revenue Attribution
Based on removal effects, we attribute the total conversions and revenue to each campaign. The attribution is proportional to the removal effect of each campaign. We calculate the attributed conversions and revenue for each campaign based on their relative contribution to the total removal effect.

# Budget Optimization
To optimize the budget allocation across the campaigns, we formulate an optimization problem using linear programming. The objective is to maximize the total attributed revenue while satisfying the budget constraints.
The optimization problem is set up as follows:

Decision variables: x_a, x_b, x_c, x_d (representing the budget allocation for each campaign)
Objective function: Maximize the total attributed revenue
Constraints:

Total budget constraint: x_a + x_b + x_c + x_d <= total_budget
Non-negativity constraints: x_a, x_b, x_c, x_d >= 0
Removal effect constraints: Ensure that the attributed revenue for each campaign is consistent with the removal effects

By solving this optimization problem, we obtain the optimal budget allocation for each campaign that maximizes the total attributed revenue while respecting the budget constraints and considering the removal effects.
