# Reconnaissance: Zendesk Bug Bounty (Bugcrowd)

## Rules of Engagement
- **Safe Harbor:** Active.
- **Identity:** Use `@bugcrowdninja.com` email.
- **Company Name:** `bb-<bugcrowd-username>`.
- **Instance Format:** `bb-<bugcrowd-username>-<suffix>.zendesk.com`.
- **Prohibitions:** No DoS/DDoS, no social engineering, no physical attacks.

## Scope
- `*.zendesk.com`
- `*.zd-master.com`
- Zendesk AI features (AI agents, Copilot, App Builder).
- LLM-related vulnerabilities.

## Tools Available
- Nmap
- Metasploit Framework (msfconsole)
- SQLmap
- Aircrack-ng
- Dirb
- Hashcat
- Cewl
- Proxychains4
- (and others)

## Strategy
- Follow the Vulnerability Rating Taxonomy (VRT).
- Focus on high-impact logic flaws or AI-specific vulnerabilities as requested.

## Potential P1 Patterns for Zendesk
1. **Broken Access Control (IDOR) - P1**:
   - Accessing/Modifying tickets or user data from a different tenant (`Cross-Tenant`).
   - Endpoint example: `GET /api/v2/tickets/{ticket_id}.json` (where ticket_id belongs to another account).
2. **AI Application Security - P1**:
   - **Cross-Tenant PII Leakage**: Using Prompt Injection to force a Zendesk AI Agent to leak data belonging to other customers or internal system configurations.
   - **Remote Code Execution (RCE)**: If the AI Agent has tool-calling capabilities (e.g., App Builder) that can be abused to execute system commands.
3. **Authentication Bypass - P1**:
   - Bypassing SSO or 2FA to gain full access to an agent or admin account.

## Testing Methodology (Legal Scope)
1. Register two separate trial instances: `bb-jules-test1.zendesk.com` and `bb-jules-test2.zendesk.com`.
2. Use the credentials of Test1 to attempt to access objects (tickets, files) created in Test2.
3. For AI testing, interact with the AI Agent in Test1 and use adversarial prompts to test for model behavior or data leakage.
