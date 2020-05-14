import os
import xml.etree.cElementTree as etree
import logging
import xmltodict
import pymongo
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
    },
    'users': {
        'Id': 'INTEGER',
        'Reputation': 'INTEGER',
        'CreationDate': 'DATETIME',
        'DisplayName': 'TEXT',
        'LastAccessDate': 'DATETIME',
        'WebsiteUrl': 'TEXT',
        'Location': 'TEXT',
        'Age': 'INTEGER',
        'AboutMe': 'TEXT',
        'Views': 'INTEGER',
        'UpVotes': 'INTEGER',
        'DownVotes': 'INTEGER',
        'AccountId': 'INTEGER',
        'ProfileImageUrl': 'TEXT'
    },
    'tags': {
        'Id': 'INTEGER',
        'TagName': 'TEXT',
        'Count': 'INTEGER',
        'ExcerptPostId': 'INTEGER',
        'WikiPostId': 'INTEGER'
    }
}


def dump_files(file_names, anathomy,
               databaseName='Test',
               dump_path='/home/deep/Academics/BTP/cooking.stackexchange.com/test',
               log_filename='so-parser.log'):

    logging.basicConfig(filename=os.path.join(
        dump_path, log_filename), level=logging.INFO)

    mng_client = pymongo.MongoClient('localhost', 27017)
    mng_db = mng_client[databaseName]

    for file in file_names:
        print("Opening {0}.xml".format(file))
        with open(os.path.join('.', file + '.xml')) as fd:
            my_dict = xmltodict.parse(fd.read())
            collection_name = file.lower()
            db_cm = mng_db[collection_name]
            db_cm.remove()
            db_cm.insert_many(my_dict[collection_name]['row'])

if __name__ == '__main__':
    dump_files(ANATHOMY.keys(), ANATHOMY)



