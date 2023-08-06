import os

from django.core.management.base import BaseCommand

from botocore.exceptions import NoCredentialsError

from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    location = 'static/public'
    file_overwrite = True


def get_files(dir_root, files):
    for file in os.listdir(dir_root):
        file_path = '{}{}'.format(dir_root, file)
        if os.path.isdir(file_path):
            files = get_files('{}/'.format(file_path), files)
        else:
            files.append(file_path)

    return files


class Command(BaseCommand):
    def handle(self, *args, **options):
        dir_root = input('Please specify directory path: ')
        files = get_files(dir_root, [])
        success = 0
        try:
            for file in files:
                with open(file, 'rb') as file_obj:
                    file_path_within_bucket = file.replace(dir_root, '')
                    media_storage = StaticStorage()
                    media_storage.save(file_path_within_bucket, file_obj)
                    success += 1
                    print('{}: success'.format(file))
        except FileNotFoundError:
            print("The file was not found")
        except NoCredentialsError:
            print("Credentials not available")
        except Exception:
            print("Upload Unsuccessful")
        finally:
            print('Total file uploaded: {}'.format(success))
