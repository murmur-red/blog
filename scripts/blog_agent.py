import anthropic
import os
import datetime
import subprocess
import re
import json
import uuid
import base64
import requests

BLOG_BASE_URL = "https://murmur-red.github.io/blog"
WEBSITE_ARTICLES_API = "https://api.github.com/repos/murmur-red/murmur/contents/articles.json"


SYSTEM = """You are writing a blog post for "Poorly Researched" — tagline: "Thoughts on tech, AI, and career — half-baked and served fresh."

Voice and tone:
- Personal and direct. Use "I" and "we". Sound like a real person, not a publication.
- Short punchy sentences mixed with longer explanations. Vary the rhythm.
- Strong opinions stated plainly. No hedging language.
- A little sarcastic, occasionally funny, never mean.
- Explain things properly. Don't assume the reader knows everything. Make it clear.
- End with a real conclusion. Wrap it up. Land the point. Don't leave it dangling.
- Plain words. No jargon unless you explain it.

Argument quality — non-negotiable:
- Every post must make ONE clear, specific argument. Not a vibe. Not an observation. A claim someone could disagree with.
- Back the argument with at least ONE concrete example: a real company, a real number, a real event, a named person, a specific product. "Some companies" and "many experts" are not examples. Name them.
- Acknowledge the strongest counterargument in one sentence, then explain why your argument still holds. Ignoring the other side makes the post weak.
- If the research contains numbers or facts, use them. Vague gestures at data ("studies show", "research suggests") are banned.

Hard rules — never break these:
- NO em dashes (—). Use a period or colon instead.
- NO filler transitions: "Furthermore", "Moreover", "It's worth noting", "Interestingly", "Notably".
- NO passive voice.
- NO hedging: "could potentially", "might possibly", "to some extent".
- NO generic endings like "only time will tell" or "the future remains uncertain".
- NO bullet points or headers in the post body.
- NO unsupported assertions — every claim needs a fact, number, or named example from the research to back it.

Post format (strict):
- Title on line 1 (no quotes, no label)
- Blank line
- 350 words of flowing prose — hit this target, do not fall short
- Open with something that grabs attention, not "Today I want to talk about"
- Close with a clear conclusion: what does this mean, what should we think about it"""


def get_yesterday():
    return (datetime.date.today() - datetime.timedelta(days=1)).strftime("%B %d, %Y")


def get_x_trends(yesterday):
    """Use Grok to find what's trending on X in tech/AI/gaming."""
    response = requests.post(
        "https://api.x.ai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {os.environ['XAI_API_KEY']}",
            "Content-Type": "application/json",
        },
        json={
            "model": "grok-3",
            "messages": [{
                "role": "user",
                "content": (
                    f"What were the top trending tech, AI, and gaming topics on X on {yesterday}? "
                    "Focus on what people were actually debating, hyping, or dunking on. "
                    "Give me the top 3 topics with a sentence on why each was getting attention."
                )
            }],
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]


def research_topics(trends, yesterday):
    """Use Perplexity to research the X trends deeper with facts and context."""
    for attempt in range(3):
        try:
            response = requests.post(
                "https://api.perplexity.ai/chat/completions",
                headers={
                    "Authorization": f"Bearer {os.environ['PERPLEXITY_API_KEY']}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "sonar-pro",
                    "messages": [{
                        "role": "user",
                        "content": (
                            f"These topics were trending on X on {yesterday}:\n\n{trends}\n\n"
                            "Research each one and give me the actual facts, numbers, and context behind them. "
                            "What really happened? What are the real implications? Be specific and concise."
                        )
                    }],
                },
                timeout=90,
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except requests.exceptions.Timeout:
            if attempt == 2:
                raise
            print(f"Perplexity timeout, retrying ({attempt + 2}/3)...")


def write_post(research, yesterday):
    """Use Claude to write a 350-word blog post based on the research."""
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    response = client.messages.create(
        model="claude-opus-4-8",
        max_tokens=1024,
        system=SYSTEM,
        messages=[{
            "role": "user",
            "content": (
                f"Here's what was trending and what's behind it from {yesterday}:\n\n"
                f"{research}\n\n"
                "Pick the single most interesting topic — the one with the most surprising implications "
                "or that most people are underestimating — and write a 350-word blog post about it.\n\n"
                "Return ONLY:\n"
                "Line 1: Post title\n"
                "Line 2: blank\n"
                "Lines 3+: the 350-word post body\n\n"
                "Nothing else. No preamble."
            )
        }],
    )
    text = response.content[0].text.strip()
    # Hard-remove em dashes regardless of what the model produces
    text = text.replace(" — ", ". ").replace("— ", ". ").replace(" —", ".").replace("—", ".")
    return text


def generate_post():
    yesterday = get_yesterday()
    trends = get_x_trends(yesterday)
    research = research_topics(trends, yesterday)
    return write_post(research, yesterday)


def create_post_file(content, date):
    lines = content.strip().split("\n")
    title = lines[0].strip().strip('"').strip("'")
    body = "\n".join(lines[2:]).strip()

    slug = re.sub(r"[^\w\s-]", "", title.lower())
    slug = re.sub(r"\s+", "-", slug)[:50].strip("-")

    filename = f"_posts/{date.strftime('%Y-%m-%d')}-{slug}.md"

    # json.dumps yields a valid double-quoted YAML scalar with inner quotes
    # escaped, so titles containing " or ' can't break the front matter.
    yaml_title = json.dumps(title)

    with open(filename, "w") as f:
        f.write(f"""---
layout: post
title: {yaml_title}
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


def publish_to_website(title, date, slug):
    token = os.environ["MURMUR_WEBSITE_TOKEN"]
    url = f"{BLOG_BASE_URL}/tech/{date.strftime('%Y/%m/%d')}/{slug}.html"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
    }

    res = requests.get(WEBSITE_ARTICLES_API, headers=headers)
    res.raise_for_status()
    file_data = res.json()
    sha = file_data["sha"]
    data = json.loads(base64.b64decode(file_data["content"]).decode())

    data["articles"].insert(0, {
        "id": str(uuid.uuid4()),
        "title": title,
        "type": "Blog",
        "topic": "Tech & AI",
        "date": date.isoformat(),
        "status": "Published",
        "url": url,
    })
    data["updated"] = date.isoformat()

    res = requests.put(WEBSITE_ARTICLES_API, headers=headers, json={
        "message": f"Add blog post: {title}",
        "content": base64.b64encode(json.dumps(data, indent=2).encode()).decode(),
        "sha": sha,
        "committer": {"name": "murmur-red", "email": "murmur.red1@gmail.com"},
    })
    res.raise_for_status()


if __name__ == "__main__":
    today = datetime.date.today()
    content = generate_post()
    filename, title = create_post_file(content, today)
    push_to_github(filename, title)
    print(f"Blog published: {filename}")

    lines = content.strip().split("\n")
    slug = re.sub(r"[^\w\s-]", "", lines[0].strip().strip('"').strip("'").lower())
    slug = re.sub(r"\s+", "-", slug)[:50].strip("-")
    publish_to_website(title, today, slug)
    print(f"Website updated: articles.json")
