import os, uuid, sys
from azure.storage.blob import BlockBlobService, PublicAccess
from flask_login import current_user
from models import Single_Upload, User, Group_Upload
from database import db

#https://github.com/Azure-Samples/storage-blobs-python-quickstart


#single files will be uploaded into single containers (text or file itself)
#group files will be all grouped into one container with the container containing all the pickles

def upload_single_file(file_name_short_with_extension, file_path, container_name, file_name_long_with_extension, delete=False, update_db = True):
    try:
        block_blob_service = BlockBlobService(account_name='mednlpstorage', account_key='v+IgtNIIRhZjqMZx+e886rhJMVAhIUoUfG252SVIftBCyx8bG+NE0apP20xakOsMRQfNZFbUggUUULN2JER8lg==')

        file_name_short_with_extension = file_name_short_with_extension.replace('_', '-')
        file_name_long_with_extension = file_name_long_with_extension.replace('_', '-')
        container_name = container_name.replace('_', '-')


        # Create a container called 'quickstartblobs'.
        block_blob_service.create_container(container_name)

        print('DESTINATION CONTAINER CREATED')


        # Set the permission so the blobs are public.
        block_blob_service.set_container_acl(container_name, public_access=PublicAccess.Container)

        print('CONTAINER PERMISISON SET')


        # Upload the created file, use name_at_destination for the blob name
        block_blob_service.create_blob_from_path(container_name, file_name_long_with_extension, file_path)

        print('FILE UPLOADED')

        if delete == True:
            os.remove(file_path)



        if update_db == True:
            current_username  = current_user.username
            user = User.query.filter_by(username=current_username).first()
            file_upload = Single_Upload(container_name = container_name, file_name_short_with_extension = file_name_short_with_extension, file_name_long_with_extension = file_name_long_with_extension, user_id = user.id)
            db.session.add(file_upload)
            db.session.commit()

            print('DB UPDATED')
        
    except Exception as e:
        print(e)


def upload_group_file(compressed_file_name_short_with_extension, compressed_file_name_long_with_extension, container_name,
total_text_path, vectorizer_path, dtm_path, file_names_path, lda_model_path, lda_html_path, pyldavis_html_path, delete=False, update_db = True):
    try:
        block_blob_service = BlockBlobService(account_name='mednlpstorage', account_key='v+IgtNIIRhZjqMZx+e886rhJMVAhIUoUfG252SVIftBCyx8bG+NE0apP20xakOsMRQfNZFbUggUUULN2JER8lg==')

        # Create a container called 'quickstartblobs'.
        block_blob_service.create_container(container_name)


        # Set the permission so the blobs are public.
        block_blob_service.set_container_acl(container_name, public_access=PublicAccess.Container)

        compressed_file_name_short_with_extension = compressed_file_name_short_with_extension.replace('_', '-')
        compressed_file_name_long_with_extension = compressed_file_name_long_with_extension.replace('_', '-')
        container_name = container_name.replace('_', '-')


        # Upload the created file, use name_at_destination for the blob name
        block_blob_service.create_blob_from_path(container_name, 'total_text.p', total_text_path)
        block_blob_service.create_blob_from_path(container_name, 'vectorizer.p', vectorizer_path)
        block_blob_service.create_blob_from_path(container_name, 'dtm.p', dtm_path)
        block_blob_service.create_blob_from_path(container_name, 'file-names.p', file_names_path)
        block_blob_service.create_blob_from_path(container_name, 'lda-model.p', lda_model_path)
        block_blob_service.create_blob_from_path(container_name, 'lda-html.p', lda_html_path)
        block_blob_service.create_blob_from_path(container_name, 'pyldavis-html.p', pyldavis_html_path)


        if delete == True:
            os.remove(compressed_file_name_long_with_extension)

        if update_db == True:
            current_username  = current_user.username
            user = User.query.filter_by(username=current_username).first()
            group_upload = Group_Upload(container_name = container_name, compressed_file_name_short_with_extension = compressed_file_name_short_with_extension, compressed_file_name_long_with_extension =  compressed_file_name_long_with_extension,  user_id = user.id)
            db.session.add(group_upload)
            db.session.commit()
        
    except Exception as e:
        print(e)




def delete_all():
    block_blob_service = BlockBlobService(account_name='mednlpstorage', account_key='v+IgtNIIRhZjqMZx+e886rhJMVAhIUoUfG252SVIftBCyx8bG+NE0apP20xakOsMRQfNZFbUggUUULN2JER8lg==')
    current_username  = current_user.username
    user = User.query.filter_by(username=current_username).first()
    user_id = user.id
    single_files = Single_Upload.query.filter_by(user_id=user_id)
    group_files = Group_Upload.query.filter_by(user_id=user_id)

    for x in single_files:
        container_name = x.container_name
        block_blob_service.delete_container(container_name)
        db.session.delete(x)

    for x in group_files:
        container_name = x.container_name
        block_blob_service.delete_container(container_name)
        db.session.delete(x)

    db.session.commit()
    
