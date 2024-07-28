gauth = GoogleAuth()
gauth.LoadCredentialsFile("mycreds.txt")
if gauth.credentials is None:
    gauth.LocalWebserverAuth()
elif gauth.access_token_expired:
    gauth.Refresh()
else:
    gauth.Authorize()
gauth.SaveCredentialsFile("mycreds.txt")
drive = GoogleDrive(gauth)

file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
took = False
for file1 in file_list:
	if (file1['title'] == 'nsource'):
		myfile = drive.CreateFile({'id': file1['id']})
		myfile.SetContentString(csv_string)
		myfile.Upload()