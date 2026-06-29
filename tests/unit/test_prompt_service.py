from app.services.prompt_service import PromptService

class TestPromptService:
  def test_build_prompt_contains_question(self):
    service = PromptService()
    context = [
      {
        "text": "Karun knows React.",
        "score": 0.92,
        "chunk_index": 0,
      }
    ]
    prompt = service.build_chat_prompt(
      question="What frontend frameworks does Karun know?",
      context=context,
    )
    assert (
      "What frontend frameworks"
      in prompt
    )
    assert (
      "Karun knows React."
      in prompt
    )

  def test_prompt_contains_identity(self):
    service = PromptService()
    prompt = service.build_chat_prompt(
      question="Hello",
      context=[],
    )
    assert (
      "Karun Mourya"
      in prompt
    )
    assert (
      "AI Portfolio Assistant"
      in prompt
    )