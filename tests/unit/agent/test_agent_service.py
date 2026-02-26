# tests/unit/agent/test_agent_service.py

import pytest
from unittest.mock import MagicMock, patch
from windows_use.agent.service import Agent
from windows_use.agent.views import AgentResult
from windows_use.messages import ToolMessage
from windows_use.llms.views import ChatLLMResponse

class TestAgent:
    """
    Tests for the Agent class in windows_use.agent.service.
    """

    @pytest.fixture
    def mock_llm(self):
        """Mock LLM."""
        mock = MagicMock()
        mock.model_name = "test-model"
        mock.provider = "test-provider"
        return mock

    @pytest.fixture
    def mock_desktop(self):
        """Mock Desktop."""
        with patch("windows_use.agent.service.Desktop") as mock_class:
            mock_instance = mock_class.return_value
            mock_instance.get_state.return_value = MagicMock(screenshot=None)
            mock_instance.use_vision = False
            mock_instance.tree.on_focus_change = MagicMock()
            yield mock_instance

    @pytest.fixture
    def mock_prompt(self):
        """Mock Prompt with string return values for Pydantic."""
        with patch("windows_use.agent.service.Prompt") as mock_p:
            mock_instance = mock_p.return_value
            mock_instance.system.return_value = "System prompt"
            mock_instance.human.return_value = "Human prompt"
            yield mock_p

    @pytest.fixture
    def mock_console(self):
        """Mock Console."""
        with patch("windows_use.agent.service.Console") as mock_class:
            yield mock_class.return_value

    def test_init(self, mock_llm, mock_desktop, mock_console):
        """Test Agent initialization."""
        agent = Agent(llm=mock_llm, instructions=["Test instruction"])
        assert agent.instructions == ["Test instruction"]
        assert agent.state.max_steps == 25
        assert agent.state.max_consecutive_failures == 3

    @patch("windows_use.agent.service.Registry")
    @patch("windows_use.agent.service.WatchDog")
    def test_invoke_done(self, mock_watchdog, mock_registry_class, mock_llm, mock_desktop, mock_prompt, mock_console):
        """Test invoke method when task is completed via done_tool."""
        mock_registry = mock_registry_class.return_value
        
        # When execute is called, it returns a ToolResult-like object
        mock_response = MagicMock()
        mock_response.content = "Job's done"
        mock_response.is_success = True
        mock_registry.execute.return_value = mock_response
        
        # Mock LLM response
        mock_llm.invoke.return_value = ChatLLMResponse(
            content=ToolMessage(
                id="1",
                name="done_tool",
                params={"thought": "I have finished the task.", "evaluate": "Task complete", "answer": "Job's done"},
            )
        )
        
        agent = Agent(llm=mock_llm)
        result = agent.invoke("test query")
        
        assert isinstance(result, AgentResult)
        assert result.is_done is True
        assert result.content == "Job's done"
        assert mock_llm.invoke.call_count == 1

    @patch("windows_use.agent.service.Registry")
    @patch("windows_use.agent.service.WatchDog")
    def test_invoke_max_steps(self, mock_watchdog, mock_registry_class, mock_llm, mock_desktop, mock_prompt, mock_console):
        """Test invoke method stops after max_steps."""
        mock_registry = mock_registry_class.return_value
        mock_response = MagicMock()
        mock_response.content = "Step result"
        mock_response.is_success = True
        mock_registry.execute.return_value = mock_response
        
        # Mock LLM response (non-done action)
        mock_llm.invoke.return_value = ChatLLMResponse(
            content=ToolMessage(
                id="1",
                name="click_tool",
                params={"thought": "Keep working", "evaluate": "Not done", "loc": [10, 10]},
            )
        )
        
        agent = Agent(llm=mock_llm, max_steps=2)
        result = agent.invoke("test query")
        
        assert result.is_done is False
        assert "maximum number of steps" in result.error
        assert mock_llm.invoke.call_count == 2

