import os, uuid, sys
from azure.storage.blob import BlockBlobService, PublicAccess
from main import db
from flask_login import current_user
from models import Single_Upload, User, Group_Upload

for x in range(30):
    container = 'testtest' + str(x)
    group_upload = Group_Upload(container_name = container , compressed_file_name_short_with_extension = str(x), compressed_file_name_long_with_extension =  str(x),  user_id = 1)
    db.session.add(group_upload)
    db.session.commit()

print("DONE")