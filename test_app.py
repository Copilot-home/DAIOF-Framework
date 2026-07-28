"""Tests for HyperAI application, focusing on trigger_runtime response handling."""

import sys
import asyncio
import unittest
from unittest.mock import patch, MagicMock, AsyncMock


# Mock hypercore before importing app
mock_hypercore_module = MagicMock()
mock_hypercore_module.ExecutionMode = MagicMock()
mock_hypercore_module.ExecutionMode.READ_ONLY = MagicMock(value="read_only")
mock_hypercore_module.HyperCore = MagicMock()
mock_hypercore_module.HyperCoreAPI = MagicMock()
sys.modules["hypercore"] = mock_hypercore_module

from app import HyperAIApplication


class TestTriggerRuntimeResponseHandling(unittest.TestCase):
    """Test trigger_runtime handles None and missing response_text safely."""

    def setUp(self):
        with patch("app.setup_logging") as mock_log:
            mock_log.return_value = MagicMock()
            self.app = HyperAIApplication()

    def _run(self, coro):
        return asyncio.run(coro)

    @patch.object(HyperAIApplication, "health_check", new_callable=AsyncMock)
    @patch.object(HyperAIApplication, "_list_ollama_models", new_callable=AsyncMock)
    @patch.object(HyperAIApplication, "process_inference_request", new_callable=AsyncMock)
    def test_trigger_runtime_none_response_text(self, mock_infer, mock_models, mock_health):
        """trigger_runtime must not crash when LLM response text is None."""
        mock_health.return_value = {
            "status": "healthy",
            "components": {"hypercore": "ready", "ollama": "connected", "memory": "initialized"},
        }
        mock_models.return_value = {"models": [{"name": "qwen2.5:0.5b"}]}
        # Simulate an inference response where nested "response" key is missing
        mock_infer.return_value = {"status": "success", "response": {"model": "qwen2.5:0.5b"}}

        result = self._run(self.app.trigger_runtime("test-trigger", "ASK_SYSTEM_STATE", "qwen2.5:0.5b"))

        self.assertIn("goal_status", result)
        self.assertIsNone(result["module_execution_trace"]["llm_response_sample"])

    @patch.object(HyperAIApplication, "health_check", new_callable=AsyncMock)
    @patch.object(HyperAIApplication, "_list_ollama_models", new_callable=AsyncMock)
    @patch.object(HyperAIApplication, "process_inference_request", new_callable=AsyncMock)
    def test_trigger_runtime_empty_string_response(self, mock_infer, mock_models, mock_health):
        """trigger_runtime handles empty string response gracefully."""
        mock_health.return_value = {
            "status": "healthy",
            "components": {"hypercore": "ready", "ollama": "connected", "memory": "initialized"},
        }
        mock_models.return_value = {"models": [{"name": "qwen2.5:0.5b"}]}
        mock_infer.return_value = {"status": "success", "response": {"model": "qwen2.5:0.5b", "response": ""}}

        result = self._run(self.app.trigger_runtime("test-trigger", "ASK_SYSTEM_STATE", "qwen2.5:0.5b"))

        self.assertIn("goal_status", result)
        # Empty string is falsy so response_text block is skipped
        self.assertIsNone(result["module_execution_trace"]["llm_response_sample"])

    @patch.object(HyperAIApplication, "health_check", new_callable=AsyncMock)
    @patch.object(HyperAIApplication, "_list_ollama_models", new_callable=AsyncMock)
    @patch.object(HyperAIApplication, "process_inference_request", new_callable=AsyncMock)
    def test_trigger_runtime_valid_response_no_gap(self, mock_infer, mock_models, mock_health):
        """trigger_runtime processes a valid response indicating completion."""
        mock_health.return_value = {
            "status": "healthy",
            "components": {"hypercore": "ready", "ollama": "connected", "memory": "initialized"},
        }
        mock_models.return_value = {"models": [{"name": "qwen2.5:0.5b"}]}
        mock_infer.return_value = {
            "status": "success",
            "response": {"model": "qwen2.5:0.5b", "response": '{"goal_status": "complete", "remaining_gap": ""}'},
        }

        result = self._run(self.app.trigger_runtime("test-trigger", "ASK_SYSTEM_STATE", "qwen2.5:0.5b"))

        self.assertIn("goal_status", result)
        self.assertEqual(result["goal_status"], "CLOSED")
        self.assertNotIn("llm_reported_remaining_gap", result["remaining_gap"])

    @patch.object(HyperAIApplication, "health_check", new_callable=AsyncMock)
    @patch.object(HyperAIApplication, "_list_ollama_models", new_callable=AsyncMock)
    @patch.object(HyperAIApplication, "process_inference_request", new_callable=AsyncMock)
    def test_trigger_runtime_response_with_large_gap(self, mock_infer, mock_models, mock_health):
        """trigger_runtime detects 'large gap' in LLM response."""
        mock_health.return_value = {
            "status": "healthy",
            "components": {"hypercore": "ready", "ollama": "connected", "memory": "initialized"},
        }
        mock_models.return_value = {"models": [{"name": "qwen2.5:0.5b"}]}
        mock_infer.return_value = {
            "status": "success",
            "response": {"model": "qwen2.5:0.5b", "response": "There is a large gap in the system coverage."},
        }

        result = self._run(self.app.trigger_runtime("test-trigger", "ASK_SYSTEM_STATE", "qwen2.5:0.5b"))

        self.assertIn("llm_reported_remaining_gap", result["remaining_gap"])
        self.assertEqual(result["goal_status"], "NOT_CLOSED")

    @patch.object(HyperAIApplication, "health_check", new_callable=AsyncMock)
    @patch.object(HyperAIApplication, "_list_ollama_models", new_callable=AsyncMock)
    @patch.object(HyperAIApplication, "process_inference_request", new_callable=AsyncMock)
    def test_trigger_runtime_inference_failure(self, mock_infer, mock_models, mock_health):
        """trigger_runtime handles inference failure gracefully."""
        mock_health.return_value = {
            "status": "healthy",
            "components": {"hypercore": "ready", "ollama": "connected", "memory": "initialized"},
        }
        mock_models.return_value = {"models": [{"name": "qwen2.5:0.5b"}]}
        mock_infer.return_value = {"status": "error", "message": "timeout"}

        result = self._run(self.app.trigger_runtime("test-trigger", "ASK_SYSTEM_STATE", "qwen2.5:0.5b"))

        self.assertEqual(result["goal_status"], "NOT_CLOSED")
        self.assertIn("llm_inference_failed", result["remaining_gap"])
        self.assertIsNone(result["module_execution_trace"]["llm_response_sample"])

    @patch.object(HyperAIApplication, "health_check", new_callable=AsyncMock)
    @patch.object(HyperAIApplication, "_list_ollama_models", new_callable=AsyncMock)
    def test_trigger_runtime_model_not_available(self, mock_models, mock_health):
        """trigger_runtime reports when default model is not available."""
        mock_health.return_value = {
            "status": "healthy",
            "components": {"hypercore": "ready", "ollama": "connected", "memory": "initialized"},
        }
        mock_models.return_value = {"models": [{"name": "llama3:8b"}]}

        result = self._run(self.app.trigger_runtime("test-trigger", "ASK_SYSTEM_STATE"))

        self.assertEqual(result["goal_status"], "NOT_CLOSED")
        self.assertIn("default_model_not_available:qwen2.5:0.5b", result["remaining_gap"])


if __name__ == "__main__":
    unittest.main()
