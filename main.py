import yaml
from assistant.agents.feeds import FeedsAgent


if __name__ == "__main__":
    with open('configs.yaml', 'r') as f:
        configs = yaml.safe_load(f)

    with open('auths.yaml', 'r') as f:
        auths_configs = yaml.safe_load(f)

    # feeds
    feeds_agent = FeedsAgent(configs['feeds'], auths_configs)
    
    feeds_agent.run_task()
    