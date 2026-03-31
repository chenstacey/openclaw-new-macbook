# Task Tracker Skill

## Description
Personal task management system with smart reminders. Tracks tasks by urgency, automates daily/weekly check-ins, and integrates with Obsidian.

## Usage

### Add Tasks
- "Add task: [description]"
- "New task: [description] due [date]"
- "Task: [description] - deciding"

### Check Tasks
- "Tasks" - Show all pending tasks
- "What do I need to do?" - Daily summary
- "Task status" - Full report

### Complete Tasks
- "Done #1" - Mark task complete
- "Complete task 2" - Mark by number
- "Finished [task name]" - Mark by name

### Task Types
| Type | Behavior |
|------|----------|
| **Urgent** | Daily reminders until done |
| **Deciding** | Visible in list, no nagging |
| **Recurring** | Auto-reschedules after completion |

## Automated Reminders

| Time | What |
|------|------|
| 8:00 AM | Podcast briefing |
| 9:00 AM | Task check (if pending urgent tasks) |
| Wednesday 9:00 AM | Insurance claim status check |
| Friday 6:00 PM | Weekly review + system suggestions |

## Obsidian Integration
- Saves to: `Task Tracker.md`
- Auto-updates with new/completed tasks
- Links to related notes (claims, podcasts, etc.)

## Examples

**Daily workflow:**
```
You: "Tasks"
Claw: "📋 2 pending tasks:
      1. Submit insurance claim (urgent)
      2. ESF school fee (deciding - due Sat)"

You: "Done #1"
Claw: "✅ Task 1 complete. 1 task remaining."
```

**Adding tasks:**
```
You: "New task: Call dentist to schedule cleaning"
Claw: "Added task #3. Due date?"

You: "Next week"
Claw: "✅ Task added: Call dentist - due 2026-03-03"
```

## Task Categories
- 🏥 Medical / Insurance
- 👶 School / Family
- 💼 Work
- 📅 Administrative
- 🎯 Personal

## Notes
- Tasks without due dates default to "this week"
- "Deciding" tasks stay visible but don't trigger daily reminders
- Completed tasks archived in tracker history
