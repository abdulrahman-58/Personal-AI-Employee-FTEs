# Project Context: Personal AI Employee FTEs

## Project Overview

This repository contains a comprehensive architectural blueprint and hackathon guide for building a **"Digital FTE" (Full-Time Equivalent)** — an autonomous AI agent that manages personal and business affairs 24/7. The project uses **Qwen Code** as the reasoning engine and **Obsidian** as the local-first knowledge base/dashboard.

**Core Concept:** Transform Qwen Code from a reactive chatbot into a proactive employee that:
- Monitors Gmail, WhatsApp, and filesystem events via "Watcher" scripts
- Reasons about tasks and creates action plans
- Executes actions through MCP (Model Context Protocol) servers
- Requires human approval for sensitive operations (payments, emails to new contacts)

**Key Innovation:** The "Monday Morning CEO Briefing" — where the AI autonomously audits bank transactions and tasks to report revenue and bottlenecks.

## Directory Structure

```
Personal-AI-Employee-FTEs/
├── Personal AI Employee Hackathon 0_ Building Autonomous FTEs in 2026.md  # Main architecture doc (1201 lines)
├── skills-lock.json          # Qwen skill dependencies
├── .gitattributes            # Git text file settings
├── QWEN.md                   # This file - project context
└── .qwen/skills/
    └── browsing-with-playwright/  # Installed Qwen skill for browser automation
```

## Key Concepts & Architecture

### The Four Layers

1. **Perception (Watchers):** Lightweight Python scripts monitoring external inputs
   - Gmail Watcher (Google API)
   - WhatsApp Watcher (Playwright-based)
   - File System Watcher (watchdog library)

2. **Memory/GUI (Obsidian):** Local Markdown vault structure
   - `/Needs_Action/` — New items requiring processing
   - `/Plans/` — AI-generated action plans
   - `/Pending_Approval/` — Actions awaiting human approval
   - `/Approved/` — Ready-to-execute actions
   - `/Done/` — Completed tasks
   - `Dashboard.md` — Real-time status summary
   - `Company_Handbook.md` — Rules of engagement
   - `Business_Goals.md` — Objectives and metrics

3. **Reasoning (Qwen Code):** The brain that reads, thinks, plans, and writes

4. **Action (MCP Servers):** Model Context Protocol servers for external actions
   - Email MCP (send/draft emails)
   - Browser MCP (web automation via Playwright)
   - Calendar MCP (scheduling)
   - Custom MCPs (banking, payments, social media)

### Critical Patterns

**Ralph Wiggum Loop:** A Stop hook pattern that keeps Qwen iterating until multi-step tasks are complete. Intercepts Qwen's exit and re-injects prompts until the task file is moved to `/Done/`.

**Human-in-the-Loop (HITL):** Sensitive actions create approval request files. AI never executes until a human moves the file from `/Pending_Approval/` to `/Approved/`.

**Claim-by-Move Rule:** Prevents double-work in multi-agent scenarios. First agent to move a task to `/In_Progress/<agent>/` owns it.

## Hackathon Tiers

| Tier | Time | Deliverables |
|------|------|--------------|
| **Bronze** | 8-12h | Obsidian vault, 1 Watcher, basic Qwen integration |
| **Silver** | 20-30h | Multiple Watchers, MCP server, HITL workflow, scheduling |
| **Gold** | 40+h | Full integration, Odoo accounting, Ralph Wiggum loop, audit logging |
| **Platinum** | 60+h | Cloud deployment, domain specialization, 24/7 always-on |

## Tech Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| Reasoning Engine | Qwen Code | Primary AI/LLM interface |
| Knowledge Base | Obsidian | Local Markdown dashboard |
| Automation | Python 3.13+ | Watcher scripts, orchestration |
| Web Automation | Playwright | WhatsApp, browser-based actions |
| External APIs | MCP Servers | Email, calendar, payments |
| Process Management | PM2/supervisord | Keep watchers running 24/7 |
| Version Control | Git/GitHub Desktop | Vault versioning |

## Building & Running (Typical Setup)

### Prerequisites
```bash
# Install core tools
npm install -g @anthropics/qwen-code
pip install playwright watchdog google-api-python-client
playwright install
```

### Typical Workflow
1. **Setup Obsidian Vault:** Create folder structure (`Inbox/`, `Needs_Action/`, `Done/`, etc.)
2. **Configure MCP Servers:** Set up credentials in `~/.config/qwen-code/mcp.json`
3. **Start Watchers:** Run watcher scripts (or use PM2 for persistence)
4. **Launch Qwen:** Point Qwen Code at the vault directory
5. **Enable Ralph Wiggum:** Configure Stop hook for autonomous loops

### Example: Start Watchers with PM2
```bash
pm2 start gmail_watcher.py --interpreter python3
pm2 start whatsapp_watcher.py --interpreter python3
pm2 start orchestrator.py --interpreter python3
pm2 save
pm2 startup
```

## Development Conventions

### Security Principles
- **Never store credentials in vault** — use environment variables or secrets manager
- **Dry-run mode** — all action scripts support `--dry-run` flag
- **Audit logging** — every action logged to `/Vault/Logs/YYYY-MM-DD.json`
- **Permission boundaries** — auto-approve only low-risk actions (<$50, known contacts)

### File Naming Conventions
- `TYPE_description_date.md` — e.g., `EMAIL_invoice_client_a_2026-01-07.md`
- Timestamps in ISO 8601 format
- YAML frontmatter for metadata

### Testing Practices
- Test in `DEV_MODE` with sandbox accounts first
- Implement exponential backoff retry logic for transient errors
- Watchdog process monitors and restarts failed watchers

## Installed Skills

- **browsing-with-playwright:** Browser automation skill for web-based actions (WhatsApp Web, payment portals, etc.)

## Key Reference Files

| File | Purpose |
|------|---------|
| `Personal AI Employee Hackathon 0_...md` | Complete architecture spec, templates, examples, troubleshooting |
| `skills-lock.json` | Qwen skill dependency lock file |

## Common Commands

```bash
# Check Qwen Code installation
qwen --version

# Start Qwen in vault directory
cd /path/to/vault && qwen

# Run watcher in dry-run mode
DRY_RUN=true python gmail_watcher.py

# View PM2 process status
pm2 status

# Check logs
tail -f /path/to/vault/Logs/2026-01-07.json
```

## External Resources

- **Qwen Code Docs:** https://platform.qwen.com/docs
- **MCP Specification:** https://modelcontextprotocol.io
- **Obsidian:** https://obsidian.md
- **Playwright:** https://playwright.dev
- **Odoo API (for Gold tier):** https://www.odoo.com/documentation/19.0/developer/reference/external_api.html

## Meeting Information

Weekly Research & Showcase: Wednesdays 10:00 PM PKT on Zoom
- Meeting ID: 871 8870 7642
- Passcode: 744832
- YouTube Backup: https://www.youtube.com/@panaversity
