import anthropic
import os
import datetime
import subprocess
import re


SYSTEM = """You are a tech blogger writing for "Poorly Researched" — tagline: "Thoughts on tech, AI, and career — half-baked and served fresh."

Style rules:
- Slightly sarcastic, self-aware, never mean
- Casual and direct — no corporate speak, no buzzword salad
- Looks at real implications and future consequences, not just what happened
- Grounded in specific facts, numbers, and named examples
- Confident but honest about uncertainty
- Like a smart friend explaining something over coffee, not a press release
- Occasionally funny without trying too hard

Post format (strict):
- Title on line 1 (no quotes, no label)
- Blank line
- 350 words of flowing prose — no headers, no bullet points
- Don't start with "Today I want to..." — open with something interesting
- End with a forward-looking thought or wry observation"""


def get_yesterday():
    return (datetime.date.today() - datetime.timedelta(days=1)).strftime("%B %d, %Y")


def generate_post():
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    yesterday = get_yesterday()

    messages = [{
        "role": "user",
        "content": (
            f"Search the web for the most interesting tech, AI, and gaming news from {yesterday}. "
            "Then pick the single most interesting topic — the one with the most surprising implications "
            "or that most people are underestimating — and write a 350-word blog post about it.\n\n"
            "Return ONLY:\n"
            "Line 1: Post title\n"
            "Line 2: blank\n"
            "Lines 3+: the 350-word post body\n\n"
            "Nothing else. No preamble."
        )
    }]

    # Web search is server-side — just handle pause_turn if the server loop hits its limit
    for _ in range(5):
        response = client.messages.create(
            model="claude-opus-4-8",
            max_tokens=2048,
            system=SYSTEM,
            tools=[{"type": "web_search_20260209", "name": "web_search"}],
            messages=messages,
        )

        if response.stop_reason == "end_turn":
            for block in response.content:
                if hasattr(block, "text") and block.text.strip():
                    return block.text.strip()

        if response.stop_reason == "pause_turn":
            # Append assistant turn and loop — server resumes automatically from the trailing tool blocks
            messages.append({"role": "assistant", "content": response.content})
        else:
            break

    raise RuntimeError(f"Unexpected stop_reason: {response.stop_reason}")


def create_post_file(content, date):
    lines = content.strip().split("\n")
    title = lines[0].strip().strip('"').strip("'")
    body = "\n".join(lines[2:]).strip()

    slug = re.sub(r"[^\w\s-]", "", title.lower())
    slug = re.sub(r"\s+", "-", slug)[:50].strip("-")

    filename = f"_posts/{date.strftime('%Y-%m-%d')}-{slug}.md"

    with open(filename, "w") as f:
        f.write(f"""---
layout: post
title: "{title}"
date: {date.strftime('%Y-%m-%d')}
categories: tech
---

{body}
""")

    return filename, title


def push_to_github(filename, title):
    subprocess.run(["git", "config", "user.email", "murmur.red1@gmail.com"], check=True)
    subprocess.run(["git", "config", "user.name", "murmur-red"], check=True)
    subprocess.run(["git", "add", filename], check=True)
    subprocess.run(["git", "commit", "-m", f"Add post: {title}"], check=True)
    subprocess.run(["git", "push"], check=True)


if __name__ == "__main__":
    today = datetime.date.today()
    content = generate_post()
    filename, title = create_post_file(content, today)
    push_to_github(filename, title)
    print(f"Published: {filename}")
