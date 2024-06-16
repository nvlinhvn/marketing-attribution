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

# Markov Chain

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

The training state based on frequency can give us transition matrix
![HMM](https://raw.githubusercontent.com/nvlinhvn/marketing-attribution/linh-dev/img/transition_matrix.png)

# Removal Effects
To determine the contribution of each campaign to the conversions and revenue, we calculate the removal effect of each campaign. The removal effect measures the impact of removing a campaign from the Markov Chain on the overall conversion probability.
For each campaign, we remove it from the Markov Chain by setting the transition probabilities from the removed campaign to other states and from other states to the removed campaign to 0. We then calculate the conversion probability without the removed campaign and compare it to the original conversion probability. The difference between the two probabilities gives us the removal effect of that campaign.

Let $P$ be the transition probability matrix of the Markov Chain, and $P_{\text{removed}}^{(i)}$ be the modified transition probability matrix with campaign $i$ removed.
The conversion probability with all campaigns is given by:
$$P(\text{conversion}) = P(X_t = 1 | X_0 = \text{start})$$
The conversion probability without campaign $i$ is given by:
$$P(\text{conversion}{\text{ removed}}^{(i)}) = P(X_t = 1 | X_0 = \text{start}, P{\text{removed}}^{(i)})$$
The removal effect of campaign $i$ is calculated as:
$$\text{Removal Effect}(i) = P(\text{conversion}) - P(\text{conversion}_{\text{removed}}^{(i)})$$
where:

* $X_t$ represents the state of the Markov Chain at time step $t$
* $X_0$ represents the initial state of the Markov Chain
* $P(X_t = 1 | X_0 = \text{start})$ denotes the probability of reaching the conversion state (state 1) starting from the initial state
* $P(X_t = 1 | X_0 = \text{start}, P_{\text{removed}}^{(i)})$ denotes the probability of reaching the conversion state starting from the initial state, with campaign $i$ removed from the Markov Chain

The removal effects of each campaign: 

*`a`: -0.137 (Removing campaign `a` would decrease the conversion probability by 13.7%)
*`b`: -0.135 (Removing campaign `b` would decrease the conversion probability by 13.5%)
*`c`: -0.143 (Removing campaign `c` would decrease the conversion probability by 14.3%)
*`d`: -0.144 (Removing campaign `d` would decrease the conversion probability by 14.4%)

# Revenue Attribution
Based on removal effects, we attribute the total conversions and revenue to each campaign. The attribution is proportional to the removal effect of each campaign. We calculate the attributed conversions and revenue for each campaign based on their relative contribution to the total removal effect.

Let $\text{RE}(i)$ be the removal effect of campaign $i$, $\text{Total Conversions}$ be the total number of conversions, and $\text{Total Revenue}$ be the total revenue.
The attributed conversions for campaign $i$ is given by:
$$\text{Attributed Conversions}(i) = \frac{\text{RE}(i)}{\sum_{j=1} \text{RE}(j)} \times \text{Total Conversions}$$
The attributed revenue for campaign $i$ is given by:
$$\text{Attributed Revenue}(i) = \frac{\text{RE}(i)}{\sum_{j=1} \text{RE}(j)} \times \text{Total Revenue}$$
where:

* $\text{RE}(i)$ represents the removal effect of campaign $i$
* $\sum_{j=1} \text{RE}(j)$ represents the sum of removal effects of all campaigns
* $\frac{\text{RE}(i)}{\sum_{j=1} \text{RE}(j)}$ represents the proportion of the removal effect of campaign $i$ relative to the total removal effect of all campaigns
* $\text{Total Conversions}$ represents the total number of conversions across all campaigns
* $\text{Total Revenue}$ represents the total revenue generated across all campaigns

The revenue attribution of each campaign: 

*`a`: 21567 (~24%)
*`b`: 21210 (~24%)
*`c`: 22463 (~26%)
*`d`: 22691 (~26%)

# Budget Optimization
To optimize the budget allocation across the campaigns, we formulate an optimization problem using linear programming. The objective is to maximize the total attributed revenue while satisfying the budget constraints.

Assuming retun on investment of each campaign is constant, the optimization problem is set up as follows:

Decision variables: $\mathbf{x} = [x_a, x_b, x_c, x_d]^T$ (representing the budget allocation for each campaign)
Objective function: Maximize the total attributed revenue
Constraints:

* Total budget constraint: x_a + x_b + x_c + x_d = total_budget
* Non-negativity constraints: all x_a, x_b, x_c, x_d > 0
* Removal effect constraints: Ensure that the attributed revenue for each campaign is consistent with the removal effects

Let $\mathbf{x} = [x_a, x_b, x_c, x_d]^T$ be the vector of decision variables representing the budget allocation for each campaign, and $\mathbf{r} = [r_a, r_b, r_c, r_d]^T$ be the vector of attributed revenue per unit budget for each campaign ( ($\mathbf{r} = (1 + \text{return on investment (%) }) \odot \text{cost}$)), and $\mathbf{RE} = [\text{RE}(a), \text{RE}(b), \text{RE}(c), \text{RE}(d)]^T$ be the vector of removal effects for each campaign, and $\mathbf{AR} = [\text{AR}(a), \text{AR}(b), \text{AR}(c), \text{AR}(d)]^T$ be the vector of attributed revenue for each campaign.
The optimization problem can be formulated as follows:
Objective function:
$$\text{Maximize: } \mathbf{r}^T \mathbf{x}$$
Subject to:

* Total budget constraint: $$ \mathbf{1}^T \mathbf{x} \eq \text{total budget}$$
* Removal effect constraints: $$\mathbf{AR} = \frac{\mathbf{RE}}{\mathbf{1}^T \mathbf{RE}} \odot (\mathbf{r}^T \mathbf{x})$$

The optimization problem can be solved using linear programming techniques, to obtain the optimal budget allocation $\mathbf{x}^*$ that maximizes the total attributed revenue while satisfying the constraints.
