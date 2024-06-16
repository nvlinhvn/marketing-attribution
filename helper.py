from typing import Dict, Tuple
import numpy as np
import pandas as pd

def calculate_removal_effects(transition_matrix: pd.DataFrame, cost_per_click: Dict[str, float]) -> Dict[str, float]:
    """
    Calculate the removal effect of each campaign.

    Args:
        transition_matrix (pd.DataFrame): The transition probability matrix.
        cost_per_click (Dict[str, float]): A dictionary mapping campaign names to their cost per click.

    Returns:
        Dict[str, float]: A dictionary mapping campaign names to their removal effects.
    """
    removal_effects_dict = {}
    
    for campaign in cost_per_click.keys():
        modified_matrix = transition_matrix.copy()
        
        # Set the transition probabilities from the removed campaign to other states to 0
        modified_matrix.loc[campaign, :] = 0
        
        # Set the transition probabilities from other states to the removed campaign to 0
        modified_matrix.loc[:, campaign] = 0
        
        # Set the transition probability from the removed campaign to itself to 1
        modified_matrix.loc[campaign, campaign] = 1
        
        # Calculate the conversion probability without the removed campaign
        Q = modified_matrix.iloc[:-2, :-2]
        R = modified_matrix.iloc[:-2, -2:]
        try:
            F = np.linalg.inv(np.eye(Q.shape[0]) - Q)
        except np.linalg.LinAlgError:
            F = np.linalg.pinv(np.eye(Q.shape[0]) - Q)  # Use pseudo-inverse if matrix is singular
        conversion_prob_without_campaign = np.sum(F @ R)
        
        # Calculate the removal effect
        removal_effect = transition_matrix.loc[1, 1] - conversion_prob_without_campaign
        removal_effects_dict[campaign] = removal_effect[1]
    
    return removal_effects_dict


def calculate_attribution(removal_effects: Dict[str, float], total_conversions: int, total_revenue: float) -> Tuple[Dict[str, float], Dict[str, float]]:
    """
    Calculate the attribution of conversions and revenue for each campaign.

    Args:
        removal_effects (Dict[str, float]): A dictionary mapping campaign names to their removal effects.
        total_conversions (int): The total number of conversions.
        total_revenue (float): The total revenue.

    Returns:
        Tuple[Dict[str, float], Dict[str, float]]: A tuple containing two dictionaries:
            - A dictionary mapping campaign names to their attributed conversions.
            - A dictionary mapping campaign names to their attributed revenue.
    """
    total_removal_effect = sum(removal_effects.values())
    attribution_conversions = {k: v / total_removal_effect * total_conversions for k, v in removal_effects.items()}
    attribution_revenue = {k: v / total_removal_effect * total_revenue for k, v in removal_effects.items()}
    return attribution_conversions, attribution_revenue


def calculate_roi(attribution_revenue: Dict[str, float], total_cost_by_campaign: Dict[str, float]) -> Dict[str, float]:
    """
    Calculate the ROI (Return on Investment) for each campaign.

    Args:
        attribution_revenue (Dict[str, float]): A dictionary mapping campaign names to their attributed revenue.
        total_cost_by_campaign (Dict[str, float]): A dictionary mapping campaign names to their total cost.

    Returns:
        Dict[str, float]: A dictionary mapping campaign names to their ROI.
    """
    roi = {}
    for campaign, revenue in attribution_revenue.items():
        roi[campaign] = (revenue - total_cost_by_campaign[campaign]) / total_cost_by_campaign[campaign]
    return roi
