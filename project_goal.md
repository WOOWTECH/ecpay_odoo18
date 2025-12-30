# Code Review and Live Odoo Instance Test

## Goal

Make sure all functions related to `ecpay_invoice_tw` and `ecpay_invoice_website` and `payment_ecpay` are 100% working correctly in Live Odoo 18 Instance. 

## Requirement

- Review the codebase of 3 modules see if they comply with odoo architecture and don't have any compile error. The Odoo environment architecture located in the path `/mnt/c/Users/Matt/Desktop/CLAUDE專案/ODOO相關/Odoo_18_Environment_Architecture`. 
- Git commit when file changed (including files in .claude). Please manage the branch properly.
- Design a comprehensive live odoo 18 instance test for all functions. Use playwright-mcp test it.
- Use `MASTER_TASK.md` with task summary to track progress. Whenever a task is completed, write the task summary to `MASTER_TASK.md`.

## Note

You can always refer to the older version of the user manual `ECPay_user_manual_1.0.2.pdf`. However, please note that since this is an older version of the user manual, you should not rely on it excessively.

## Test Information for CLAUDE

### ODOO UI - Admin permission login information

- URL : https://matt-test-254-odoo.woowtech.io/
- Login user name : admin
- Login password : admin

### ODOO UI - User permission login information

- URL : https://matt-test-254-odoo.woowtech.io/
- Login user name : woow_ngrok_002@protonmail.com
- Login password : admin

### Email UI - User Email account login information

- URL : https://mail.proton.me/
- Login user name : woow_ngrok_002@protonmail.com
- Login password : 4,vUipokfFvJnS/

### SSH to HomeAssistant terminal

My Odoo server is installed in the same Docker environment as the Home Assistant Addon. Use command `ssh ha-192-168-2-254` to access to HomeAssistant terminal. You can perform any query in HomeAssistant terminal, but you **MUST NOT modify any data during HomeAssistant terminal**.