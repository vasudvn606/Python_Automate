# Python Automate - GitLab CI/CD Setup Guide

Complete guide to set up, run, and manage automated Python scripts using GitLab CI/CD.

## Table of Contents
1. [Initial Setup](#initial-setup)
2. [Creating the Python Script](#creating-the-python-script)
3. [Creating GitLab CI/CD Pipeline](#creating-gitlab-cicd-pipeline)
4. [Running the Pipeline](#running-the-pipeline)
5. [Checking Pipeline Output](#checking-pipeline-output)
6. [Scheduling the Pipeline](#scheduling-the-pipeline)
7. [Disabling/Pausing the Schedule](#disablingpausing-the-schedule)
8. [Troubleshooting](#troubleshooting)

---

## Initial Setup

### Prerequisites
- GitLab account
- GitLab repository created
- Python 3.10+ installed locally (for testing)
- GitLab Runner configured (or use shared runners)

### Repository Structure
```
Python_Automate/
├── .gitlab-ci.yml
├── popup.py
└── README.md
```

---

## Creating the Python Script

### Step 1: Create `popup.py`

1. Go to your GitLab repository
2. Click **+ (New file)** → **New file**
3. Name it: `popup.py`
4. Add the following code:

```python
print("Hi")
```

5. Click **Commit changes**

**What this script does:**
- Prints "Hi" to the console
- This output will be visible in GitLab CI/CD logs

### Alternative: Add more functionality

```python
import datetime

print("Script started at:", datetime.datetime.now())
print("Hello from GitLab CI/CD!")
print("This runs automatically on schedule")
```

---

## Creating GitLab CI/CD Pipeline

### Step 1: Create the Pipeline Configuration File

1. Go to your GitLab repository
2. Click **+ (New file)** → **New file**
3. Name it: `.gitlab-ci.yml`
4. Paste the complete pipeline configuration below:

### Complete Pipeline File: `.gitlab-ci.yml`

```yaml
# GitLab CI/CD Pipeline Configuration
# Python Automation Script

stages:
  - run

variables:
  PYTHON_VERSION: "3.10"

run_popup:
  stage: run
  image: python:${PYTHON_VERSION}
  script:
    - echo "Running popup script..."
    - python popup.py
    - echo "Script completed!"
  only:
    - main
    - web  # Allow manual trigger
    - schedules  # Allow scheduled runs
  tags:
    - docker

# Schedule job for hourly execution (every hour at :30 UTC / every hour IST)
run_popup_scheduled:
  stage: run
  image: python:${PYTHON_VERSION}
  script:
    - echo "Running scheduled popup script..."
    - python popup.py
    - echo "Scheduled script completed!"
  only:
    - schedules
  tags:
    - docker
```

5. Click **Commit changes**

### Pipeline File Explanation

| Section | Purpose |
|---------|---------|
| `stages:` | Defines pipeline stages (jobs run in order) |
| `variables:` | Environment variables (PYTHON_VERSION) |
| `run_popup:` | Job name - runs on push/merge to main |
| `stage:` | Which stage this job belongs to |
| `image:` | Docker image to use (python:3.10) |
| `script:` | Commands to execute |
| `only:` | When this job runs (branches/events) |
| `tags:` | Runner tags to use |
| `schedules:` | Enables scheduled pipeline runs |
| `run_popup_scheduled:` | Separate job for scheduled runs |

---

## Running the Pipeline

### Option 1: Automatic Trigger (Push to Main)

1. Make changes to your code
2. Commit and push to `main` branch
3. Pipeline automatically runs

**View result:**
- Go to **CI/CD** → **Pipelines**
- Click on latest pipeline
- Click **run_popup** job to see logs

### Option 2: Manual Trigger (Web)

1. Go to your GitLab repository
2. Click **CI/CD** → **Pipelines**
3. Click **Run pipeline** button
4. Select branch: `main`
5. Click **Run pipeline**

**View result:**
- Pipeline starts immediately
- See logs in real-time

### Option 3: Scheduled Trigger

- Automatically runs on a schedule (configured separately)
- See [Scheduling](#scheduling-the-pipeline) for setup
- Dedicated `run_popup_scheduled` job runs on schedule

---

## Checking Pipeline Output

### View All Pipeline Runs

1. Go to your GitLab repository
2. Click **CI/CD** → **Pipelines**
3. You'll see a list of all pipeline runs

### View Specific Pipeline Job Output

1. Click on a pipeline in the list
2. Click the **run_popup** or **run_popup_scheduled** job
3. You'll see the console output:

```
Running popup script...
Hi
Script completed!
```

### Pipeline Status Indicators

| Icon | Meaning |
|------|---------|
| ✅ | Success |
| ❌ | Failed |
| ⏳ | Running |
| ⏸ | Skipped |
| 🔄 | Pending |

### Download Logs

1. In the job details page
2. Click **Download** button (top right)
3. Logs will be downloaded as a text file

### Real-time Monitoring

- Watch job progress in real-time
- See output as it's printed
- Auto-refresh available

---

## Scheduling the Pipeline

### Step 1: Create a Pipeline Schedule

1. Go to your GitLab repository
2. Click **CI/CD** → **Schedules**
3. Click **New schedule** button

### Step 2: Configure the Schedule

**Fill in the form:**

| Field | Value |
|-------|-------|
| **Description** | Hourly Popup Script |
| **Cron** | `30 * * * *` |
| **Timezone** | UTC (or your timezone) |
| **Target branch** | `main` |
| **Active** | ✅ (checked) |

4. Click **Create pipeline schedule**

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

### Time Zone Conversion

**GitLab uses UTC timezone by default**

| IST Time | UTC Time | Cron |
|----------|----------|------|
| 12:00 AM | 6:30 PM (prev day) | `30 18 * * *` |
| 6:00 AM | 12:30 AM | `30 0 * * *` |
| 12:00 PM | 6:30 AM | `30 6 * * *` |
| 6:00 PM | 12:30 PM | `30 12 * * *` |

IST = UTC + 5:30 hours

### Edit an Existing Schedule

1. Go to **CI/CD** → **Schedules**
2. Click the **Edit** button (pencil icon)
3. Modify the cron expression or settings
4. Click **Save pipeline schedule**

### View Schedule History

1. Go to **CI/CD** → **Schedules**
2. Click on a schedule
3. See all past executions
4. View logs for each run

---

## Disabling/Pausing the Schedule

### Option 1: Disable the Schedule (Recommended)

1. Go to your GitLab repository
2. Click **CI/CD** → **Schedules**
3. Find your schedule
4. Click the **Toggle** button to disable
5. Icon changes to ⏸ (paused)

**To re-enable:** Click the toggle button again

### Option 2: Delete the Schedule

1. Go to **CI/CD** → **Schedules**
2. Find your schedule
3. Click the **Delete** button (trash icon)
4. Confirm deletion

**To restore:** Create a new schedule with same settings

### Option 3: Modify the Pipeline Configuration

Edit `.gitlab-ci.yml` to remove the `schedules` trigger:

1. Go to your repository
2. Click `.gitlab-ci.yml` file
3. Click **Edit**
4. Remove `schedules` from the `only:` section:

**Before:**
```yaml
only:
  - main
  - web
  - schedules
```

**After:**
```yaml
only:
  - main
  - web
```

5. Click **Commit changes**

Now the job won't run on scheduled triggers, but manual runs still work.

---

## Complete Pipeline Examples

### Example 1: Daily at 9 AM UTC

```yaml
stages:
  - run

run_daily:
  stage: run
  image: python:3.10
  script:
    - echo "Running daily task..."
    - python popup.py
    - echo "Daily task completed!"
  only:
    - schedules
  tags:
    - docker
```

**Schedule Setup:**
- Cron: `0 9 * * *`
- Branch: main
- Active: ✅

### Example 2: Every 6 Hours

```yaml
stages:
  - run

run_every_6_hours:
  stage: run
  image: python:3.10
  script:
    - echo "Running 6-hourly task..."
    - python popup.py
    - echo "6-hourly task completed!"
  only:
    - schedules
  tags:
    - docker
```

**Schedule Setup:**
- Cron: `0 */6 * * *`
- Branch: main
- Active: ✅

### Example 3: Multiple Schedules with Different Jobs

```yaml
stages:
  - run

run_morning:
  stage: run
  image: python:3.10
  script:
    - echo "Morning task..."
    - python popup.py
  only:
    - schedules
  tags:
    - docker

run_evening:
  stage: run
  image: python:3.10
  script:
    - echo "Evening task..."
    - python popup.py
  only:
    - schedules
  tags:
    - docker
```

**Create two schedules:**
1. Morning: Cron `0 6 * * *`
2. Evening: Cron `0 18 * * *`

---

## Troubleshooting

### Issue: Pipeline not running

**Solution:**
1. Check if `.gitlab-ci.yml` file exists in repository root
2. Verify YAML syntax (indentation is critical)
3. Check **CI/CD** → **Schedules** - is schedule active?
4. Verify runner is available (green status)

### Issue: "No such file or directory: popup.py"

**Solution:**
- Ensure `popup.py` is in the repository root
- File path should be: `Python_Automate/popup.py`
- Script command should use: `python popup.py`

### Issue: Job fails due to missing Python modules

**Solution:**
Add pip install step:
```yaml
script:
  - pip install -r requirements.txt
  - python popup.py
```

Create `requirements.txt`:
```
requests==2.28.0
numpy==1.23.0
```

### Issue: Can't see job output

**Solution:**
1. Job must have completed (check status)
2. Click on the job name in pipeline view
3. Scroll to bottom of logs
4. Use `cat` command to display output:
   ```yaml
   script:
     - echo "Output:" && python popup.py
   ```

### Issue: Schedule not running at expected time

**Solution:**
1. Check timezone setting in schedule
2. Verify cron expression at [crontab.guru](https://crontab.guru)
3. Check GitLab runner status (must be online)
4. Verify runner tags match job tags

### Issue: "Runner not available"

**Solution:**
1. Go to **Admin** → **Runners** (or **CI/CD** → **Runners**)
2. Check if runners are online
3. Ensure runner tags match job tags
4. Use `docker` tag for shared runners

### Issue: Permission denied error

**Solution:**
1. Ensure you have push access to repository
2. Check branch protection rules
3. Verify GitLab user has CI/CD permissions
4. Check runner permissions

---

## Quick Reference Commands

### Access CI/CD
- **URL:** Repository → **CI/CD** menu

### View Pipelines
- **URL:** Repository → **CI/CD** → **Pipelines**

### View Schedules
- **URL:** Repository → **CI/CD** → **Schedules**

### Edit Pipeline Configuration
- **File:** `.gitlab-ci.yml`
- **Location:** Repository root

### Create New Schedule
- **Steps:** CI/CD → Schedules → New schedule → Fill form → Create

### Cron Validator
- **Website:** https://crontab.guru

---

## Comparison: GitHub Actions vs GitLab CI/CD

| Feature | GitHub Actions | GitLab CI/CD |
|---------|---|---|
| Config File | `.github/workflows/*.yml` | `.gitlab-ci.yml` |
| Triggers | `on:` section | `only:` section |
| Manual Trigger | `workflow_dispatch:` | Web UI → Run pipeline |
| Scheduling | `schedule:` with cron | Separate schedules menu |
| Status Display | Actions tab | Pipelines page |
| Logs | In-step logs | Job logs |
| Docker Support | Yes | Primary method |
| Free Tier | 2000 minutes/month | 400 minutes/month |
| Runners | GitHub-hosted | GitLab-hosted + self-hosted |

---

## Summary

### Setup Steps
1. ✅ Create `popup.py` with your Python code
2. ✅ Create `.gitlab-ci.yml` with pipeline configuration
3. ✅ Commit both files to repository
4. ✅ Create schedule in **CI/CD** → **Schedules**
5. ✅ Go to **Pipelines** to verify

### Running Options
- **Manual:** CI/CD → Pipelines → Run pipeline
- **Automatic:** Push to main branch
- **Scheduled:** Create schedule with cron

### Monitoring
- Check **CI/CD** → **Pipelines** for all runs
- Click on any pipeline to see jobs
- Click on job to see detailed logs

### Managing Schedule
- **Enable:** Toggle schedule switch ON
- **Disable:** Toggle schedule switch OFF
- **Change:** Edit schedule → Update cron
- **Delete:** Delete schedule (can recreate)

---

## Additional Resources

- [GitLab CI/CD Documentation](https://docs.gitlab.com/ee/ci/)
- [GitLab CI/CD YAML Reference](https://docs.gitlab.com/ee/ci/yaml/)
- [Pipeline Schedules](https://docs.gitlab.com/ee/ci/scheduled_pipelines.html)
- [Cron Expression Validator](https://crontab.guru)
- [Docker Images on Docker Hub](https://hub.docker.com/)

---

## Key Differences from GitHub Actions

### 1. Configuration File
- **GitHub:** `.github/workflows/run-popup.yml`
- **GitLab:** `.gitlab-ci.yml` (single file for all pipelines)

### 2. Job Syntax
- **GitHub:** `jobs: → run-popup: → steps:`
- **GitLab:** Direct job definition with `stage:` and `script:`

### 3. Scheduling
- **GitHub:** Built into workflow file with `schedule:`
- **GitLab:** Separate UI menu **CI/CD** → **Schedules**

### 4. Docker
- **GitHub:** Optional, runs on virtual machines by default
- **GitLab:** Primary method, uses Docker images

### 5. Manual Trigger
- **GitHub:** `workflow_dispatch:` in YAML
- **GitLab:** UI button **Run pipeline**

---

**Last Updated:** 2026-06-13
**Repository Type:** GitLab
