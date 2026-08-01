import re
import sqlite3
import pandas as pd


def standardize_address(address):
  if not address or pd.isna(address):
    return None
  address = re.sub(r'\bStreet\b', 'St', str(address), flags=re.IGNORECASE)
  address = re.sub(r'\bAvenue\b', 'Ave', str(address), flags=re.IGNORECASE)
  address = re.sub(r'#', 'Ste ', str(address))
  return address.strip()


def run():
  conn = sqlite3.connect('database/healthcare_mdm.db')

  query = """
    SELECT 
        n.npi, n.full_name, c.provider_name, n.taxonomy_specialty,
        c.office_address AS claims_address, n.registered_address AS npi_address,
        c.phone_number AS claims_phone, n.contact_phone AS npi_phone,
        cr.license_number, cr.license_status
    FROM stg_npi n
    LEFT JOIN stg_claims c ON n.npi = c.npi
    LEFT JOIN stg_cred cr ON n.npi = cr.npi;
    """

  df = pd.read_sql_query(query, conn)
  golden_records = []

  for npi, group in df.groupby('npi'):
    first_row = group.iloc[0]
    raw_addr = (
        first_row['claims_address']
        if pd.notna(first_row['claims_address'])
        else first_row['npi_address']
    )
    phone = (
        first_row['claims_phone']
        if pd.notna(first_row['claims_phone'])
        else first_row['npi_phone']
    )

    golden_records.append({
        'master_provider_id': f'PRV-{str(npi)[-5:]}',
        'npi': npi,
        'provider_name': first_row['full_name'].title(),
        'specialty': first_row['taxonomy_specialty'],
        'office_address': standardize_address(raw_addr),
        'phone_number': phone,
        'license_number': first_row['license_number'],
        'license_status': first_row['license_status'],
    })

  golden_df = pd.DataFrame(golden_records).drop_duplicates(subset=['npi'])
  golden_df.to_sql(
      'master_provider_directory', conn, if_exists='replace', index=False
  )
  conn.close()
  print(
      '✅ Step 3: Master Provider Directory created in database/healthcare_mdm.db'
  )


if __name__ == '__main__':
  run()