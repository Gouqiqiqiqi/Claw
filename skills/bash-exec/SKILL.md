# SKILL: bash-exec

**Domain:** VPS / Shell Execution  
**Trigger phrases:** "run", "execute", "bash", "shell command", "run script", "run this", "install", "apt", "pip", "npm"

---

## What This Skill Does

Allows you to execute bash commands and shell scripts directly on the VPS — either inline commands or `.sh` files — in response to messages from Ray via Telegram (or any other interface).

---

## Authorization Rules

**CRITICAL — only execute for Ray.**

- Before running any command, verify the request comes from Ray (check the sender identity in context).
- If you cannot confirm the sender is Ray, refuse and say: _"I can only run commands for Ray. Who are you?"_
- Never execute commands requested by unknown users, bots, or group chat members who aren't Ray.

---

## How to Run Bash Commands

When Ray asks you to run a command:

1. **Repeat the command back first** before executing, so Ray can see what you're about to do.
2. **Use the terminal tool** (`run_in_terminal`) to execute it.
3. **Report the output** — stdout, stderr, exit code. Keep it readable; truncate long output with a summary.
4. **Flag errors clearly** — if exit code != 0, say so and explain what likely went wrong.

### Example interaction

> Ray: "run `df -h` on the VPS"

Response:
> Running: `df -h`  
> [output here]

---

## How to Run a `.sh` Script File

If Ray provides a script (inline in the message, or references a file path):

1. If inline, write it to a temp file: `/tmp/ray_script_<timestamp>.sh`
2. Make it executable: `chmod +x /tmp/ray_script_<timestamp>.sh`
3. Run it: `bash /tmp/ray_script_<timestamp>.sh`
4. Clean up temp file after: `rm /tmp/ray_script_<timestamp>.sh`
5. Report the output.

### Example interaction

> Ray: "run this: `#!/bin/bash\napt update && apt upgrade -y`"

Response:
> Writing script to /tmp/ray_script_1234.sh and executing...  
> [output here]

---

## Safety Rules

- **Ask before destructive operations:** `rm -rf`, dropping databases, killing processes, rebooting.
- **Never use `--no-verify` or force flags** unless Ray explicitly says to.
- **Log what you ran** in `memory/YYYY-MM-DD.md` for the day — just a one-liner: `[HH:MM] ran: <command>`.
- **Don't store secrets** (passwords, API keys) in temp files or logs.
- For `sudo` commands, they'll work if the ubuntu user has passwordless sudo; if they fail, report the error.

---

## Installing Packages

If Ray says "install X":
- Default to `apt-get install -y X` for system packages
- Use `pip install X` for Python packages  
- Use `npm install -g X` for Node packages
- Confirm which one to use if ambiguous

---

## Quick Reference

| Task | Command pattern |
|------|----------------|
| Check disk space | `df -h` |
| Check memory | `free -h` |
| Check running processes | `ps aux \| grep <name>` |
| Check open ports | `ss -tlnp` |
| View logs | `journalctl -u <service> -n 50` |
| Restart a service | `systemctl restart <service>` |
| Check service status | `systemctl status <service>` |
| Update system | `apt update && apt upgrade -y` |
