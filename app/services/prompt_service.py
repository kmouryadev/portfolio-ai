class PromptService:
  """Responsible for building prompts sent to the LLM."""
  def build_chat_prompt(
    self,
    message: str,
  ) -> str:
    return f"""
  You are an AI assistant for Karun Mourya.
  Answer the user's question professionally.
  Question:
  {message}
  """.strip()