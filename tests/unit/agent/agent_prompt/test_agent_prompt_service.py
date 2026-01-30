# tests/unit/agent/agent_prompt/test_agent_prompt_service.py

import pytest
from unittest.mock import MagicMock, patch
from pathlib import Path
from windows_use.agent.prompt.service import Prompt
from windows_use.agent.views import AgentData, Action
from windows_use.agent.registry.views import ToolResult
from windows_use.agent.desktop.views import DesktopState, Browser

class TestPrompt:
    """Tests the static methods of the Prompt service class."""

    @pytest.fixture
    def mock_desktop(self):
        mock = MagicMock()
        mock.get_windows_version.return_value = "Windows 11"
        mock.get_user_account_type.return_value = "Admin"
        mock.get_dpi_scaling.return_value = "100%"
        return mock

    @pytest.fixture
    def mock_desktop_state(self):
        mock = MagicMock(spec=DesktopState)
        mock.active_window_to_string.return_value = "Active App: Notepad"
        mock.windows_to_string.return_value = "Open Apps: [Notepad]"
        mock.active_desktop_to_string.return_value = "Desktop 1"
        mock.desktops_to_string.return_value = "Desktops: [1, 2]"
        mock.tree_state = MagicMock()
        mock.tree_state.interactive_elements_to_string.return_value = "Interactive elements"
        mock.tree_state.scrollable_elements_to_string.return_value = "Scrollable elements"
        return mock

    @patch("windows_use.agent.prompt.service.Path.read_text")
    @patch("windows_use.agent.prompt.service.pg.size")
    def test_system_prompt(self, mock_size, mock_read_text, mock_desktop):
        mock_size.return_value = (1920, 1080)
        mock_read_text.return_value = "System prompt: {datetime} {instructions} {os} {language} {browser} {home_dir} {user} {resolution} {max_steps}"
        
        result = Prompt.system_prompt(
            mode="normal",
            desktop=mock_desktop,
            browser=Browser.EDGE,
            language="English",
            max_steps=25,
            instructions=["Do something"]
        )
        
        assert "System prompt:" in result
        assert "Windows 11" in result
        assert "English" in result
        assert "25" in result

    @patch("windows_use.agent.prompt.service.Path.read_text")
    def test_action_prompt(self, mock_read_text):
        mock_read_text.return_value = "Action prompt: {evaluate} {thought} {action_name} {action_input}"
        agent_data = AgentData(
            evaluate="Good",
            thought="Thinking",
            action=Action(name="click", params={"x": 1})
        )
        
        result = Prompt.action_prompt(agent_data)
        assert "Action prompt:" in result
        assert "Good" in result
        assert "click" in result

    @patch("windows_use.agent.prompt.service.Path.read_text")
    def test_previous_observation_prompt(self, mock_read_text):
        mock_read_text.return_value = "Prev Obs: {steps} {max_steps} {observation} {query}"
        result = Prompt.previous_observation_prompt(query="find paper", step=1, max_steps=10, observation="Seen paper")
        assert "Prev Obs:" in result
        assert "Seen paper" in result
        assert "find paper" in result

    @patch("windows_use.agent.prompt.service.Path.read_text")
    @patch("windows_use.agent.prompt.service.pg.position")
    def test_observation_prompt(self, mock_position, mock_read_text, mock_desktop_state):
        mock_position.return_value = MagicMock(x=10, y=20)
        mock_read_text.return_value = "Obs: {steps} {max_steps} {observation} {active_window} {windows} {cursor_location} {interactive_elements} {scrollable_elements} {active_desktop} {desktops} {query}"
        
        tool_result = ToolResult(is_success=True, content="Success")
        result = Prompt.observation_prompt(
            query="test",
            step=2,
            max_steps=10,
            tool_result=tool_result,
            desktop_state=mock_desktop_state
        )
        
        assert "Obs:" in result
        assert "Success" in result
        assert "(10,20)" in result

    @patch("windows_use.agent.prompt.service.Path.read_text")
    def test_answer_prompt(self, mock_read_text):
        mock_read_text.return_value = "Answer: {evaluate} {thought} {final_answer}"
        agent_data = AgentData(evaluate="Done", thought="Finished", action=Action(name="done", params={}))
        tool_result = ToolResult(is_success=True, content="The result")
        
        result = Prompt.answer_prompt(agent_data, tool_result)
        assert "Answer:" in result
        assert "Done" in result
        assert "The result" in result