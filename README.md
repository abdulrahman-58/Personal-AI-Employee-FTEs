# Personal AI Employee - Bronze Tier

> **Your life and business on autopilot. Local-first, agent-driven, human-in-the-loop.**

This is a **Bronze Tier** implementation of the Personal AI Employee hackathon. It provides the foundational layer for an autonomous AI agent that manages your personal and business affairs using Qwen Code and Obsidian.

## What This Does

- 📁 **File Drop Processing**: Drop any file into the Inbox folder, and the AI will process it
- 📊 **Dashboard**: Real-time view of pending tasks and completed work
- 📖 **Company Handbook**: Rules and guidelines for your AI employee
- 🎯 **Business Goals**: Track objectives and metrics

## Prerequisites

| Software | Version | Purpose |
|----------|---------|---------|
| [Python](https://www.python.org/downloads/) | 3.13+ | Watcher scripts |
| [Qwen Code](https://github.com/anthropics/qwen-code) | Latest | AI reasoning engine |
| [Obsidian](https://obsidian.md/download) | v1.10.6+ | Knowledge base (optional for viewing) |

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env if needed (defaults work for Bronze tier)
```

### 3. Verify Vault Structure

The Obsidian vault is already created at `./AI_Employee_Vault/` with these folders:

```
AI_Employee_Vault/
├── Dashboard.md          # Main status view
├── Company_Handbook.md   # Rules of engagement
├── Business_Goals.md     # Objectives and metrics
├── Inbox/                # Drop files here for processing
├── Needs_Action/         # Auto-created action items
├── Plans/                # AI-generated plans
├── Done/                 # Completed tasks
├── Pending_Approval/     # Awaiting your approval
├── Approved/             # Ready to execute
├── Rejected/             # Declined items
├── Logs/                 # System logs
├── Accounting/           # Financial records
├── Briefings/            # CEO briefings
└── Invoices/             # Invoice files
```

### 4. Start the File System Watcher

```bash
# From the project root directory
python watchers/filesystem_watcher.py --vault ./AI_Employee_Vault
```

The watcher will:
- Monitor the `Inbox/` folder for new files
- Create action files in `Needs_Action/` when files are dropped
- Log all activity to `Logs/`

### 5. Use Qwen Code to Process Tasks

Open a new terminal and run:

```bash
cd AI_Employee_Vault
qwen
```

Then prompt Qwen Code:

```
Check the Needs_Action folder and process any pending items.
Create a plan for each item and move completed tasks to Done.
Update the Dashboard.md with current status.
```

## Usage Examples

### Example 1: Process a Document

1. Drop a file into `AI_Employee_Vault/Inbox/`:
   ```bash
   echo "Meeting notes from today..." > AI_Employee_Vault/Inbox/meeting_notes.txt
   ```

2. The watcher detects it and creates an action file in `Needs_Action/`

3. Ask Qwen to process:
   ```bash
   cd AI_Employee_Vault && qwen "Summarize the meeting notes and extract action items"
   ```

### Example 2: Batch Process

Drop multiple files into `Inbox/` and then:

```bash
cd AI_Employee_Vault
qwen "Process all files in Needs_Action folder. For each file:
1. Read and understand what's needed
2. Create a plan in /Plans
3. Execute the plan
4. Move to /Done when complete
5. Update Dashboard.md"
```

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `VAULT_PATH` | `./AI_Employee_Vault` | Path to Obsidian vault |
| `FILE_WATCHER_INTERVAL` | `5` | Seconds between file checks |
| `DRY_RUN` | `true` | If true, no external actions |

### Watcher Options

```bash
# Custom vault path
python watchers/filesystem_watcher.py --vault /path/to/vault

# Custom check interval
python watchers/filesystem_watcher.py --interval 10

# Combined
python watchers/filesystem_watcher.py -v ./AI_Employee_Vault -i 5
```

## Bronze Tier Deliverables Checklist

- [x] Obsidian vault with `Dashboard.md` and `Company_Handbook.md`
- [x] One working Watcher script (File System monitoring)
- [x] Qwen Code reads from and writes to the vault
- [x] Basic folder structure: `/Inbox`, `/Needs_Action`, `/Done`
- [ ] All AI functionality implemented as Agent Skills (optional enhancement)

## Next Steps (Silver Tier)

To upgrade to Silver tier, add:

1. **Gmail Watcher**: Monitor Gmail for important emails
2. **WhatsApp Watcher**: Monitor WhatsApp for urgent messages
3. **MCP Server**: Send emails automatically
4. **HITL Workflow**: Approval system for sensitive actions
5. **Scheduling**: Cron jobs for regular processing

## Troubleshooting

### Watcher not detecting files

- Ensure the watcher is running (`python watchers/filesystem_watcher.py`)
- Check logs in `AI_Employee_Vault/Logs/`
- Verify file permissions on the Inbox folder

### Qwen Code not found

```bash
# Install Qwen Code globally
npm install -g @anthropics/qwen-code

# Verify installation
qwen --version
```

### Action files not being created

- Check that `Needs_Action/` folder exists
- Verify the watcher has write permissions
- Check the state file in `Logs/filesystem_watcher_state.json`

## Security Notes

- ⚠️ **Never commit `.env`** - Contains configuration that may include secrets
- ⚠️ **Credentials stay local** - API keys in `.env`, never in the vault
- ⚠️ **Review before approving** - Always check AI actions in `Pending_Approval/`

## Project Structure

```
Personal-AI-Employee-FTEs/
├── AI_Employee_Vault/       # Obsidian vault (created)
├── watchers/
│   ├── base_watcher.py      # Base class for all watchers
│   └── filesystem_watcher.py # File system watcher (Bronze)
├── requirements.txt          # Python dependencies
├── .env.example             # Environment template
├── .gitignore               # Git ignore rules
└── README.md                # This file
```

## Resources

- [Full Hackathon Document](./Personal%20AI%20Employee%20Hackathon%200_%20Building%20Autonomous%20FTEs%20in%202026.md)
- [Qwen Code Docs](https://platform.qwen.com/docs)
- [Obsidian Help](https://help.obsidian.md)
- [Agent Skills](https://platform.qwen.com/docs/en/agents-and-tools/agent-skills/overview)

## Meeting Information

Weekly Research & Showcase: **Wednesdays 10:00 PM PKT**

- **Zoom**: Meeting ID 871 8870 7642, Passcode 744832
- **YouTube Backup**: https://www.youtube.com/@panaversity

---

*Built as part of the Personal AI Employee Hackathon 0*
*Bronze Tier Implementation - 2026*
