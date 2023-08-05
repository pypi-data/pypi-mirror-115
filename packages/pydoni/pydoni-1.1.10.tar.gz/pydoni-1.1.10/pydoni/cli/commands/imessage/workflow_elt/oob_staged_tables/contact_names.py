import click
import os
import pandas as pd
import pydoni
import re
from ....common import Verbose
from send2trash import send2trash


@click.option('--exported-contacts-csv-fpath', type=click.Path(exists=True), required=True,
              default=os.path.expanduser('~/Desktop/Contacts Export.csv'),
              help='Filepath of contacts exported .csv.')
@click.option('--pg-schema', type=str, default='imessage',
              help='Existing Postgres iMessage schema name.')
@click.option('--table-name', type=str, default='contact_names',
              help='Contact names table name.')
@click.option('--delete-csv', is_flag=True, default=False,
              help='Move contacts .csv to the trash when upload to Postgres is complete.')
@click.option('-v', '--verbose', is_flag=True, default=False,
              help='Print messages to console.')

@click.command()
def refresh_contact_names(exported_contacts_csv_fpath, pg_schema, table_name, delete_csv, verbose):
    """
    Refresh a contact name mapping in the user's local iMessage SQLite chat.db. The resulting
    table will contain `chat_identifier`: `contact_name` pairs and will be used for
    displaying a user's contact name (i.e. {first_name} {last_name}) given that user's
    phone number or iCloud email address when querying chat.db.
    """
    args, result = pydoni.__pydonicli_declare_args__(locals()), dict()
    pydoni.__pydonicli_register__({'command_name': pydoni.what_is_my_name(with_modname=True), 'args': args})

    pg = pydoni.Postgres()
    vb = Verbose(verbose)

    df = pd.read_csv(exported_contacts_csv_fpath)
    df.columns = [x.lower().replace(' : ', '_').replace(' ', '_').strip().strip('_') for x in df.columns]
    result['n_contacts_exported'] = len(df)
    vb.info(f'Read exported contacts CSV file ' + exported_contacts_csv_fpath)
    vb.info('CSV shape: ' + str(df.shape))

    # Create contact map in format `chat_identifier`: `contact_name`, where
    # `chat_identifier` is the contact's phone number or email, and `contact_name`
    # is the contact's display name in clear text.
    contact_map_df = pd.DataFrame(columns=['chat_identifier', 'contact_name'])
    for i, row in df.iterrows():
        name = row['display_name']
        for k, v in row[~row.isnull()].to_dict().items():
            if (k != 'display_name') and ('phone' in k or 'email' in k):
                v_lst = [v]  # Convert to list to append alternative values

                if 'phone' in k:
                    phone_no_spaces = str(v).replace(' ', '')
                    phone_no_chars = str(v).replace(' ', '').replace('(', '').replace(')', '').replace('-', '')
                    v_lst.append(phone_no_spaces)
                    v_lst.append(phone_no_chars)

                    if re.match(r'^\d{10}$', phone_no_chars):
                        # Example: 4155954380
                        phone_10_no_chars_w_plus_one = '+1' + phone_no_chars
                        v_lst.append(phone_10_no_chars_w_plus_one)

                    if re.match(r'^\d{11}$', phone_no_chars) and phone_no_chars.startswith('1'):
                        # Example: 14155954380
                        phone_11_no_chars_w_plus = '+' + phone_no_chars
                        v_lst.append(phone_11_no_chars_w_plus)

                for v_val in v_lst:
                    contact_map_df.loc[len(contact_map_df)] = [v_val, name]

    # Ensure only populated contact names remain
    contact_map_df = contact_map_df[~contact_map_df['contact_name'].isnull()]
    contact_map_df = contact_map_df.drop_duplicates()
    result['n_extracted_contact_chat_identifier_combinations'] = len(contact_map_df)
    vb.info(f"Extracted {len(contact_map_df)} {click.style('chat_identifier: contact_name', fg='black')} pairs")

    # Refresh `contact_names` table. Requires that table exist before insertion
    pg.wipe_table(pg_schema, table_name)
    contact_map_df.to_sql(table_name, pg.dbcon, schema=pg_schema, index=False, if_exists='append')
    vb.info(f"Refreshed table {click.style(pg_schema + '.' + table_name, fg='black')}")

    # Move exported CSV to trash if specified
    if delete_csv:
        send2trash(exported_contacts_csv_fpath)
        vb.info('Moved CSV to trash')

    result['contact_map_df_shape'] = contact_map_df.shape
    pydoni.__pydonicli_register__({k: v for k, v in locals().items() if k in ['result']})
    vb.program_complete('iMessage contacts table refresh complete ')
