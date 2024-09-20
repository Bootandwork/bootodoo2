## Legend
### + Features/Added
### - Bugs/Fixed/Removed
### Date dd-mm-yyyy


## Version 6.3.0 -> 6.3.1 (25-04-2024)
### Removed
    - Deprecated service principal connection method


## Version 6.2.2 -> 6.3.0 (16-04-2024)
### Added
    + Table relationship based on many2one field
    + Controller for redirect URI
    + Auto redirect in case of api consent error during test connection
    + Custom field/column labels
    + Filters and groups in workspace, datasets and tables
    + Validation in table to check relationship
    + Other view level and stability updates
### Removed
    - Parent-Child relation between table columns
### Fixed
    - Installation warnings


## Version 6.2.1 -> 6.2.2 (15-12-2023)
### Added
    + Computing default workspace or dataset when creating new dataset or table respectively
### Fixed
    - Data export issue in tables (memory limit exceed)

## Version 6.2.0 -> 6.2.1 (20-07-2023)
### Added
    + Table count in datasets
    + Report and dashboard count in workspaces
### Fixed
    - Using odoo field description as powerbi column name instead of adding parent and child fields


## Version 6.1.0 -> 6.2.0 (30-06-2023)
### Added
    + Last sync date to avoid duplicity on PowerBI end
    + Warning message for schema update
    + Other message level updates
### Removed
    - powerbi.snipper model
    - Report and Dashboard wizards


## Version 6.0.1 -> 6.1.0 (16-05-2023)
### Added
    + Option to unpublish a dataset from odoo
    + Reset connection
    + Chatter for logging error/success messages and conversations
    + Odoo dashboard for overall summary of published and unpublished records
    + Confirmation messages during data export/delete and schema update
    + Responsible user and object counts in workspace
    + Record rules to streamline access management
    + Connection states management
    + Option to configure cron from connection
    + Other view level and stability updates
### Fixed
    - Report and dashboard render issue
### Removed
    - Sync history model
    - Publish server actions from workspace and datasets


## Version 6.0.0 -> 6.0.1 (25-01-2023)
### Added
    + Support for PowerBI's "My Workspace" (Default workspace)
### Fixed
    - Data type issue in date/datetime fields


## Version 3.2.0 -> 6.0.0 (18-11-2022)
### Added
    Module is now compatible with Odoo v16
    + Minor view level updates
### Removed
    - Required field check on connection create method, made required in form view


## Version 3.1.1 -> 3.2.0 (22-03-2022)
## Fixed
    - Rows limit issue in API, using batch of 10k rows


## Version 2.0.1 -> 3.1.1 (17-03-2022)
### Added
    + Openid scope during connection
    + Minor stability updates


## Version 2.0.0 -> 2.0.1 (11-02-2022)
### Added
    + All the required api scopes during connection


## Version 1.0.0 -> 2.0.0 (04-10-2021)
### Added
    Module is now compatible with Odoo v15
    + Cron to export data
    + Wizard to update connection credentials
    + Api consent permission error with complete url to hit on browser for api permissions
    + Creation/Deletion of server actions from tables
    + Web Ribbon widget for connection status
    + Other view level and stability updates


## Version 1.0.0 (20-07-2021) (Initial Release)
### Features
    + Import/Export workspaces
    + Export datasets with tables
    + Export/Delete data in tables for any odoo model
    + Update the table schema on PowerBI from Odoo
    + Import PowerBI reports and dashboards on Odoo
    + Embedd PowerBI reports and dashboard on Odoo
