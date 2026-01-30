# tests/unit/agent/test_agent_utils.py

import pytest
from unittest.mock import MagicMock, patch
import json
from windows_use.agent.utils import read_file, json_parser
from windows_use.agent.views import AgentData, Action
from windows_use.llms.views import ChatLLMResponse
from windows_use.messages import AIMessage

class TestAgentUtils:
    """
    Tests for utility functions in windows_use.agent.utils.
    """

    @patch("builtins.open", new_callable=MagicMock)
    def test_read_file_success(self, mock_open):
        """Test read_file function."""
        mock_file = MagicMock()
        mock_file.read.return_value = "file content"
        mock_open.return_value.__enter__.return_value = mock_file

        content = read_file("dummy.txt")
        assert content == "file content"
        mock_open.assert_called_once_with("dummy.txt", "r")

    def test_json_parser_success(self):
        """Test json_parser with valid JSON."""
        data = {
            "thought": "I will click here.",
            "evaluate": "Good state",
            "action": {"name": "click_tool", "params": {"loc": [100, 200]}}
        }
        message = ChatLLMResponse(content=AIMessage(content=json.dumps(data)))
        agent_data = json_parser(message)
        
        assert agent_data.thought == data["thought"]
        assert agent_data.evaluate == data["evaluate"]
        assert agent_data.action.name == data["action"]["name"]
        assert agent_data.action.params == data["action"]["params"]

    def test_json_parser_markdown(self):
        """Test json_parser with markdown-wrapped JSON."""
        data = {
            "thought": "Thinking...",
            "evaluate": "Evaluating...",
            "action": {"name": "done_tool", "params": {"answer": "Done"}}
        }
        content = f"Here is the JSON:\n```json\n{json.dumps(data)}\n```"
        message = ChatLLMResponse(content=AIMessage(content=content))
        agent_data = json_parser(message)
        
        assert agent_data.action.name == "done_tool"

    def test_json_parser_invalid_json(self):
        """Test json_parser with invalid JSON."""
        message = ChatLLMResponse(content=AIMessage(content="Not a JSON"))
        with pytest.raises(ValueError, match="Invalid JSON format"):
            json_parser(message)

    def test_json_parser_missing_fields(self):
        """Test json_parser with missing required fields."""
        data = {"thought": "missing action and evaluate"}
        message = ChatLLMResponse(content=AIMessage(content=json.dumps(data)))
        with pytest.raises(ValueError, match="Missing required fields"):
            json_parser(message)
