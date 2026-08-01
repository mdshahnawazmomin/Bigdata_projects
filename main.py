from scripts import step1_generate_raw_data, step2_sql_audit, step3_build_golden_records, step4_outreach_workflow, step5_export_excel_report

if __name__ == "__main__":
    print("🚀 Starting Healthcare Provider MDM Pipeline Execution...\n")
    step1_generate_raw_data.run()
    step2_sql_audit.run()
    step3_build_golden_records.run()
    step4_outreach_workflow.run()
    step5_export_excel_report.run()
    print("\n✅ Pipeline Completed! Open data/processed/ to view the Excel report.")