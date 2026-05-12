---
name: wrapup
description: Daily progress tracking and documentation update for Debaz and Byso Global. Use this skill at the end of the day or when the user wants to "wrap up" to log progress in docs/progress_report.md and update docs/daily_tracker.csv and docs/plan.md.
---

# Wrap-up Workflow

This skill automates the end-of-day reporting for the Debaz & Byso Global portfolio. It ensures that progress is captured and the 6:2 time rule is maintained.

## Workflow Instructions

1.  **Gather Progress**: Prompt the user to provide a summary of the day's accomplishments.
    *   Ask for updates specifically for **Debaz** (Engineering Projects).
    *   Ask for updates specifically for **Byso Global** (Liaising/Trading/Diversified Projects).
    *   Ask for any blockers or changes in priorities.

2.  **Update `docs/progress_report.md`**:
    *   Read the current `docs/progress_report.md`.
    *   Append a new entry with the current date.
    *   Format the entry using the following template:
        ```markdown
        ## [YYYY-MM-DD]
        ### Debaz (Engineering - 6h Focus)
        - [Accomplishment 1]
        - [Accomplishment 2]

        ### Byso Global (Diversified - 2h Focus)
        - [Accomplishment 1]

        ### Blockers / Next Steps
        - [Blocker/Next Step]
        ```

3.  **Sync with `docs/daily_tracker.csv`**:
    *   Identify any mentions of new deals or status changes in the progress summary.
    *   Update the `Status`, `Next Action`, and `Description` columns in `docs/daily_tracker.csv` accordingly.
    *   If a new lead was mentioned, add a new row to the CSV.

4.  **Sync with `docs/plan.md`**:
    *   If a weekly task from `docs/plan.md` was completed, mark it as done or update the progress.
    *   If a task is delayed, note the reason and ensure the 6:2 balance is still reflected in the plan.

5.  **Final Summary**: Confirm to the user that all documents have been updated and provide a brief recap of the changes.

## Best Practices
*   Ensure the 6:2 time split is respected when suggesting next steps.
*   Keep the CSV formatting consistent.
*   Use concise bullet points for the progress report.
