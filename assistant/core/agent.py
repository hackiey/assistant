from abc import ABC, abstractmethod


class Agent:
    @abstractmethod
    def run_task(self):
        pass
