import random
import json
import os
from scrapers.youtube_scraper import fetch_youtube_trends
from scrapers.twitter_scraper import fetch_twitter_trends

class RLScraperAgent:
    """
    A Reinforcement Learning Agent using a Markov Decision Process (MDP) 
    via Q-learning to self-supervise the content scraping strategy.
    """
    def __init__(self, actions, state_space, q_file='database/scraper_q_table.json'):
        self.actions = actions
        self.state_space = state_space
        self.q_file = q_file
        self.epsilon = 0.2  # Exploration rate: 20% chance to try random action
        self.alpha = 0.1    # Learning rate
        self.gamma = 0.9    # Discount factor
        
        self.q_table = self.load_q_table()

    def load_q_table(self):
        if os.path.exists(self.q_file):
            try:
                with open(self.q_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Could not load Q-table: {e}")
        
        # Initialize Q-table: Q[state][action] = 0.0
        q_table = {}
        for s in self.state_space:
            q_table[s] = {a: 0.0 for a in self.actions}
        return q_table

    def save_q_table(self):
        # Ensure directory exists
        os.makedirs(os.path.dirname(self.q_file), exist_ok=True)
        with open(self.q_file, 'w') as f:
            json.dump(self.q_table, f)

    def choose_action(self, state):
        # Epsilon-greedy action selection
        if random.uniform(0, 1) < self.epsilon:
            return random.choice(self.actions) # Explore
        else:
            # Exploit best known action
            q_values = self.q_table[state]
            max_q = max(q_values.values())
            best_actions = [a for a, q in q_values.items() if q == max_q]
            return random.choice(best_actions)

    def update_q_table(self, state, action, reward, next_state):
        current_q = self.q_table[state][action]
        max_next_q = max(self.q_table[next_state].values())
        
        # Bellman equation for Q-learning
        new_q = current_q + self.alpha * (reward + self.gamma * max_next_q - current_q)
        self.q_table[state][action] = new_q
        self.save_q_table()

def get_state(num_results):
    """Discretize the number of results into a state for the MDP."""
    if num_results == 0: return 'Empty'
    if num_results < 5: return 'Low'
    if num_results < 15: return 'Medium'
    return 'High'

def execute_action(action, keyword):
    """Execute the scraping action and return the results."""
    try:
        if action == 'youtube_base':
            return fetch_youtube_trends(keyword, max_results=15)
        elif action == 'youtube_deep':
            return fetch_youtube_trends(f"{keyword} tutorial analysis", max_results=15)
        elif action == 'twitter_base':
            return fetch_twitter_trends(keyword, max_results=15)
        elif action == 'twitter_latest':
            return fetch_twitter_trends(f"{keyword} news", max_results=15)
    except Exception as e:
        print(f"Action {action} failed: {e}")
        
    return []

def rl_supervised_scrape(keyword, steps=3):
    """
    Runs the RL agent through a few MDP steps to self-supervise
    the scraping process and maximize valuable content retrieval.
    """
    actions = ['youtube_base', 'youtube_deep', 'twitter_base', 'twitter_latest']
    state_space = ['Empty', 'Low', 'Medium', 'High']
    
    agent = RLScraperAgent(actions, state_space, q_file='database/scraper_q_table.json')
    
    # The initial state assumes we start with no prior knowledge for this scrape session
    current_state = 'Empty'
    all_results = []
    
    print(f"\n--- Starting RL Supervised Scraping for: '{keyword}' ---")
    
    for step in range(steps):
        # 1. Agent chooses an action based on the current state
        action = agent.choose_action(current_state)
        print(f"[RL Agent] Step {step+1}: State='{current_state}', Chosen Action='{action}'")
        
        # 2. Execute the action (Scraping)
        results = execute_action(action, keyword)
        num_results = len(results)
        
        # Filter duplicates across steps if needed, but for simplicity we just extend
        all_results.extend(results)
        
        # 3. Calculate Reward
        # Reward is proportional to the number of valid results. 
        # Negative reward (penalty) if no results to discourage bad strategies.
        if num_results == 0:
            reward = -5.0
        else:
            reward = float(min(num_results, 15)) # Cap reward to prevent explosion
            
        # 4. Determine the next state
        next_state = get_state(num_results)
        
        print(f"[RL Agent] Action '{action}' yielded {num_results} results. Reward: {reward}. Next State: '{next_state}'")
        
        # 5. Update the MDP Q-table
        agent.update_q_table(current_state, action, reward, next_state)
        
        # Transition to next state
        current_state = next_state
        
    print(f"--- Completed RL Scraping. Total Results: {len(all_results)} ---\n")
    return all_results
