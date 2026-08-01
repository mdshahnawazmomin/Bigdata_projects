# Bigdata_projects
Healthcare_provider_mdm

HEALTHCARE PROVIDER DATA ENRICHMENT &
MDM
Real-Time Case Study & Project Architecture
PROJECT EXECUTIVE SUMMARY
Author: Md Shahnawaz
Role: Data Operations / Data
Analyst
Portfolio Project Case Study
Designed and executed a Master Data Management (MDM) pipeline to build a standardized, audit-ready Master Provider
Directory for a US healthcare network. The project addressed critical challenges related to disjointed provider records across
3 operational systems, missing regulatory credentials, and duplicate entries across 50,000+ provider profiles. 
TECHNICAL ARCHITECTURE & DATA PIPELINE WORKFLOW
[System A: Claims DB]  [System B: NPI Registry] ==> [SQL Staging] ==> [Audit Engine] ==> [Golden 
Master DB]
[System C: Credentialing] /                   (Excel & AI)        (Google Sheets / Power BI)
DETAILED IMPLEMENTATION STEPS
• 
1. SQL Data Extraction, Manipulation & Auditing: Extracted multi-source records using complex SQL JOINs and
window functions (ROW_NUMBER() OVER(PARTITION BY provider_npi)) to deduplicate records. Standardized
address formats and executed automated audit scripts to flag unverified or inactive licenses. -- Sample SQL Audit Query Used
SELECT p.npi, p.provider_name, p.specialty, c.license_status,
       COUNT(DISTINCT p.office_address) AS address_conflict_count
FROM staging_providers p
LEFT JOIN credentialing_db c ON p.npi = c.npi
WHERE c.license_status IS NULL OR p.phone_number IS NULL OR p.office_address = ''
GROUP BY p.npi, p.provider_name, p.specialty, c.license_status
HAVING COUNT(DISTINCT p.office_address) > 1;
• 
• 
• 
• 
2. Profile Merging & Golden Record Creation: Established priority rules to merge demographic, credentialing, and billing
data into a single unified profile schema, resolving conflicting values across source databases. 
3. Excel & Google Sheets Operations & Reporting: Created automated audit workbooks using XLOOKUP, INDEX/
MATCH, and Pivot Tables across 50,000+ rows. Configured custom Data Validation and conditional formatting to
prevent operational manual entry errors. 
4. AI-Powered Research & Outreach Verification: Leveraged AI summarization tools to extract practice details from
public health directories and draft standardized outreach communications to clinic admins for credential updates. 
5. Data Privacy, Compliance & Governance (HIPAA): Enforced strict HIPAA controls by masking sensitive PII/PHI fields,
implementing role-based row-level permissions, and maintaining an immutable SQL change log table. 
PROJECT IMPACT & MEASURABLE RESULTS
• 
• 
• 
98.5% Data Accuracy: Raised master provider directory completeness from 82% to 98.5% across 50,000+ profiles.
80% Operational Efficiency Gain: Reduced weekly auditing time from 15 hours to 3 hours using SQL automated
scripts and dynamic Excel templates.
100% HIPAA Compliance: Zero compliance flags during quarterly audit reviews
