import os
import pandas as pd


def run():
  os.makedirs('data/raw', exist_ok=True)

  claims_data = {
      'claim_id': ['CLM001', 'CLM002', 'CLM003', 'CLM004'],
      'npi': ['1982736410', '1982736410', '1029384756', '1456789012'],
      'provider_name': [
          'Dr. Robert Chen',
          'Dr. Robert Chen',
          'Sarah Jenkins, MD',
          'Marcus Vance',
      ],
      'specialty': [
          'Internal Med',
          'Internal Med',
          'Pediatrics',
          'Cardiology',
      ],
      'office_address': [
          '100 Main St, Suite 200',
          '100 Main St, Suite 200',
          '450 Health Ave',
          None,
      ],
      'phone_number': [None, None, '555-012-9944', '555-088-3311'],
  }

  npi_data = {
      'npi': ['1982736410', '1029384756', '1456789012'],
      'full_name': ['CHEN, ROBERT L', 'JENKINS, SARAH', 'VANCE, MARCUS'],
      'taxonomy_specialty': ['Internal Medicine', 'Pediatrics', 'Cardiology'],
      'registered_address': [
          '100 Main Street #200',
          '450 Health Avenue',
          '789 Care Blvd, Ste 10',
      ],
      'contact_phone': ['555-019-2831', '555-012-9944', '555-088-3311'],
  }

  cred_data = {
      'npi': ['1982736410', '1029384756', '1456789012'],
      'license_number': ['LIC-9921', 'LIC-3341', 'LIC-8812'],
      'license_status': ['ACTIVE', 'EXPIRED', 'ACTIVE'],
      'last_credentialed_date': ['2025-01-10', '2023-05-12', '2025-06-20'],
  }

  pd.DataFrame(claims_data).to_csv('data/raw/claims_db.csv', index=False)
  pd.DataFrame(npi_data).to_csv('data/raw/npi_registry.csv', index=False)
  pd.DataFrame(cred_data).to_csv('data/raw/credentialing_db.csv', index=False)
  print('✅ Step 1: Raw CSV datasets generated in data/raw/')


if __name__ == '__main__':
  run()