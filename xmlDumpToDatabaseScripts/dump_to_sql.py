import sqlite3
import os
import xml.etree.cElementTree as etree
import logging
from gensim.parsing.preprocessing import strip_tags
ANATHOMY = {
    'badges': {
        'Id': 'INTEGER',
        'UserId': 'INTEGER',
        'Class': 'INTEGER',
        'Name': 'TEXT',
        'Date': 'DATETIME',
        'TagBased': 'BOOLEAN',
    },
    'comments': {
        'Id': 'INTEGER',
        'PostId': 'INTEGER',
        'Score': 'INTEGER',
        'Text': 'TEXT',
        'CreationDate': 'DATETIME',
        'UserId': 'INTEGER',
        'UserDisplayName': 'TEXT'
    },
    'posts': {
        'Id': 'INTEGER',
        'PostTypeId': 'INTEGER',  # 1: Question, 2: Answer
        'ParentId': 'INTEGER',  # (only present if PostTypeId is 2)
        'AcceptedAnswerId': 'INTEGER',  # (only present if PostTypeId is 1)
        'CreationDate': 'DATETIME',
        'Score': 'INTEGER',
        'ViewCount': 'INTEGER',
        'Body': 'TEXT',
        # (present only if user has not been deleted)
        'OwnerUserId': 'INTEGER',
        'OwnerDisplayName': 'TEXT',
        'LastEditorUserId': 'INTEGER',
        'LastEditorDisplayName': 'TEXT',  # ="Rich B"
        'LastEditDate': 'DATETIME',  # ="2009-03-05T22:28:34.823"
        'LastActivityDate': 'DATETIME',  # ="2009-03-11T12:51:01.480"
        # (present only if post is community wikied)
        'CommunityOwnedDate': 'DATETIME',
        'Title': 'TEXT',
        'Tags': 'TEXT',
        'AnswerCount': 'INTEGER',
        'CommentCount': 'INTEGER',
        'FavoriteCount': 'INTEGER',
        'ClosedDate': 'DATETIME'
    },
    'votes': {
        'Id': 'INTEGER',
        'PostId': 'INTEGER',
        'UserId': 'INTEGER',
        'VoteTypeId': 'INTEGER',
        # -   1: AcceptedByOriginator
        # -   2: UpMod
        # -   3: DownMod
        # -   4: Offensive
        # -   5: Favorite
        # -   6: Close
        # -   7: Reopen
        # -   8: BountyStart
        # -   9: BountyClose
        # -  10: Deletion
        # -  11: Undeletion
        # -  12: Spam
        # -  13: InformModerator
        'CreationDate': 'DATETIME',
        'BountyAmount': 'INTEGER'
    },
    'posthistory': {
        'Id': 'INTEGER',
        'PostHistoryTypeId': 'INTEGER',
        'PostId': 'INTEGER',
        'RevisionGUID': 'TEXT',
        'CreationDate': 'DATETIME',
        'UserId': 'INTEGER',
        'UserDisplayName': 'TEXT',
        'Comment': 'TEXT',
        'Text': 'TEXT'
    },
    'postlinks': {
        'Id': 'INTEGER',
        'CreationDate': 'DATETIME',
        'PostId': 'INTEGER',
        'RelatedPostId': 'INTEGER',
        'PostLinkTypeId': 'INTEGER',
        'LinkTypeId': 'INTEGER'
    }
    # 'users': {
    #     'Id': 'INTEGER',
    #     'Reputation': 'INTEGER',
    #     'CreationDate': 'DATETIME',
    #     'DisplayName': 'TEXT',
    #     'LastAccessDate': 'DATETIME',
    #     'WebsiteUrl': 'TEXT',
    #     'Location': 'TEXT',
    #     'Age': 'INTEGER',
    #     'AboutMe': 'TEXT',
    #     'Views': 'INTEGER',
    #     'UpVotes': 'INTEGER',
    #     'DownVotes': 'INTEGER',
    #     'AccountId': 'INTEGER',
    #     'ProfileImageUrl': 'TEXT'
    # },
    # 'tags': {
    #     'Id': 'INTEGER',
    #     'TagName': 'TEXT',
    #     'Count': 'INTEGER',
    #     'ExcerptPostId': 'INTEGER',
    #     'WikiPostId': 'INTEGER'
    # }
}


def dump_files(file_names, anathomy,
               dump_path='/home/deep/Academics/IS/TEST/Q-A-Data_annotation-Portal/db',
               dump_database_name='development.sqlite3',
               insert_query='INSERT INTO {table} ({columns}) VALUES ({values})',
               create_query='CREATE TABLE IF NOT EXISTS {table} ({fields})',
               log_filename='so-parser.log'):
    logging.basicConfig(filename=os.path.join(
        dump_path, log_filename), level=logging.INFO)
    db = sqlite3.connect(os.path.join(dump_path, dump_database_name))
    for file in file_names:
        print("Opening {0}.xml".format(file))
        with open(os.path.join('.', file + '.xml')) as xml_file:
            tree = etree.iterparse(xml_file)
            table_name = file.lower()

            sql_create = create_query.format(
                table=table_name,
                fields=", ".join(['{0} {1}'.format(name, type) for name, type in anathomy[table_name].items()]))
            print('Creating table {0}'.format(table_name))

            try:
                logging.info(sql_create)
                db.execute(sql_create)
            except Exception as e:
                logging.warning(e)

            count = 0
            for events, row in tree:
                try:
                    if row.attrib.values():
                        logging.debug(row.attrib.keys())
                        query = insert_query.format(
                            table=table_name,
                            columns=', '.join(row.attrib.keys()),
                            values=('?, ' * len(row.attrib.keys()))[:-2])
                        vals = []
                        for key, val in row.attrib.items():
                            if anathomy[table_name][key] == 'INTEGER':
                                vals.append(int(val))
                            elif anathomy[table_name][key] == 'BOOLEAN':
                                vals.append(1 if val == "TRUE" else 0)
                            elif anathomy[table_name][key] == 'TEXT':
                                vals.append(strip_tags(val))
                            else:
                                vals.append(val)
                    
                        count += 1
                        if (count % 15000 == 0):
                            print("{}".format(count))
                            print(query)
                            print(vals)
                        db.execute(query, vals)

                except Exception as e:
                    logging.warning(e)
                    print("x", end="")
                finally:
                    row.clear()
            print("\n")
            db.commit()
            del (tree)

if __name__ == '__main__':
    dump_files(ANATHOMY.keys(), ANATHOMY)