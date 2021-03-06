#!/usr/bin/env python3
"""This is a test of flask."""

# Standard packages
import socket
import json
import logging

# Pip packages
from flask import Flask

from infoset.agents import agent as Agent
from infoset.agents import data_linux
from infoset.utils import jm_configuration

# Define flask parameters
APP = Flask(__name__)


@APP.route('/')
def home():
    """Display api data on home page.

    Args:
        None

    Returns:
        None

    """
    # Initialize key variables
    agent_name = 'linux_passive'

    # Get configuration
    config = jm_configuration.ConfigAgent(agent_name)

    # Get hostname
    hostname = socket.getfqdn()

    # Initialize key variables
    agent = Agent.Agent(config, hostname)

    # Update agent with linux data
    data_linux.getall(agent)

    # Return
    data_dict = agent.polled_data()
    data = json.dumps(data_dict)
    return data


if __name__ == "__main__":
    APP.logger.setLevel(logging.DEBUG)
    APP.logger.addHandler()

    # Start app
    APP.run(debug=True)
