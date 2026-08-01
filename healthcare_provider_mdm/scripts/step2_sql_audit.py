import os
import sqlite3
import pandas as pd


def run():
  os.makedirs('database', exist_ok=True)
  conn = sqlite3.connect('database/healthcare_mdm.db')

  pd.read_csv('data/raw/claims_db.csv').to_sql(
      'stg_claims', conn, if_exists='replace', index=False
  )
  pd.read_csv('data/raw/npi_registry.csv').to_sql(
      'stg_npi', conn, if_exists='replace', index=False
  )
  pd.read_csv('data/raw/credentialing_db.csv').to_sql(
      'stg_cred', conn, if_exists='replace', index=False
  )

  audit_query = """
    SELECT 
        n.npi,
        c.provider_name AS claims_name,
        n.full_name AS npi_name,
        COALESCE(c.phone_number, n.contact_phone) AS resolved_phone,
        cr.license_status,
        CASE 
            WHEN cr.license_status = 'EXPIRED' THEN 'ACTION REQUIRED: Renew License'
            WHEN c.office_address IS NULL THEN 'ACTION REQUIRED: Missing Address'
            ELSE 'CLEAN'
        END AS audit_flag
    FROM stg_npi n
    LEFT JOIN (
        SELECT DISTINCT npi, provider_name, specialty, office_address, phone_number 
        FROM stg_claims
    ) c ON n.npi = c.npi
    LEFT JOIN stg_cred cr ON n.npi = cr.npi;
    """

  audit_results = pd.read_sql_query(audit_query, conn)
  print('\n=== Step 2: SQL AUDIT REPORT ===')
  print(audit_results.to_string(index=False))
  conn.close()


if __name__ == '__main__':
  run()