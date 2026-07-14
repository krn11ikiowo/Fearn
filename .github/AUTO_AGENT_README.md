# 🤖 Copilot Auto Agent for Fearn

Automated bugfixes and feature implementation powered by GitHub Copilot.

## Overview

The Copilot Auto Agent automatically:
- **Fixes bugs** reported in GitHub issues
- **Implements small features** and enhancements
- **Improves code quality** through refactoring
- **Runs nightly maintenance** tasks
- **Creates pull requests** with comprehensive descriptions
- **Adds tests** for all changes

## How It Works

### 1. Issue-Triggered Processing
When a new issue is created or reopened with labels like `bug` or `enhancement`:
- The agent analyzes the issue
- Creates a branch with the fix/feature
- Opens a pull request automatically
- Comments on the issue with status updates

### 2. Nightly Runs
Every night at 2 AM UTC, the agent:
- Reviews open issues
- Identifies improvements
- Implements optimizations
- Updates dependencies
- Generates reports

### 3. Manual Trigger
You can manually trigger the agent via:
- GitHub Actions workflow_dispatch
- Labels on issues
- Workflow run button

## Configuration

### Labels That Trigger Auto-Processing
- `bug` - Automatic bugfix
- `enhancement` - Small feature implementation
- `good first issue` - Beginner-friendly fixes
- `help wanted` - Community issues

### Labels That Skip Processing
- `wontfix` - Will not be processed
- `duplicate` - Skip duplicates
- `invalid` - Skip invalid issues
- `on-hold` - Skip pending issues

## Pull Request Behavior

### Auto-Generated PRs Include:
✅ Detailed commit messages  
✅ Comprehensive test coverage  
✅ Code quality checks  
✅ Documentation updates  
✅ Closes issue reference  

### Review Process:
1. Agent creates draft PR for complex changes
2. All checks must pass
3. Manual approval required for merge
4. Auto-comments on issue with updates

## Configuration File

Edit `.github/copilot-agent-config.yml` to customize:

```yaml
issues:
  auto_process_labels:
    - "bug"
    - "enhancement"
  skip_labels:
    - "wontfix"

code_quality:
  min_coverage: 75
  auto_fix: true

schedule:
  nightly:
    enabled: true
    time: "02:00"
```

## Monitoring

### Track Agent Activity
```bash
# View workflow runs
gh run list --workflow copilot-auto-agent.yml

# View specific run
gh run view <run_id>

# View logs
gh run view <run_id> --log
```

### Metrics Tracked
- Issues processed
- Pull requests created
- Fixes merged
- Features implemented
- Average resolution time

## Best Practices

### For Issue Reporters
✅ Provide clear, detailed descriptions  
✅ Use appropriate labels  
✅ Include code examples if applicable  
✅ Specify expected vs actual behavior  

### For Maintainers
✅ Review auto-generated PRs promptly  
✅ Provide feedback on agent decisions  
✅ Adjust configuration based on results  
✅ Monitor code quality metrics  

### Disabling Auto-Processing
Add label: `auto-agent-skip` to issue to prevent automatic processing

## Common Issues

### PR Not Created
- Check if issue has auto-process label
- Verify workflow is enabled
- Check GitHub Actions logs

### Incorrect Implementation
- Provide more specific issue description
- Use related issues to provide context
- Comment on PR with corrections

### Too Many False Positives
- Adjust `max_complexity` setting
- Add more exclusions
- Use `on-hold` label temporarily

## Workflow Files

### Main Workflow
`.github/workflows/copilot-auto-agent.yml` - Orchestrates all agent tasks

### Configuration
`.github/copilot-agent-config.yml` - Agent behavior and settings

## Disabling the Agent

### Temporarily
Add label `auto-agent-skip` to issues

### Permanently
```bash
# Disable workflow
gh workflow disable copilot-auto-agent.yml

# Re-enable when ready
gh workflow enable copilot-auto-agent.yml
```

## Troubleshooting

### Check Workflow Status
1. Go to Actions tab in GitHub
2. Select "Copilot Auto Agent" workflow
3. View recent runs and logs

### View Last Run
```bash
gh run list --workflow copilot-auto-agent.yml --limit 1
```

### Debug Issues
Enable debug logging in workflow file:
```yaml
env:
  ACTIONS_STEP_DEBUG: true
```

## Support

For issues with the auto agent:
1. Check workflow logs
2. Review configuration file
3. File issue with `auto-agent` label
4. Include error messages and workflow run ID

## Statistics

Track success metrics:
- Total issues processed
- Successful fixes/features
- Average time to resolution
- Code quality improvements
- Test coverage changes

---

**Status**: ✅ Active  
**Last Updated**: 2026-07-14  
**Maintainer**: @krn11ikiowo
