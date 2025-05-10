from __future__ import annotations
from backend.commands.utils.command_registry import CommandRegistry
from abc import ABCMeta, abstractmethod
from typing import Any, Literal
import logging

CommandName = str
CommandArgs = dict[str, str]
AgentThoughts = dict[str, Any]

logger = logging.getLogger(__name__)
class BaseAgent(metaclass=ABCMeta):
    """Base class for all Auto-GPT agents."""

    def __init__(self, command_registry: CommandRegistry, ):
        self.command_registry = command_registry

    @abstractmethod
    def execute(
            self,
            command_name: str | None,
            command_args: dict[str, str] | None,
            user_input: str | None,
    ) -> str:
        """Executes the given command, if any, and returns the agent's response.

        Params:
            command_name: The name of the command to execute, if any.
            command_args: The arguments to pass to the command, if any.
            user_input: The user's input, if any.

        Returns:
            The results of the command.
        """
        ...
        logger.info(f"execute command: name={command_name}, command_args={command_args}, userinput={user_input}")
        if command_name is not None and command_name.lower().startswith("error"):
            result = f"Could not execute command: {command_name}{command_args}"
        elif command_name == "human_feedback":
            result = f"Human feedback: {user_input}"
            logger.info(f"execute: {result}")
        else:
            command_result = self.execute_command(
                command_name=command_name,
                arguments=command_args,
            )

            result = f"Command {command_name} returned: " f"{command_result}"
            logger.info(f"execute command result: {result}")


        return result


    def execute_command(
            self,
            command_name: str,
            arguments: dict[str, str]
    ) -> Any:
        """Execute the command and return the result

        Args:
            command_name (str): The name of the command to execute
            arguments (dict): The arguments for the command
            agent (Agent): The agent that is executing the command

        Returns:
            str: The result of the command
        """
        try:
            # Execute a native command with the same name or alias, if it exists
            if command := self.command_registry.get_command(command_name):
                return command(**arguments)

            # Handle non-native commands (e.g. from plugins)
            # for command in agent.ai_config.prompt_generator.commands:
            #     if (
            #             command_name == command.label.lower()
            #             or command_name == command.name.lower()
            #     ):
            #         return command.function(**arguments)

            raise RuntimeError(
                f"Cannot execute '{command_name}': unknown command."
                " Do not try to use this command again."
            )
        except Exception as e:
            return f"Error: {str(e)}"

