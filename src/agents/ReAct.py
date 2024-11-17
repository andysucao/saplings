# Standard library
from typing import List, Optional, Tuple

# Local
from src.abstract import Tool, Model
from src.agents.Base import BaseAgent
from src.dtos import Node, Message
from src.prompts import AGENT_PROMPT


class ReActAgent(BaseAgent):
    def __init__(
        self,
        tools: List[Tool],
        model: Optional[Model] = None,
        prompt: str = AGENT_PROMPT,
        max_depth: int = 5,
        verbose: bool = True,
        tool_choice: str = "auto",
        parallel_tool_calls: bool = False,
    ):
        super().__init__(
            tools,
            model,
            evaluator=None,
            prompt=prompt,
            b_factor=1,
            max_depth=max_depth,
            threshold=1.0,
            verbose=verbose,
            tool_choice=tool_choice,
            parallel_tool_calls=parallel_tool_calls,
        )

    def should_terminate(self, node: Node) -> bool:
        return self.is_terminal_node(node)

    async def run_async(self, prompt: str) -> Tuple[List[Message], float, bool]:
        self.log(f"Running a ReAct sequence (no search)\n\n\033[37m{prompt}\033[0m\n")

        curr_node = Node([Message.user(prompt)])
        while not self.should_terminate(curr_node):
            await self.expand(curr_node, run_eval=False)
            curr_node = curr_node.children[0]

        messages = curr_node.get_trajectory()

        self.log(
            f"\033[1;32mFinal trajectory:\033[0m\n\n"
            + "\n".join(str(m) for m in messages)
        )

        return messages
