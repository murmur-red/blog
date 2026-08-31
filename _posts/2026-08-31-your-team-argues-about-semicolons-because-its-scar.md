---
layout: post
title: "Your Team Argues About Semicolons Because It's Scared to Argue About Logic"
date: 2026-08-31
categories: tech
---

Pull up your last ten code reviews. Count the comments. I did this on a project once and the split was ugly: about seven out of every ten notes were about style. Rename this variable. Move this bracket. Add a blank line here. Maybe two were actual questions about whether the code did the right thing. The rest were "looks good to me" stamped on 400 lines nobody read.

That ratio is not a coincidence. It tells you exactly what your team is comfortable doing and what it is avoiding.

Style comments are cheap. Anyone can spot an inconsistent indent. You don't need to understand the feature, the edge cases, or the database schema to say "we use camelCase here." It feels like work. It looks like rigor. It is neither. It is the review equivalent of straightening the picture frames while the kitchen is on fire.

Correctness comments are expensive. To say "this breaks when the input is empty" you have to actually run the logic in your head. You have to know the system. You have to risk being wrong in front of a colleague. Most people would rather nitpick a naming convention than admit they don't fully understand the change they're approving.

Google noticed this years ago. Their engineering team built an auto-formatter and a linter directly into the pipeline so machines handle whitespace and naming before a human ever looks. The point was blunt: stop wasting your best engineers on tab-versus-space debates and free them to check whether the thing works. When a bot owns style, style comments vanish, and what's left is the hard stuff.

Here's the counterargument. Style matters too. Consistent code is easier to read, and readable code has fewer bugs over time. True. So automate it. A machine enforces style perfectly and never gets defensive. A human who spends review energy on formatting is a human dodging the real job.

Look at your ratio. If it leans style, your team isn't careful. It's frightened, or it's checked out. Buy a linter, delete the easy comments, and see who still has something to say about whether the code is actually correct.
