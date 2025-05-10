"""Commands to control the internal state of the program"""

from __future__ import annotations

COMMAND_CATEGORY = "system"
COMMAND_CATEGORY_TITLE = "System"

from typing import NoReturn

from src.autogpt_agent.autogpt.agents.agent import Agent
from src.autogpt_agent.autogpt.command_decorator import command
from src.autogpt_agent.autogpt.logs import logger


@command(
    "goals_accomplished",
    "This is the command for the last step to finish your task, used to give your final conclusion.",
    {
        "reason": {
            "type": "string",
            "description": "A summary to the user of how the goals were accomplished ",
            "required": True,
        },
        "final_answer": {
            "type": "string",
            "description": "A detailed explanation with your final conclusion to the user's requirement ",
            "required": True,
        }

    },
)
def task_complete(reason: str, final_answer: str, agent: Agent) -> NoReturn:
    """
    A function that takes in a string and exits the program

    Parameters:
        reason (str): A summary to the user of how the goals were accomplished.
        final_answer (str): A detailed explanation with your final conclusion to the user's requirement.
    Returns:
        A result string from create chat completion. A list of suggestions to
            improve the code.
    """
    logger.info(title="Shutting down...\n", message=reason)
    return reason
    # quit()
