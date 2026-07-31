---
layout: post
title: "Your AI Agent Is a While Loop Wearing a Blazer"
date: 2026-07-31
categories: tech
---

Here is a secret the AI industry does not want you to say out loud. Most "agents" shipping right now are the same code you wrote in your first programming class. Try something. It fails. Try again. Try again. Stop after ten tries. That is a retry loop. Add a language model to pick what to try next, slap the word "autonomous" on the slide deck, and now it costs money.

I am not exaggerating. Look at the actual benchmarks. On SWE-bench Verified, a test of 500 real GitHub bugs, the best agents crossed 70% in 2025 only by running the same task many times and keeping the answer that passes the tests. That technique has a name: pass@k. You give the model k attempts and grade it as a win if any single attempt works. That is a retry loop with a scoreboard. When Devin, the "first AI software engineer" from Cognition, got independently tested by the YouTube channel Internet of Bugs in 2024, it finished 3 of 20 tasks and often "solved" problems by inventing errors that were not there, then fixing its own inventions.

The honest counterargument: retry loops are useful. A human developer also tries things until the tests pass. True. But a human knows when they are lost and stops digging. Today's agents keep looping with total confidence, burning tokens, until a timer or a budget cap kills them. That is the difference between judgment and thrashing.

Think about who pays for this. A plumber buying a $200-a-month "AI scheduling agent" is not buying a colleague. He is buying a script that calls the model over and over until it gets a plausible reply, and he eats the API bill for every failed loop. Nobody tells him the "intelligence" is mostly retries he is funding.

So here is the point. An agent is not smart because it acts on its own. It is smart when it knows when to quit. Until these tools can say "I don't know, ask a human," they are automated persistence, not automated thinking. Before you pay for one, ask what it does when it is wrong. Right now, the answer is: it tries again.
