# Reinforcement Learning Suite

A collection of basic reinforcement learning algorithms and environments. All algorithms are self-contained and implemented using TensorFlow.

## Examples

The following is a list of Jupyter notebooks that run through usage examples of RL Suite.

- [Visualization](examples/visualization.ipynb)

## Algorithms

### Exact solution methods

- [Q-learning](rlsuite/algos/qlearning.py)
- [Sarsa](rlsuite/algos/sarsa.py)
- [Expected Sarsa](rlsuite/algos/expected_sarsa.py)
- [On-policy Monte Carlo control](rlsuite/algos/mc_control.py)
- [Policy evaluation](rlsuite/algos/policy_eval.py)

### Approximate solution methods

- [Gradient Monte Carlo Prediction](rlsuite/algos/gradient_mc_prediction.py)
- [Semi-gradient TD Prediction](rlsuite/algos/semi_gradient_td_prediction.py)
- [Least Squares Temporal Difference Learning](rlsuite/algos/lstd.py)
- [TD(lambda)](rlsuite/algos/td_lambda.py)
