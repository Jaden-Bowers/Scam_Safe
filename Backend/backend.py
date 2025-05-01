# Backend api server
# talks to OpenAI api, mail server, and frontend

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from pydantic import BaseModel
import os
import asyncio
import json
from openai import OpenAI
from dotenv import load_dotenv
from fastapi import Body

load_dotenv()

# Create your own .env file and add your open ai api key name it `OPENAI_API_KEY`
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()
active_sessions = {}

# Handle sending email to gpt
async def analyze_email(email_data):
    extension = email_data['recipients'][0].split('@')[0].replace('fwrd2me_', '')
    subject = email_data['subject'][:100] if email_data['subject'] else "[No Subject]"
    print(f"Sending Email for Analysis: {extension} : {subject}")

    # content of the email
    email_summary = f"""
    Email Scam Analysis Request:

    - From: {email_data['sender']}
    - To: {', '.join(email_data['recipients'])}
    - Date: {email_data['date']}
    - Subject: {email_data['subject']}

    Body:
    {email_data['body']}
    """

    # Prompt sent to gpt
    prompt = f"""
    Note do not use bolding or any `*` in your response.

    Here is the email: {email_summary}

    Your Response should be formatted as follows.

    Based on the information fowarded email, the email does/does not seem to be a scam. Here is a deatailed analysis:

    1. Sender Email Address:
    - ... Sender Email Address Analysis ...

    2. Subject Line:
    - ... Subject Line Analysis ...

    3. Email Headers:
    - ... Email Headers Analysis ... --[Note ignore the recipient address *_fwrd2me.xyz this is a temp email the possible scam email was sent to for you to analyze]--

    4. Email Body:
    - ... Email Body Analysis ...

    5. MISC:
    - ... Anything extra you want to add ...

    Overall, ... Your Conclusion ...
    """

    try:
        # Sending email to gpt for analysis
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an AI trained to detect email scams. Analyze the email headers, sender, subject, and body to determine if this is a scam. Provide detailed reasoning. Note all emails will be fowarded to you so ignore the fowarding addresses and such and focus on the mail email, sender, and original target."},
                {"role": "user", "content": prompt}
            ]
        )
        result = completion.choices[0].message.content
        print(f"Analysis Received: {extension} : {result[:60].replace('\n', ' ')}...")
        return result
    except Exception as e:
        print(f"Analysis Error: {extension} : {str(e)}")
        return f"Error analyzing email: {str(e)}"


# Function for sending updates via the websocket to the frontend
async def send_ws_event(email, event_type, message):
    if email in active_sessions:
        socket = active_sessions[email]["socket"]
        await socket.send_text(json.dumps({
            "event": event_type,
            "message": message
        }))


# Handling recieving the email from mail server
@app.post("/receive-email/")
async def receive_email(email_data: dict = Body(...)):
    sender = email_data.get("sender")
    recipient = email_data.get("recipients", [""])[0]
    subject = email_data.get("subject")
    body = email_data.get("body") or "[No plain body found]"

    extension = recipient.split('@')[0].replace('fwrd2me_', '')
    subj_display = subject[:100] if subject else "[No Subject]"
    print(f"Email Received: {extension} : {subj_display}")

    # Frontend logging
    await send_ws_event(recipient, "email_received", f"Email received: {subj_display}")
    await send_ws_event(recipient, "analysis_started", f"Sending to AI for analysis: {subj_display}")

    analysis = await analyze_email(email_data)

    if recipient in active_sessions:
        try:
            await send_ws_event(recipient, "analysis_result", analysis)
            print(f"Analysis Sent via WebSocket: {extension}")
            return {"message": "Analysis sent to frontend"}
        except Exception as e:
            print(f"WebSocket Send Error: {extension} : {str(e)}")
            return {"message": "WebSocket send failed"}
    else:
        print(f"No Active WebSocket for: {extension}")
        return {"message": "No active session for recipient email"}


# Handle creation of websocket connection
@app.websocket("/ws/{temp_email}")
async def websocket_endpoint(websocket: WebSocket, temp_email: str):
    await websocket.accept()
    active_sessions[temp_email] = {"socket": websocket}
    extension = temp_email.replace('fwrd2me_', '')
    print(f"WebSocket Connected: {extension}")

    try:
        while True:
            await asyncio.sleep(30)
    except WebSocketDisconnect:
        print(f"WebSocket Disconnected: {extension}")
    finally:
        active_sessions.pop(temp_email, None)


@app.get("/health")
def health_check():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
