# Python Automate - GitHub Actions Setup Guide

Complete guide to set up, run, and manage automated Python scripts using GitHub Actions.

## Table of Contents
1. [Initial Setup](#initial-setup)
2. [Creating the Python Script](#creating-the-python-script)
3. [Creating GitHub Actions Workflow](#creating-github-actions-workflow)
4. [Running the Workflow](#running-the-workflow)
5. [Checking Workflow Output](#checking-workflow-output)
6. [Scheduling the Workflow](#scheduling-the-workflow)
7. [Disabling/Pausing the Schedule](#disablingpausing-the-schedule)
8. [Troubleshooting](#troubleshooting)

---

## Initial Setup

### Prerequisites
- GitHub account
- GitHub repository created
- Python 3.10+ installed locally (for testing)

### Repository Structure
```
Python_Automate/
├── .github/
│   └── workflows/
│       └── run-popup.yml
├── popup.py
└── README.md
```

---

## Creating the Python Script

### Step 1: Create `popup.py`

1. Go to your repository: https://github.com/vasudvn606/Python_Automate
2. Click **Add file** → **Create new file**
3. Name it: `popup.py`
4. Add the following code:

```python
print("Hi")
```

5. Click **Commit changes**

**What this script does:**
- Prints "Hi" to the console
- This output will be visible in GitHub Actions logs

### Alternative: Add more functionality

```python
import datetime

print("Script started at:", datetime.datetime.now())
print("Hello from GitHub Actions!")
print("This runs automatically on schedule")
```

---

## Creating GitHub Actions Workflow

### Step 1: Create Workflow Directory Structure

The workflow file must be in `.github/workflows/` directory.

### Step 2: Create the Workflow File

1. Go to your repository: https://github.com/vasudvn606/Python_Automate
2. Click **Add file** → **Create new file**
3. Name it: `.github/workflows/run-popup.yml`
4. Paste the complete workflow file below:

### Complete Workflow File: `run-popup.yml`

```yaml
name: Run Popup Message Box

env:
  FORCE_JAVASCRIPT_ACTIONS_TO_NODE24: true

on:
  push:
    branches: [ main ]
  workflow_dispatch:
  schedule:
    - cron: '30 * * * *'

jobs:
  run-popup:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.10'
    
    - name: Run popup script
      run: |
        echo "Running popup script..."
        python popup.py
        echo "Script completed!"
```

5. Click **Commit changes**

### Workflow File Explanation

| Section | Purpose |
|---------|---------|
| `name:` | Display name of the workflow |
| `env:` | Sets Node.js 24 compatibility |
| `on:` | Defines triggers (when workflow runs) |
| `push:` | Runs when code is pushed to main branch |
| `workflow_dispatch:` | Allows manual trigger from GitHub UI |
| `schedule:` | Runs on a cron schedule (see [Scheduling](#scheduling-the-workflow)) |
| `jobs:` | Defines tasks to execute |
| `runs-on:` | Specifies the virtual machine (ubuntu-latest) |
| `steps:` | Individual commands to run |

---

## Running the Workflow

### Option 1: Automatic Trigger (Push to Main)

1. Make changes to your code
2. Commit and push to `main` branch
3. Workflow automatically runs

### Option 2: Manual Trigger (workflow_dispatch)

1. Go to your repository: https://github.com/vasudvn606/Python_Automate
2. Click the **Actions** tab
3. Click **Run Popup Message Box** on the left
4. Click **Run workflow** button
5. Select branch (main)
6. Click **Run workflow**

### Option 3: Scheduled Trigger (cron)

- Automatically runs every hour at :30 UTC (every hour IST)
- No manual action needed
- See [Scheduling](#scheduling-the-workflow) for more details

---

## Checking Workflow Output

### View All Workflow Runs

1. Go to your repository: https://github.com/vasudvn606/Python_Automate
2. Click the **Actions** tab
3. You'll see a list of all workflow runs

### View Specific Workflow Run Output

1. Click on a workflow run in the list
2. Click the **run-popup** job
3. Expand the **Run popup script** step
4. You'll see the console output:

```
Running popup script...
Hi
Script completed!
```

### Download Logs

1. In the workflow run details page
2. Click **Download logs** button (top right)
3. Logs will be downloaded as a zip file

### Live Monitoring

- Refresh the Actions page to see latest status
- Status shows: ⏳ In progress → ✅ Success or ❌ Failed

---

## Scheduling the Workflow

### Understanding Cron Schedule

The schedule `30 * * * *` means:

```
30 * * * *
│  │ │ │ │
│  │ │ │ └─ Day of week (0-6, 0=Sunday) - * = every day
│  │ │ └──── Month (1-12) - * = every month
│  │ └─────── Day of month (1-31) - * = every day
│  └──────── Hour (0-23) - * = every hour
└─────────── Minute (0-59) - 30 = at minute :30
```

**Result:** Runs every hour at :30 past UTC (every hour IST)

### Common Cron Schedules

| Schedule | Description |
|----------|-------------|
| `0 * * * *` | Every hour at minute 0 |
| `30 * * * *` | Every hour at minute 30 |
| `0 0 * * *` | Every day at midnight UTC |
| `0 9 * * *` | Every day at 9:00 AM UTC |
| `0 0 * * 0` | Every Sunday at midnight UTC |
| `0 0 1 * *` | First day of every month at midnight UTC |
| `*/15 * * * *` | Every 15 minutes |
| `0 */6 * * *` | Every 6 hours |

### Change the Schedule

1. Go to: https://github.com/vasudvn606/Python_Automate/blob/main/.github/workflows/run-popup.yml
2. Click **Edit** (pencil icon)
3. Find this line:
   ```yaml
   - cron: '30 * * * *'
   ```
4. Change to your desired cron schedule
5. Click **Commit changes**

### Time Zone Conversion

**GitHub Actions uses UTC timezone**

| IST Time | UTC Time | Cron |
|----------|----------|------|
| 12:00 AM | 6:30 PM (prev day) | `30 18 * * *` |
| 6:00 AM | 12:30 AM | `30 0 * * *` |
| 12:00 PM | 6:30 AM | `30 6 * * *` |
| 6:00 PM | 12:30 PM | `30 12 * * *` |

IST = UTC + 5:30 hours

---

## Disabling/Pausing the Schedule

### Option 1: Comment Out the Schedule (Recommended)

This keeps the code but disables the schedule temporarily.

1. Go to: https://github.com/vasudvn606/Python_Automate/blob/main/.github/workflows/run-popup.yml
2. Click **Edit** (pencil icon)
3. Find:
   ```yaml
   on:
     push:
       branches: [ main ]
     workflow_dispatch:
     schedule:
       - cron: '30 * * * *'
   ```

4. Comment it out with `#`:
   ```yaml
   on:
     push:
       branches: [ main ]
     workflow_dispatch:
     # schedule:
     #   - cron: '30 * * * *'
   ```

5. Click **Commit changes**

**To re-enable:** Remove the `#` symbols

### Option 2: Disable the Entire Workflow

1. Go to: https://github.com/vasudvn606/Python_Automate/actions
2. Click **run-popup** workflow
3. Click the **⋮** (three dots) menu → **Disable workflow**

**To re-enable:** Click the **⋮** menu → **Enable workflow**

### Option 3: Remove the Schedule Section Only

1. Go to: https://github.com/vasudvn606/Python_Automate/blob/main/.github/workflows/run-popup.yml
2. Click **Edit** (pencil icon)
3. Delete these lines:
   ```yaml
   schedule:
     - cron: '30 * * * *'
   ```

4. Click **Commit changes**

Workflow will still run on push and manual trigger, but not on schedule.

---

## Complete Workflow Examples

### Example 1: Daily at 9 AM UTC

```yaml
name: Daily Task

on:
  schedule:
    - cron: '0 9 * * *'

jobs:
  run-task:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-python@v5
      with:
        python-version: '3.10'
    - run: python popup.py
```

### Example 2: Every 6 Hours

```yaml
name: Every 6 Hours

on:
  schedule:
    - cron: '0 */6 * * *'

jobs:
  run-task:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-python@v5
      with:
        python-version: '3.10'
    - run: python popup.py
```

### Example 3: Multiple Schedules

```yaml
name: Multiple Schedules

on:
  schedule:
    - cron: '0 9 * * *'      # 9 AM UTC
    - cron: '0 17 * * *'     # 5 PM UTC

jobs:
  run-task:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-python@v5
      with:
        python-version: '3.10'
    - run: python popup.py
```

---

## Troubleshooting

### Issue: Workflow not running

**Solution:**
1. Check if workflow is disabled: Go to Actions → ⋮ menu → Enable workflow
2. Check if schedule syntax is correct using [crontab.guru](https://crontab.guru)
3. Verify `.github/workflows/run-popup.yml` file exists
4. Check for YAML syntax errors (indentation is critical)

### Issue: "No such file or directory: popup.py"

**Solution:**
- Ensure `popup.py` is in the repository root
- File path should be: `Python_Automate/popup.py`
- Run step should use: `python popup.py`

### Issue: Node.js 20 deprecation warning

**Solution:**
- Already handled in the workflow with: `FORCE_JAVASCRIPT_ACTIONS_TO_NODE24: true`
- This is just a warning, workflow still runs correctly

### Issue: Can't see output in logs

**Solution:**
1. Add `echo` statements before Python command
2. Expand the step in workflow run details
3. Scroll down to see all output
4. Use: `python -u popup.py` (unbuffered output)

### Issue: Workflow fails due to missing dependencies

**Solution:**
Add pip install step:
```yaml
- name: Install dependencies
  run: pip install -r requirements.txt

- name: Run popup script
  run: python popup.py
```

### Issue: Python version mismatch

**Solution:**
Specify Python version in workflow:
```yaml
- uses: actions/setup-python@v5
  with:
    python-version: '3.10'
```

---

## Quick Reference Commands

### Check Workflow Status
- **URL:** https://github.com/vasudvn606/Python_Automate/actions

### View Latest Run
- **URL:** https://github.com/vasudvn606/Python_Automate/actions/workflows/run-popup.yml

### Edit Workflow
- **URL:** https://github.com/vasudvn606/Python_Automate/blob/main/.github/workflows/run-popup.yml

### Cron Generator
- **Website:** https://crontab.guru

---

## Summary

### Setup Steps
1. ✅ Create `popup.py` with your Python code
2. ✅ Create `.github/workflows/run-popup.yml` with workflow configuration
3. ✅ Commit both files to repository
4. ✅ Go to Actions tab to verify

### Running Options
- **Manual:** Actions tab → Run workflow
- **Automatic:** Push to main branch
- **Scheduled:** Cron schedule (every hour IST by default)

### Monitoring
- Check Actions tab for all runs
- Click on any run to see detailed logs
- Logs show all echo statements and Python output

### Managing Schedule
- **Enable:** Remove `#` comments from schedule section
- **Disable:** Add `#` comments to schedule section
- **Change:** Update cron expression
- **Remove:** Delete schedule section entirely

---

## Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Workflow Syntax Reference](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)
- [Cron Expression Validator](https://crontab.guru)
- [Schedule Events in Workflows](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#schedule)

---

**Last Updated:** 2026-06-13
**Repository:** https://github.com/vasudvn606/Python_Automate
