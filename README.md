# SAIL_VT(Project-8_weeks)
Python-based GUI tool built during my internship at SAIL to compare two CSV files and identify differences in employee data. It highlights modified records and new joiners, and generates professional PDF reports for easy data auditing and HR records management and automated payslip generation.

📊 CSV Comparator (Python GUI for SAIL employees Payroll)  
A Python-based desktop GUI application designed during my internship at SAIL to automate payroll data comparisons between two employee CSV files: a Master and a Slave. The tool identifies:

- Data discrepancies in employee details (like IFSC, DOJ, DOB)
- New Joinees absent in the Master dataset
- Generates well-structured PDF reports for audits and HR documentation, now with password protection for enhanced security.
- Supports emailing the generated PDF reports directly to specified recipients.

📌 Technical Overview  
**Framework & Libraries:**

- Tkinter: GUI layout and event handling
- Pandas: Data manipulation and comparison logic
- ReportLab: PDF generation
- PyPDF2: PDF encryption for password protection
- smtplib: Email functionality for sending reports
- ttk.Treeview: Data table presentation with search filters
- ttk.Style: Custom Light/Dark mode support
- Sendgrid API: Sending email from primary gmail to receipients.

📐 Architecture Summary  
**GUI Layer:** Tkinter-based interface with file selectors, action buttons, tabbed result views, and status messages.

**Data Handling:** Pandas processes both CSV files, matches records by SAIL_PERNO & UNIT_PERNO, detects field-level changes, and isolates new records.

**Report Generator:** ReportLab converts result dataframes into clean, timestamped PDF documents, now with password protection to secure sensitive information.

**Email Functionality:** Allows users to send generated PDF reports directly to specified email addresses, facilitating easy sharing of audit documentation.

**Theme Control:** User-selectable Light/Dark mode via ttk.Style configurations.

📋 Features  
- Compare two payroll CSVs for data changes
- Detect and display new joinee records
- Interactive, searchable tables with instant viewing
- Export categorized difference reports as professional PDFs
- Password protection for PDF reports to secure sensitive data
- Email functionality to send reports directly to recipients
- Light/Dark mode toggle for improved usability

🔍 Example Use Cases  
- Payroll audits for IFSC, DOJ, or account changes
- Automated tracking of monthly new joinees
- Audit trail documentation generation for HR & Finance departments
- Secure sharing of reports via email for compliance and record-keeping

📌 Key Technical Highlights  
**Dynamic Data Comparison:**  
Indexes dataframes by composite keys, excludes non-relevant columns, and checks for value changes field-wise.

**New Joinee Detection:**  
Isolates records existing in the Slave but absent in the Master, based on core identifying fields.

**PDF Report Styling:**  
Converts Pandas data into well-formatted ReportLab tables, with automatic timestamped file naming and password protection for enhanced security.

**Email Integration:**  
Facilitates direct emailing of generated reports to specified recipients, streamlining the documentation process.

**Dark Mode Implementation:**  
Dynamically switches ttk.Style configurations to toggle UI appearance without restarting the application.

---
