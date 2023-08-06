import random
from typing import Any, Generator, Optional, Sequence

import numpy as np
from scipy.special import softmax


__all__ = ['Arm', 'Loss', 'Advice', 'Player', 'exp4']


Arm = Any
ExpertAdvice = Sequence[float]
Advice = Sequence[ExpertAdvice]
Expert = Any
Loss = float
Player = Generator[
    Optional[Arm],                  # Yield Arm to have pulled.
    tuple[Optional[Loss], Advice],  # Receive loss and advice.
    None,
]


def exp4(noise_coeff: float = 0) -> Player:
    """Implements exp4 as described in https://banditalgs.com/2016/10/14/exp4/

    Arguments:
      - noise_coeff: Called γ in the literature.

    Yields:
      - Arm to pull.

    Recieves:
      - Tuple of loss due to previous arm pull (initially None) and
        expert advice (arm weights).
      - Advice is a num_experts × num_arms matrix (rows should sum to 1).
    """
    player = _exp4(noise_coeff)
    next(player)  # Initialize co-routine.
    return player


def _exp4(noise_coeff: float) -> Player:
    temp = 0  # E₀*
    arm = expert = expert_weights = prev_advice = None

    while True:
        loss, advice = yield arm
        advice = np.array(advice)
        num_experts, num_arms = advice.shape

        temp += advice.max(axis=0).sum()          # Eₜ*

        # Update weights.
        if expert_weights is None:
            expert_weights = np.ones(num_experts)        # Uniform weights.
        else:
            assert 0 <= loss <= 1

            # Compute Expert rewards.
            arm_prob = expert_weights[expert] * advice[expert, arm]
            rewards = np.zeros(num_arms)
            rewards[arm] = (1 - loss) / arm_prob
            rewards = prev_advice @ rewards
            rewards *= np.sqrt(np.log(num_experts) / temp)  # η·rewards.

            # Exponential weighting update.
            expert_weights = softmax(rewards + np.log(expert_weights))

        # Sample arm and remember previous advice.
        expert = random.choices(range(num_experts), weights=expert_weights)[0]
        arm = random.choices(range(num_arms), weights=advice[expert])[0]
        prev_advice = advice
