from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MODEL = "llama-3.3-70b-versatile"

SYSTEM_PROMPTS = {
    "student": """You are an expert Student Assistant AI. Your job is to help students learn effectively.
You explain concepts clearly with examples, analogies, and step-by-step breakdowns.
You can summarize topics, generate quiz questions, and simplify complex subjects.
Always encourage the student, be patient, and adapt your explanation to their level.
When asked to quiz, generate MCQ or short answer questions with answers at the end.
Format code or math clearly when needed.""",

    "code": """You are an expert Software Engineer and Code Assistant AI.
You help developers write clean, efficient, and well-documented code.
You can debug errors, explain code line by line, suggest improvements, and generate code in any language.
Always explain WHY a solution works, not just what it does.
Format all code in proper markdown code blocks with the language specified.
When debugging, identify the root cause clearly before suggesting a fix.
Follow best practices and mention edge cases where relevant.""",

    "interview": """You are an expert Interview Coach AI specializing in technical and HR interviews.
You conduct realistic mock interviews, ask one question at a time, and wait for the user answer.
After each answer, provide detailed feedback: what was good, what was missing, and a score out of 10.
Always show the score in this exact format: X/10
Cover DSA problems, system design, behavioral STAR method, and HR questions based on the domain selected.
Be encouraging but honest. After all questions are done, provide an overall performance summary.
Always suggest how the candidate can improve their answer."""
}

MODE_SETTINGS = {
    "student": {"temperature": 0.7, "max_tokens": 2048},
    "code":    {"temperature": 0.3, "max_tokens": 3000},
    "interview": {"temperature": 0.6, "max_tokens": 2048},
}

MAX_HISTORY_MESSAGES = 20

def get_groq_response(mode: str, messages: list, stream: bool = False):
    system_prompt = SYSTEM_PROMPTS.get(mode, SYSTEM_PROMPTS["student"])
    settings = MODE_SETTINGS.get(mode, MODE_SETTINGS["student"])

    trimmed_messages = messages[-MAX_HISTORY_MESSAGES:] if len(messages) > MAX_HISTORY_MESSAGES else messages

    full_messages = [{"role": "system", "content": system_prompt}] + trimmed_messages

    response = client.chat.completions.create(
        model=MODEL,
        messages=full_messages,
        temperature=settings["temperature"],
        max_tokens=settings["max_tokens"],
        stream=stream
    )

    if stream:
        return response

    content = response.choices[0].message.content
    if not content or not content.strip():
        content = "I could not generate a response. Please try again."

    return {
        "content": content,
        "tokens_used": response.usage.total_tokens
    }

def get_streaming_response(mode: str, messages: list):
    return get_groq_response(mode, messages, stream=True)