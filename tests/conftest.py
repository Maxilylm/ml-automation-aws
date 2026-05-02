"""Shared pytest fixtures for ml-automation-aws."""
from __future__ import annotations
import pytest
from pathlib import Path


@pytest.fixture
def mock_llm_response():
    """Deterministic LLM response for evaluation/integration tests."""
    return {
        "id": "test-completion-001",
        "model": "claude-opus-4-7",
        "choices": [{
            "index": 0,
            "message": {"role": "assistant", "content": "test response content"},
            "finish_reason": "stop",
        }],
        "usage": {"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15},
    }


@pytest.fixture
def sample_dataset():
    """Small in-memory dataset for ML pipeline tests."""
    return [
        {"id": i, "feature_a": float(i), "feature_b": float(i * 2), "label": i % 2}
        for i in range(10)
    ]


@pytest.fixture
def temp_workspace(tmp_path: Path) -> Path:
    """Isolated tmpdir for plugin filesystem operations."""
    return tmp_path
