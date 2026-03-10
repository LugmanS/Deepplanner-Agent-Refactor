"""
Write Todo Tool - Manage a todo list for travel planning
"""
from typing import Dict, List, Optional, Union

from .base_travel_tool import BaseTravelTool, register_tool


@register_tool('write_todo')
class WriteTodoTool(BaseTravelTool):
    """Tool for writing/updating a todo list"""

    def __init__(self, cfg: Optional[Dict] = None):
        super().__init__(cfg)

    def call(self, params: Union[str, dict], **kwargs) -> str:
        """
        Update the todo list.

        Args:
            params: Dictionary containing 'todos', a list of dicts each with:
                - content (str): The todo item content
                - status (str): One of "pending", "in_progress", "completed"

        Returns:
            Confirmation string with updated todo list
        """
        params = self._verify_json_format_args(params)

        todos: List[Dict[str, str]] = params.get('todos', [])

        # Validate each todo item
        valid_statuses = {"pending", "in_progress", "completed"}
        for item in todos:
            if not isinstance(item, dict):
                return f"Invalid todo item: each item must be a dict, got {type(item).__name__}"
            if 'content' not in item or 'status' not in item:
                return "Each todo item must have 'content' and 'status' fields"
            if item['status'] not in valid_statuses:
                return f"Invalid status '{item['status']}'. Must be one of: {', '.join(valid_statuses)}"

        return f"Updated todo list to {todos}"
