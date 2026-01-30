# tests/unit/agent/test_agent_views.py

import pytest
from windows_use.agent.views import AgentResult, Action, AgentData

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

    def test_action_initialization(self):
        """
        Test Action initialization.
        """
        action = Action(name="test_action", params={"key": "value"})
        assert action.name == "test_action"
        assert action.params == {"key": "value"}
        
        # Test to_dict
        d = action.to_dict()
        assert d == {'name': 'test_action', 'params': {'key': 'value'}}

    def test_agent_data_initialization(self):
        """
        Test AgentData initialization.
        """
        agent_data = AgentData()
        assert agent_data.evaluate is None
        assert agent_data.thought is None
        assert agent_data.action is None
        assert agent_data.observation is None

        mock_action = Action(name="mock_action", params={})
        agent_data_custom = AgentData(
            evaluate="eval", thought="thought", action=mock_action, observation="obs"
        )
        assert agent_data_custom.evaluate == "eval"
        assert agent_data_custom.thought == "thought"
        assert agent_data_custom.action == mock_action
        assert agent_data_custom.observation == "obs"
