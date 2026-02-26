# tests/unit/agent/agent_prompt/test_agent_prompt_service.py

import pytest
from unittest.mock import MagicMock, patch
from windows_use.agent.prompt.service import Prompt
from windows_use.agent.desktop.views import DesktopState, Browser

class TestPrompt:
    """Tests the static methods of the Prompt service class."""

    @pytest.fixture
    def mock_desktop(self):
        mock = MagicMock()
        mock.get_windows_version.return_value = "Windows 11"
        mock.get_user_account_type.return_value = "Admin"
        mock.get_dpi_scaling.return_value = "100%"
        mock.get_default_language.return_value = "English"
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
        mock_read_text.return_value = (
            "System prompt: {datetime} {instructions} {os} {language} {browser} "
            "{home_dir} {user} {resolution} {max_steps}"
        )
        
        result = Prompt.system(
            mode="normal",
            desktop=mock_desktop,
            browser=Browser.EDGE,
            max_steps=25,
            instructions=["Do something"]
        )
        
        assert "System prompt:" in result
        assert "Windows 11" in result
        assert "English" in result
        assert "25" in result

    @patch("windows_use.agent.prompt.service.Path.read_text")
    @patch("windows_use.agent.prompt.service.pg.size")
    def test_system_prompt_flash(self, mock_size, mock_read_text, mock_desktop):
        mock_size.return_value = (1920, 1080)
        mock_read_text.return_value = "Flash prompt: {datetime} {os} {browser} {max_steps}"

        result = Prompt.system(
            mode="flash",
            desktop=mock_desktop,
            browser=Browser.EDGE,
            max_steps=5,
        )

        assert "Flash prompt:" in result
        assert "Windows 11" in result
        assert Browser.EDGE.value in result
        assert "5" in result

    @patch("windows_use.agent.prompt.service.Path.read_text")
    @patch("windows_use.agent.prompt.service.pg.position")
    def test_human_prompt(self, mock_position, mock_read_text, mock_desktop_state):
        mock_position.return_value = MagicMock(x=10, y=20)
        mock_read_text.return_value = (
            "Human prompt: {steps} {max_steps} {active_window} {windows} {cursor_location} "
            "{interactive_elements} {scrollable_elements} {active_desktop} {desktops} {query}"
        )

        mock_desktop = MagicMock()
        mock_desktop.use_accessibility = True
        mock_desktop.desktop_state = mock_desktop_state

        result = Prompt.human(
            query="test",
            step=2,
            max_steps=10,
            desktop=mock_desktop,
        )

        assert "Human prompt:" in result
        assert "Notepad" in result
        assert "(10,20)" in result
        assert "test" in result
