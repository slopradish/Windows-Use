# tests/unit/agent/test_agent_views.py

import pytest
from windows_use.agent.views import AgentResult, AgentState
from windows_use.messages import AIMessage

class TestAgentViews:
    """
    Tests for the data models in windows_use.agent.views.
    """

    def test_agent_result_initialization(self):
        """
        Test AgentResult initialization.
        """
        result = AgentResult(is_done=False)
        assert result.is_done is False
        assert result.content is None
        assert result.error is None

        result_custom = AgentResult(is_done=True, content="Success", error="No error")
        assert result_custom.is_done is True
        assert result_custom.content == "Success"
        assert result_custom.error == "No error"

    def test_agent_state_defaults(self):
        """
        Test AgentState default values.
        """
        state = AgentState()
        assert state.task == ""
        assert state.messages == []
        assert state.error_messages == []
        assert state.desktop is None
        assert state.step == 0
        assert state.max_steps == 25
        assert state.max_consecutive_failures == 3

    def test_agent_state_custom(self):
        """
        Test AgentState initialization with custom values.
        """
        msg = AIMessage(content="hello")
        state = AgentState(
            task="test",
            messages=[msg],
            error_messages=[msg],
            step=2,
            max_steps=10,
            max_consecutive_failures=1,
        )
        assert state.task == "test"
        assert state.messages == [msg]
        assert state.error_messages == [msg]
        assert state.step == 2
        assert state.max_steps == 10
        assert state.max_consecutive_failures == 1
