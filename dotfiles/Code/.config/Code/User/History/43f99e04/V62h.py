import os
import time
import io
import google.generativeai as genai
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

# --- CONFIGURATION ---
GEMINI_API_KEY = "AIzaSyDecHLxkNpEfQb9t5ZPVsj3RLCecCowbaw"
SPREADSHEET_ID = "1SmonHbLCcG26K8n2a8BCr2MY6zu46iCxpqgUvfF-7vM"
CLIENT_SECRETS_FILE = "credentials.json"
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive.readonly',
    'https://www.googleapis.com/auth/documents'
]

genai.configure(api_key=GEMINI_API_KEY)

def get_services():
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    creds = flow.run_local_server(port=0)
    return build('sheets', 'v4', credentials=creds), build('drive', 'v3', credentials=creds), build('docs', 'v1', credentials=creds)

def download_video(drive_service, file_id, filename):
    print(f"Downloading {filename}...")
    request = drive_service.files().get_media(fileId=file_id)
    fh = io.FileIO(filename, 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
        print(f"Download {int(status.progress() * 100)}%.")
    return filename

def process_with_gemini(video_path):
    print("Uploading to Gemini...")
    video_file = genai.upload_file(path=video_path)
    
    while video_file.state.name == "PROCESSING":
        time.sleep(5)
        video_file = genai.get_file(video_file.name)
    
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    prompt = """
    1. Transcribe this video verbatim. 
    2. After the transcript, write '===SEP==='
    3. Provide a Summary, Meeting Details (Loan, Property, Challenges), and Next Steps for the advisor.
    """
    response = model.generate_content([video_file, prompt])
    return response.text

def create_tabbed_doc(docs_service, title, content_raw):
    # Split AI response
    parts = content_raw.split('===SEP===')
    transcript = parts[0] if len(parts) > 0 else "No transcript found."
    summary = parts[1] if len(parts) > 1 else "No summary found."

    # 1. Create Doc
    doc = docs_service.documents().create(body={'title': f"AI Analysis: {title}"}).execute()
    doc_id = doc.get('documentId')

    # 2. Add Tabs (Using the new Document Tabs API features)
    requests = [
        {
            "createTab": {
                "tabProperties": {"title": "Raw Transcript"}
            }
        },
        {
            "updateTabProperties": {
                "tabId": "t.0", 
                "tabProperties": {"title": "Summary & Next Steps"},
                "fields": "title"
            }
        }
    ]
    
    # We execute batchUpdate to create tabs
    response = docs_service.documents().batchUpdate(documentId=doc_id, body={'requests': requests}).execute()
    new_tab_id = response['replies'][0]['createTab']['tabId']

    # 3. Insert Text into specific tabs
    write_requests = [
        {
            "insertText": {
                "location": {"tabId": "t.0", "index": 1},
                "text": summary
            }
        },
        {
            "insertText": {
                "location": {"tabId": new_tab_id, "index": 1},
                "text": transcript
            }
        }
    ]
    docs_service.documents().batchUpdate(documentId=doc_id, body={'requests': write_requests}).execute()
    return f"https://docs.google.com/document/d/{doc_id}/edit"

def main():
    sheets, drive, docs = get_services()
    
    # 1. Pull data from Columns A and B
    # A is usually the Link, B is usually empty (where we will put the Doc Link)
    sheet_data = sheets.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID, 
        range="Sheet1!A2:B" # Adjust "Sheet1" if your tab name is different
    ).execute()
    
    rows = sheet_data.get('values', [])

    if not rows:
        print("No data found in the sheet.")
        return

    for i, row in enumerate(rows):
        # SKIP EMPTY ROWS
        if not row or len(row) == 0:
            continue
            
        # FIX: Use index 0 if the link is in Column A
        video_url = row[0] 
        
        # Check if it's actually a link
        if "drive.google.com" not in video_url:
            print(f"Skipping row {i+2}: Not a valid Drive link.")
            continue
            
        try:
            file_id = video_url.split('/d/')[1].split('/')[0]
            
            # Download, Process, and Create
            local_filename = f"temp_video_{i}.mp4"
            download_video(drive, file_id, local_filename)
            
            ai_result = process_with_gemini(local_filename)
            
            # Use the filename from Drive for the Doc title
            drive_file = drive.files().get(fileId=file_id).execute()
            meeting_name = drive_file.get('name', f"Meeting {i+1}")
            
            doc_link = create_tabbed_doc(docs, meeting_name, ai_result)
            
            # 2. PASTE THE LINK IN COLUMN B
            # This puts the new Doc link right next to the video link
            sheets.spreadsheets().values().update(
                spreadsheetId=SPREADSHEET_ID,
                range=f"Sheet1!B{i+2}", 
                valueInputOption="USER_ENTERED",
                body={"values": [[doc_link]]}
            ).execute()
            
            os.remove(local_filename) 
            print(f"✅ Success! Doc created: {doc_link}")
            
        except Exception as e:
            print(f"❌ Error on row {i+2}: {e}")

if __name__ == "__main__":
    main()
