"""
Write Draft Plan Tool - Save a draft plan string
"""
import json
import os
from typing import Dict, Optional, Union

from .base_travel_tool import BaseTravelTool, register_tool

CHECKLIST_PATH = os.path.join(os.path.dirname(__file__), 'checklist.json')


@register_tool('write_draft_plan')
class WriteDraftPlanTool(BaseTravelTool):
    """Tool for saving a draft plan string"""

    def __init__(self, cfg: Optional[Dict] = None):
        super().__init__(cfg)

    def call(self, params: Union[str, dict], **kwargs) -> str:
        """
        Accept a draft plan string and return a success message.

        When the ENABLE_CHECKLIST_RESPONSE environment variable is set to '1'
        or 'true', returns a formatted checklist instead of the simple message.

        Args:
            params: Dictionary containing:
                - draft_plan (str): Draft plan content

        Returns:
            Success message, or formatted checklist if the toggle is enabled.
        """
        params = self._verify_json_format_args(params)
        _ = params.get('draft_plan', '')
        
        return self._format_checklist()

    @staticmethod
    def _format_checklist() -> str:
        """Load checklist.json and return it as a formatted string."""
        with open(CHECKLIST_PATH, 'r', encoding='utf-8') as f:
            checklist = json.load(f)

        lines = []
        for category, items in checklist.items():
            heading = category.replace('_', ' ').title()
            lines.append(f"## {heading}")
            for i, item in enumerate(items, 1):
                lines.append(f"  {i}. {item}")
            lines.append('')  # blank line between sections

        return '\n'.join(lines).strip()
