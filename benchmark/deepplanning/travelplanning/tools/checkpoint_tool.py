"""
Checkpoint Tool - Context pruning via milestone checkpoints (task-scoped)

When invoked, the agent loop prunes the message history sent to the LLM,
keeping only the system prompt, the first user message, and a synthesized
summary of all accumulated checkpoints.
"""
from typing import Dict, List, Optional, Union

from .base_travel_tool import BaseTravelTool, register_tool


@register_tool('create_checkpoint')
class CreateCheckpointTool(BaseTravelTool):
    """Tool for creating a checkpoint that triggers context pruning in the agent loop."""

    def __init__(self, cfg: Optional[Dict] = None):
        super().__init__(cfg)
        # Shared mutable list reference injected via cfg by the agent.
        # Each entry: {"milestone_name": str, "exact_selections": str, "next_steps": str}
        self._checkpoints: List[Dict[str, str]] = cfg.get('checkpoints_store', []) if cfg else []

    def call(self, params: Union[str, dict], **kwargs) -> str:
        """
        Record a checkpoint.  The agent loop will detect this tool was called
        and prune the message history accordingly.

        Args:
            params: Dictionary containing:
                - milestone_name (str): Short name for this milestone
                - exact_selections (str): Key selections / decisions made so far
                - next_steps (str): What remains to be done

        Returns:
            Confirmation string
        """
        params = self._verify_json_format_args(params)

        milestone_name: str = params.get('milestone_name', '')
        exact_selections: str = params.get('exact_selections', '')
        next_steps: str = params.get('next_steps', '')

        if not milestone_name:
            return "milestone_name is required"

        self._checkpoints.append({
            'milestone_name': milestone_name,
            'exact_selections': exact_selections,
            'next_steps': next_steps,
        })

        return (
            f"Checkpoint '{milestone_name}' saved (total checkpoints: {len(self._checkpoints)}). "
            "Context has been pruned."
        )
