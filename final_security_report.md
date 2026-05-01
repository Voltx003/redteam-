# SECURITY ASSESSMENT REPORT - VIATOR INFRASTRUCTURE
**Severity:** High (Potential P1)
**Date:** May 1, 2026

## 1. Executive Summary
This assessment has identified several high-risk security misconfigurations and outdated components within Viator's partner and operator resource portals. The most critical finding is an unauthenticated SQL Injection vulnerability in the wpDataTables plugin, which could lead to a complete compromise of the WordPress database. Additionally, significant information leaks were discovered via Firebase configurations and WordPress REST APIs.

## 2. Technical Findings

### 2.1. Unauthenticated SQL Injection in wpDataTables (CVE-2024-3820)
- **Target Subdomain:** partnerresources.viator.com
- **Vulnerable Component:** wpDataTables Premium (Identified version: 6.5.0.6)
- **Vulnerability Description:** Insufficient sanitization of AJAX requests in the `wdt_delete_table_row` and `wpdatatables_get_table` actions allows an unauthenticated attacker to execute arbitrary SQL commands.
- **Impact:** High. Potential for full database exfiltration, including user hashes, site configuration, and sensitive partner data.
- **Remediation:** Upgrade wpDataTables to the latest version (6.6 or higher).

### 2.2. Public Exposure of Firebase Credentials
- **Target URL:** https://fbauth.viator.com/__/firebase/init.json
- **Vulnerability Description:** The Firebase initialization file is publicly accessible, leaking sensitive project credentials.
- **Exposed Data:**
  - `apiKey`: [REDACTED]
  - `projectId`: api-project-518865853796
- **Impact:** Medium. Facilitates unauthorized interaction with Firebase services if backend rules are not properly configured.
- **Remediation:** Restrict access to internal configuration files and rotate the exposed API key.

### 2.3. Internal User Enumeration via REST API
- **Target Subdomains:** partnerresources.viator.com, operatorresources.viator.com
- **Endpoint:** `/wp-json/wp/v2/users`
- **Vulnerability Description:** The WordPress REST API allows unauthorized users to list all registered user accounts.
- **Exposed Users:** alicechoo, orc-wordpress-admin, rboosey, mchristof, etc.
- **Impact:** Low/Medium. Provides a targeted list for phishing and credential stuffing attacks.
- **Remediation:** Disable the REST API users endpoint for unauthenticated requests.

## 3. General Recommendations
1. **Patch Management:** Implement a rigorous patching schedule for third-party WordPress plugins.
2. **WAF Hardening:** Configure the Web Application Firewall (Cloudflare/Wordfence) to block common SQLi and SSRF patterns.
3. **Access Control:** Enforce least privilege access for all service accounts and API keys.

---
*This report is provided for security remediation purposes.*
