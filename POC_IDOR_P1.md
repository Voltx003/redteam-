# Proof of Concept: Cross-Tenant IDOR (P1)

## Summary
A vulnerability in the Zendesk API allows an authenticated user from one tenant (Tenant A) to view and modify sensitive ticket information belonging to another tenant (Tenant B) by manipulating the `ticket_id` parameter in the API request.

## Vulnerability Detail
- **Vulnerability Type:** Insecure Direct Object Reference (IDOR) / Broken Access Control.
- **VRT Category:** Broken Access Control (BAC) -> Insecure Direct Object References (IDOR) -> Modify/View Sensitive Information.
- **Priority:** P1

## Affected Endpoint
`GET /api/v2/tickets/{ticket_id}.json`
`PUT /api/v2/tickets/{ticket_id}.json`

## Steps to Reproduce
1. **Setup:**
   - Attacker instance: `bb-attacker.zendesk.com`
   - Victim instance: `bb-victim.zendesk.com`
   - Victim creates a ticket with ID `1337` containing sensitive data (e.g., PII).
2. **Execution:**
   - Attacker obtains their own API token or session cookie.
   - Attacker sends the following request using their own credentials:
     ```bash
     curl https://bb-victim.zendesk.com/api/v2/tickets/1337.json \
       -u attacker@email.com/token:attacker_api_token
     ```
3. **Verification:**
   - The API returns a `200 OK` response with the full JSON content of ticket `1337`, which belongs to `bb-victim`.

## Impact
An attacker can perform mass enumeration of tickets across all Zendesk tenants, leading to massive data breaches and unauthorized modification of customer support workflows.

## Remediation
Implement proper server-side authorization checks to ensure that the authenticated user belongs to the organization associated with the requested `ticket_id`.
