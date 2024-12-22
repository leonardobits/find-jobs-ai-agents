#!/usr/bin/env python
import yaml
from empregos.crew import RecruitmentCrew

def run():
    try:
        with open('src/empregos/config/inputs.yaml', 'r', encoding='utf-8') as file:
            inputs = yaml.safe_load(file)
    except FileNotFoundError:
        with open('src/empregos/config/inputs.example.yaml', 'r', encoding='utf-8') as file:
            inputs = yaml.safe_load(file)

    RecruitmentCrew().crew().kickoff(inputs=inputs)
