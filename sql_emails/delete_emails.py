#!/bin/env python3
import pandas as pd

email_csv = 'email_list.csv'
emails = pd.read_csv(email_csv)

# Create script
for email in emails['email']:
    print('DELETE FROM priority_emails WHERE email=\'{email}\';'.format(email=email))

