# github_cleaner

## Introduction

A fast, lightweight GitHub Action (composite) that cleans up old resources from
your repositories, including workflow runs, deployments, artifacts, caches,
Pages deployments, packages, and release assets. Highly configurable with
sensible defaults.

## Features

- **Workflow Runs**: Delete all but the most recent workflow run
- **Deployments**: Delete inactive deployments
- **Artifacts**: Delete old Actions artifacts (configurable retention)
- **Caches**: Delete all Actions caches
- **Pages**: Delete old Pages deployments (keeps most recent)
- **Packages**: Delete old package versions from GitHub Container Registry
- **Release Assets**: Delete assets from old releases

## Quick Start

Add this workflow to `.github/workflows/cleanup.yml`:

```yaml
name: github_cleaner
on:
  schedule:
    - cron: "0 * * * *"  # Run hourly
jobs:
  clean:
    runs-on: ubuntu-latest
    permissions:
      actions: write
      deployments: write
    steps:
    - name: Clean old deployments and runs
      uses: nckslvrmn/github_cleaner@master
      with:
        token: ${{ secrets.GITHUB_TOKEN }}
```

## Configuration

All cleanup types are controlled via environment variables.

### Cleanup Toggles (true/false)

| Variable | Default | Description |
| -------- | ------- | ----------- |
| `CLEAN_WORKFLOW_RUNS` | `true` | Delete all but the most recent workflow run |
| `CLEAN_DEPLOYMENTS` | `true` | Delete inactive deployments |
| `CLEAN_ARTIFACTS` | `false` | Delete old Actions artifacts |
| `CLEAN_CACHES` | `false` | Delete all Actions caches |
| `CLEAN_PAGES` | `false` | Delete old Pages deployments (keeps most recent) |
| `CLEAN_PACKAGES` | `false` | Delete old package versions |
| `CLEAN_RELEASE_ASSETS` | `false` | Delete assets from old releases |

### Retention Settings (integers)

| Variable | Default | Description |
| -------- | ------- | ----------- |
| `KEEP_LATEST_ARTIFACTS` | `1` | Number of artifacts to keep per workflow |
| `KEEP_LATEST_PACKAGES` | `3` | Number of package versions to keep |
| `KEEP_LATEST_RELEASES` | `5` | Number of releases to keep assets for |

### Example Configurations

#### Default (Backward Compatible)

Only cleans workflow runs and inactive deployments:

```yaml
- uses: nckslvrmn/github_cleaner@master
  with:
    token: ${{ secrets.GITHUB_TOKEN }}
```

#### Cleanup More Content

Clean everything with custom retention:

```yaml
- uses: nckslvrmn/github_cleaner@master
  with:
    token: ${{ secrets.GITHUB_TOKEN }}
  env:
    CLEAN_ARTIFACTS: true
    CLEAN_CACHES: true
    CLEAN_PAGES: true
    KEEP_LATEST_ARTIFACTS: 2
```

#### Artifacts and Caches Only

Disable default cleaners, enable only artifacts and caches:

```yaml
- uses: nckslvrmn/github_cleaner@master
  with:
    token: ${{ secrets.GITHUB_TOKEN }}
  env:
    CLEAN_WORKFLOW_RUNS: false
    CLEAN_DEPLOYMENTS: false
    CLEAN_ARTIFACTS: true
    CLEAN_CACHES: true
```

## Permissions

Different cleanup types require different permissions:

| Cleanup Type | Required Permission |
| ------------ | ------------------- |
| Workflow runs | `actions: write` |
| Deployments | `deployments: write` |
| Artifacts | `actions: write` |
| Caches | `actions: write` |
| Pages | `pages: write` |
| Packages | `packages: write` |
| Release assets | `contents: write` |

Example with all permissions:

```yaml
permissions:
  actions: write
  deployments: write
  pages: write
  packages: write
  contents: write
```

## Local Testing

To test locally, first install dependencies:

```bash
cd /path/to/github_cleaner
pip install -r requirements.txt
```

Then run the cleaner:

```bash
export GITHUB_TOKEN=your_personal_access_token
export GITHUB_REPOSITORY=owner/repo
python3 clean.py
```

You can also set any configuration variables:

```bash
export CLEAN_ARTIFACTS=true
export KEEP_LATEST_ARTIFACTS=2
python3 clean.py
```
