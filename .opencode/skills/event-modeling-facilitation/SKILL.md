---
name: event-modeling-facilitation
description: Event Modeling workflow facilitation; use when the user wants to model a workflow, discover behavior, or turn a business process into an event model.
---

# Event Modeling Facilitation

Use this skill to guide a workflow modeling session from plain-language conversation to an Event Modeling artifact.

## Core Stance

The user does not need to speak Event Modeling vocabulary. Facilitate in business language first. Treat Event Modeling as the internal method you use to structure the conversation and final model.

Keep the discussion focused on the domain:

- real-world workflow
- people and roles involved
- business goals
- visible outcomes
- decisions and rules
- evidence that something happened
- information needed at each step
- exceptions and alternate flows

Do not start by asking for commands, events, read models, slices, or GWTs. If the user uses those terms, respond in kind. If the user asks what a term means, explain it briefly.

## Adaptive Teaching

At the start of a substantial modeling session, calibrate gently:

`How familiar are you with Event Modeling: new to it, comfortable, or experienced?`

If asking would interrupt momentum, infer from the user's language and adjust.

For each major concept, explain it once when it first becomes useful:

- Event: a fact the system remembers happened.
- Command: something a person or process asks the system to do.
- Read model: information the system shows or uses to make a decision.
- State change: a request that changes what the system remembers.
- State view: stored facts projected into something visible or queryable.
- Automation: something the system does by itself after a trigger.
- Translation: information crossing the boundary to or from another system, file, API, or external process.
- Given/When/Then: a concrete example of a rule for a state-changing action.
- Given/Then: a concrete example of what a view should show after known facts.
- Information completeness: checking where every needed piece of data comes from.

After the first explanation, use short terms. Re-explain only when asked, when the user appears uncertain, or when a modeling mistake suggests the concept needs reinforcement.

## Conversation Flow

Use this sequence, but do not make it feel like a form.

1. Scope the workflow.
Ask what workflow or use case they want to understand. Identify the starting point, ending point, and what success looks like.

2. Elicit the story.
Ask simple sequencing questions:

- What starts this process?
- Who is involved?
- What happens next?
- After that, what should be true?
- What does the person see or need to know at that point?
- How do you know that happened?
- What information is written down or remembered?
- What can go wrong?
- What should happen when that goes wrong?

3. Capture facts in past tense.
Internally translate "what happened" answers into candidate events. Prefer past-tense names like `RepairTicketOpened`, `PaymentFailed`, or `LessonSelected`.

If the user gives an action like "approve repair," ask what fact should be true afterward: "After someone approves it, what would you say happened?"

4. Arrange the timeline.
Confirm the story left-to-right in plain language. Look for missing transitions, loops, alternate flows, and unclear ordering.

5. Discover views and needed information.
Ask what each person or process sees, chooses from, or needs to know. Work backward from visible data to stored facts.

6. Discover actions.
For each remembered fact, ask what person, process, timer, or external input caused it. Internally map these to commands, automations, or translations.

7. Identify rules with examples.
Ask for concrete examples:

- What is the simplest successful case?
- What is a case that should be rejected?
- What is the boundary case?
- What should the screen or report show after these things happened?

Translate state-changing examples into Given/When/Then. Translate view examples into Given/Then.

8. Check information completeness.
For every field on an event or view, ask where it comes from. Accept only these source categories in the final JSON: command input, generated value, external input, read model value, or prior event attribute for read-model fields.

9. Summarize before writing.
Before editing JSON, summarize in plain language and list the model elements you intend to create. Ask a focused confirmation question if there is unresolved ambiguity.

## Internal Mapping Heuristics

Map business language to modeling concepts without forcing the vocabulary on the user:

- "They clicked/submitted/asked for..." usually indicates a command.
- "Now there is a record/fact/status/history..." usually indicates an event.
- "They can see/filter/choose from..." usually indicates a read model.
- "The system automatically..." usually indicates an automation.
- "Another system sends/tells us/imports..." usually indicates a translation or external input.
- "Only if/as long as/cannot/must..." usually indicates a scenario or business rule.

## Facilitation Rules

- Prefer specific examples over abstract agreement.
- Do not invent business rules. Ask for them or mark them as open questions.
- Keep alternate flows separate when they would clutter the main success path.
- Model one coherent workflow at a time.
- Do not discuss implementation technology unless needed to clarify an external boundary or data source.
- When stuck, return to the story: what happened before this, and what should happen after?
