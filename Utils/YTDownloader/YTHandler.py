import os
import subprocess
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

class YouTubeVideoDownloader:
    SCOPES = ['https://www.googleapis.com/auth/youtube.upload', 'https://www.googleapis.com/auth/youtube.readonly']
    CREDENTIALS_FILE = 'credentials.json'
    TOKEN_FILE = 'token.json'

    def __init__(self):
        self.creds = None
        self.youtube = None

    def authenticate(self):
        # YT Auth
            if os.path.exists(self.TOKEN_FILE):
                try:
                    self.creds = Credentials.from_authorized_user_file(self.TOKEN_FILE, self.SCOPES)
                except Exception as e:
                    return [False, f"Error in token.josn file"]
            
            if not self.creds or not self.creds.valid:
                if self.creds and self.creds.expired and self.creds.refresh_token:
                    self.creds.refresh(Request())
                else:
                    try: 
                        flow = InstalledAppFlow.from_client_secrets_file(self.CREDENTIALS_FILE, self.SCOPES)
                        self.creds = flow.run_local_server(port=0)
                    except Exception as e:
                        return [False, f"Error in credentials.josn file, {e.strerror}"]
                
                if not self.creds:
                    return [False, f"Error in auth, check the credentials"]
                
                with open(self.TOKEN_FILE, 'w') as token:
                    token.write(self.creds.to_json())

                
            self.youtube = build('youtube', 'v3', credentials=self.creds)
            return [True, 'Auth']


    def get_video_url(self, video_id):
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        return video_url

    def download_video(self, video_id):
        video_url = self.get_video_url(video_id)
        
        import config as c

        command = [
            'yt-dlp', 
            '-f', 'bestvideo+bestaudio/best',
            '--merge-output-format', 'mp4', 
            '--verbose',  
            '--progress',
            '-o', f"{c.video_in}",
            video_url
        ]

        try:
            subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError as e:
            print(f"Error: {e.stderr.decode()}")
            print(f"Output: {e.stdout.decode()}")
            return False

        print(f"Downloaded: {video_url}")
        return True


    def upload_video(self, file_path, title, description="No description", tags=None):
        authRes = self.authenticate()
        if authRes[0] == False:
            return [authRes[1], 3]

        if tags is None:
            tags = []

        body = {
            'snippet': {
                'title': title,
                'description': description,
                'categoryId': '22'  # '22' is the category for 'People & Blogs'
            },
            'status': {
                'privacyStatus': 'unlisted',  # Set video privacy to 'unlisted'
                'selfDeclaredMadeForKids': False  # Indicate that the video is not made for kids
            }
        }

        media = MediaFileUpload(file_path, resumable=True)

        request = self.youtube.videos().insert(
            part='snippet,status',
            body=body,
            media_body=media
        )

        try:
            response = request.execute()
            return [f"Upload successful: https://www.youtube.com/watch?v={response['id']}", 2]
        except Exception as e:
            return [f"Error uploading video: {e}", 3]


if __name__ == "__main__":
    video_id = "ID"  # ID del video unlisted

    downloader = YouTubeVideoDownloader()
    downloader.download_video(video_id)
