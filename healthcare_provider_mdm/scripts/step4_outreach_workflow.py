import sqlite3
import pandas as pd


def run():
  conn = sqlite3.connect('database/healthcare_mdm.db')
  master_df = pd.read_sql_query('SELECT * FROM master_provider_directory', conn)

  print('\n=== Step 4: OUTREACH WORKFLOW TRIGGERED ===')
  for _, row in master_df.iterrows():
    if row['license_status'] == 'EXPIRED':
      print(
          f"📧 Email Draft Created: Renewal required for {row['provider_name']}"
          f" (NPI: {row['npi']})"
      )

  conn.close()


if __name__ == '__main__':
  run()