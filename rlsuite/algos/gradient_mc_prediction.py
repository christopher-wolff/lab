import time

import numpy as np
import tensorflow as tf

from rlsuite import utils


def gradient_mc_prediction(
    env_fn,
    policy,
    value_fn,
    alpha=0.01,
    gamma=0.99,
    num_episodes=1000,
    seed=0,
    data_dir=None,
    log_freq=0,
):
    """Gradient Monte Carlo prediction for estimating a value function.

    Assumes a discrete action space.

    Args:
        env_fn (callable): A function that creates an instance of an environment.
        policy (callable): A function mapping from state space to a probability
            over actions.
        value_fn (tf.keras.Model): The value function model.
        alpha (float): The learning rate.
        gamma (float): The discount factor.
        num_episodes (int): The number of episodes to run.
        seed (int): A seed that fixes all randomness if possible.
        data_dir (str): Optional. A directory for storing experiment data.
        log_freq (int): The interval for logging to the console.

    Returns:
        The approximate optimal value function. This is a reference to the same
        object that was provided as the parameter `value_fn`.

    """
    # --- Parameter validation ---
    assert alpha >= 0, 'alpha must be non-negative'
    assert num_episodes > 0, 'num_episodes must be positive'

    # --- Initialization ---
    logger = utils.Logger(output_dir=data_dir, log_freq=log_freq)

    env = env_fn()
    num_actions = env.action_space.n

    env.seed(seed)
    np.random.seed(seed)

    start_time = time.time()

    # --- Main loop ---
    for i in range(num_episodes):
        # Initialize episode statistics
        episode_length = 0
        episode_return = 0

        # Roll out an episode
        experience = []
        state = env.reset()
        done = False
        while not done:
            action = np.random.choice(num_actions, p=policy(state))
            next_state, reward, done, _ = env.step(action)
            experience.append((state, reward))
            state = next_state
            episode_length += 1
            episode_return += reward

        G = 0
        for state, reward in reversed(experience):
            # Convert state to one-element batch
            state = state.reshape(1, -1)

            # Compute return
            G = gamma * G + reward

            # Compute gradient
            weights = value_fn.trainable_weights
            with tf.GradientTape() as tape:
                value = value_fn(state)
            grads = tape.gradient(value, weights)

            # Update weights
            for w, g in zip(weights, grads):
                dw = tf.reshape(alpha * (G - value) * g, w.shape)
                w.assign_add(dw)

        logger.store(
            iteration=i,
            episode_length=episode_length,
            episode_return=episode_return,
            grad_norm=tf.linalg.global_norm(grads).numpy().item(),
            time=time.time()-start_time,
        )

    # --- Deinitialization ---
    env.close()
    return value_fn
