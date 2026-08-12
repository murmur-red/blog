---
layout: post
title: "The Word \"Agent\" Is Doing Ninety Percent of the Work"
date: 2026-08-12
categories: tech
---

A dishwasher repair guy in Ohio pays for a tool that promises an "AI agent" will book his jobs, chase late payments, and answer customer texts. He gets charged forty dollars a month. What he actually gets is a program that reads a message, guesses a reply, checks if it looks wrong, and tries again until it stops looking wrong. That is not an agent. That is a while loop with a subscription.

Here is the plain version. An "agent," the way the industry sells it, is supposed to take a goal and figure out the steps on its own, like a smart assistant who books your whole trip while you sleep. What actually ships is much dumber. The software calls a language model, gets an answer, checks the answer against some rule, and if the answer fails it calls the model again. Loop. Retry. Loop again. The marketing calls this "reasoning." Your first-year programming class called it a retry loop.

Look at the numbers. Salesforce launched Agentforce in 2024 and hyped it hard. Then in 2025, Salesforce's own Gartner-cited research reported that only about a quarter of businesses had actually deployed AI agents, and that many pilots quit before they shipped. A study Carnegie Mellon ran with a fake company staffed by AI agents found the best model finished real office tasks correctly around 24% of the time. Twenty-four percent. If your dishwasher guy answered one in four customers correctly, he would be out of business by Thursday.

The honest counterargument: some agents do real work. Coding tools that write and re-run tests genuinely save time, because code either passes or it does not, and the retry loop has a clear judge. Fair. But that is exactly the point. Retrying works when a machine can check the answer. It falls apart when the answer is "did this customer feel heard," which no rule catches.

So before you pay for an "agent," ask one question. Who checks whether it got the job right? If the answer is nobody, you bought a loop wearing a blazer.
