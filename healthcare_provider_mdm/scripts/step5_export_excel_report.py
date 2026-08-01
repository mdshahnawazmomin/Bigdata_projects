import os
import sqlite3
import pandas as pd


def run():
  os.makedirs('data/processed', exist_ok=True)
  conn = sqlite3.connect('database/healthcare_mdm.db')

  master_df = pd.read_sql_query('SELECT * FROM master_provider_directory', conn)

  summary_data = {
      'Metric': [
          'Total Profiles Processed',
          'Active & Clean Profiles',
          'Expired Licenses Flagged',
          'Quality Score (%)',
      ],
      'Value': [
          len(master_df),
          len(master_df[master_df['license_status'] == 'ACTIVE']),
          len(master_df[master_df['license_status'] == 'EXPIRED']),
          f"{(len(master_df[master_df['license_status'] == 'ACTIVE']) / len(master_df)) * 100:.1f}%",
      ],
  }

  summary_df = pd.DataFrame(summary_data)
  file_path = 'data/processed/Master_Provider_Directory_Report.xlsx'

  try:
    with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
      master_df.to_excel(
          writer, sheet_name='Golden Master Directory', index=False
      )
      summary_df.to_excel(writer, sheet_name='Executive Summary', index=False)
    print(f'🎉 Step 5: Report successfully exported to {file_path}')
  except PermissionError:
    print(
        f'\n⚠️  ERROR: Could not write to {file_path}. Please CLOSE the Excel'
        ' file and run again!'
    )

  conn.close()


if __name__ == '__main__':
  run()