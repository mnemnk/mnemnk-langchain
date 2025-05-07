import argparse
import json
import sys
from abc import ABC, abstractmethod
from typing import Any, Optional, Type

from loguru import logger


class BaseAgent(ABC):
    """Abstract base class for all agent implementations."""

    # Default configuration - can be overridden by subclasses
    DEFAULT_CONFIG = {}
    
    def __init__(self, config: Optional[dict[str, Any]] = None):
        """Initialize the agent with configuration.
        
        Args:
            config: Configuration for the agent
        """
        # Use provided config or empty dict
        self.config = config or {}
    
    def run(self):
        """Main loop for the agent."""
        for line in sys.stdin:
            line = line.strip()
            
            if line.startswith(".CONFIG "):
                self._handle_config(line)
            elif line == ".QUIT":
                break
            elif line.startswith(".IN "):
                self._handle_input(line)

    def _handle_config(self, line: str):
        """Handle CONFIG command."""
        try:
            [_, config_str] = line.split(" ", 1)
            new_config = json.loads(config_str)
            self.config.update(new_config)
            self.process_config(new_config)
        except Exception as e:
            logger.error(f"Error processing config: {e}")
            return
    
    def process_config(self, new_config: Optional[dict[str, Any]]):
        """Process configuration changes. Can be override by subclasses.
        
        Args:
            new_config: The new configuration
        """
        pass

    def _handle_input(self, line: str):
        """Handle IN command."""
        try:
            [ch, kind, value, metadata] = BaseAgent.parse_input(line)
            self.process_input(ch, kind, value, metadata)
        except Exception as e:
            logger.error(f"Error processing input: {e}")
    
    @abstractmethod
    def process_input(self, ch: str, kind: str, value: Any, metadata: Optional[dict[str, Any]]):
        """Process input based on kind and value. Must be implemented by subclasses.
        
        Args:
            ch: The channel of input
            kind: The kind of input
            value: The input value
            metadata: Optional metadata for the input
        """
        pass

    @staticmethod
    def parse_input(line: str) -> tuple[str, str, Any, Optional[dict[str, Any]]]:
        """Parse input line into kind and value.
        
        Args:
            line: Input line starting with ".IN "
            
        Returns:
            A tuple of (ch, kind, value, metadata)
            
        Raises:
            ValueError: If the input line is invalid
        """
        parts = line.split(" ", 1)
        if len(parts) < 2:
            raise ValueError("Invalid input format")

        in_data = json.loads(parts[1])
        if not isinstance(in_data, dict):
            raise ValueError("Invalid input format")

        if "ch" not in in_data or "kind" not in in_data or "value" not in in_data:
            raise ValueError("Invalid input format")

        if not isinstance(in_data["ch"], str):
            raise ValueError("Invalid input format")
        ch = in_data["ch"]

        if not isinstance(in_data["kind"], str):
            raise ValueError("Invalid input format")
        kind = in_data["kind"]

        value = in_data["value"]

        metadata = in_data.get("metadata", None)

        return ch, kind, value, metadata
    
    def write_out(self, ch: str, kind: str, value: Any, metadata: Optional[dict[str, Any]]):
        """Write output with given kind and value.
        
        Args:
            ch: The channel of the output
            kind: The kind of output
            value: The value to output (will be JSON serialized)
        """
        out_data = {
            "ch": ch,
            "kind": kind,
            "value": value,
            "metadata": metadata,
        }
        print(f".OUT {json.dumps(out_data)}", flush=True)


def configure_io():
    """Configure input/output streams to use UTF-8 encoding."""
    sys.stdin.reconfigure(encoding='utf-8')
    sys.stdout.reconfigure(encoding='utf-8')


def parse_agent_config(agent_class: Type['BaseAgent']) -> dict[str, Any]:
    """Parse command line arguments and create config dictionary.
    
    Args:
        agent_class: The agent class to get DEFAULT_CONFIG from
        
    Returns:
        Configuration dictionary with values from DEFAULT_CONFIG and command line
    """
    # Start with class DEFAULT_CONFIG
    config = {}
    if hasattr(agent_class, 'DEFAULT_CONFIG'):
        config.update(agent_class.DEFAULT_CONFIG.copy())
    
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", help="config json string")
    args = parser.parse_args()
    
    # Update with command line config if provided
    if args.config:
        try:
            cli_config = json.loads(args.config)
            config.update(cli_config)
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing config JSON: {e}")
    
    return config


def run_agent(agent_class: Type['BaseAgent']):
    """Create and run an agent with the given configuration.
    
    Args:
        agent_class: The agent class to instantiate
        instance_config: Optional instance-specific configuration
    """
    # Configure I/O
    configure_io()
    
    # Get configuration
    config = parse_agent_config(agent_class)
    
    # Create and run the agent
    agent = agent_class(config)
    agent.run()
