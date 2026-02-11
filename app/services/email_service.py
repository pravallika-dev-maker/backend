import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

def send_welcome_email(user_email, user_name):
    """
    Sends a premium welcome email to a newly authorized user.
    """
    print(f"DEBUG: Starting email process for {user_email}")
    
    # Only load .env if NOT running on Railway to avoid overriding dashboard variables
    if not os.getenv("RAILWAY_ENVIRONMENT"):
        load_dotenv()
        print("DEBUG: Local environment detected, loaded .env file.")

    server_host = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    # Try to get port from env, but we'll try to be smart about it
    env_port = os.getenv("SMTP_PORT")
    username = os.getenv("SMTP_USERNAME")
    password = os.getenv("SMTP_PASSWORD")
    frontend_url = os.getenv("FRONTEND_URL", "https://vrikshafrontend.vercel.app")

    if not username or not password:
        print("CRITICAL: SMTP credentials missing. Check Railway Variables!")
        return False

    # Define ports to try (465 is usually more successful on Railway)
    ports_to_try = [465, 587]
    if env_port:
        # If user explicitly set a port, try that first
        ports_to_try = [int(env_port)] + [p for p in [465, 587] if p != int(env_port)]

    last_error = None
    for port in ports_to_try:
        try:
            print(f"DEBUG: Attempting connection via PORT {port}...")
            if port == 465:
                server = smtplib.SMTP_SSL(server_host, port, timeout=15)
            else:
                server = smtplib.SMTP(server_host, port, timeout=15)
                server.starttls()
            
            with server:
                print(f"DEBUG: Successfully connected to {port}. Logging in...")
                server.login(username, password)
                
                # Create message
                msg = MIMEMultipart('alternative')
                msg['Subject'] = "Vriksha Command Center - Access Granted"
                msg['From'] = f"Vriksha Admin <{username}>"
                msg['To'] = user_email

                html = f"""
                <html>
                <body style="font-family: 'Inter', sans-serif; background-color: #f0f4f0; padding: 40px; color: #2d3436;">
                    <div style="max-width: 600px; margin: 0 auto; background: white; border-radius: 24px; padding: 40px; box-shadow: 0 10px 30px rgba(0,0,0,0.05); border: 1px solid #e2e8f0;">
                        <div style="text-align: center; margin-bottom: 30px;">
                            <h1 style="color: #2d3436; font-size: 28px; font-weight: 800; letter-spacing: -0.04em; margin: 0;">Vriksha Command Center</h1>
                            <p style="color: #636e72; font-size: 16px; margin-top: 5px;">Internal Project & Deal Tracking System</p>
                        </div>
                        <div style="margin-bottom: 30px;">
                            <p style="font-size: 18px; font-weight: 600;">Hi {user_name},</p>
                            <p style="font-size: 16px; line-height: 1.6; color: #636e72;">
                                You’ve been granted access to the <b>Vriksha Command Center</b>.
                            </p>
                        </div>
                        <div style="text-align: center; margin-bottom: 30px;">
                            <a href="{frontend_url}" style="background: linear-gradient(135deg, #a8e6cf 0%, #dcedc1 100%); color: #2d5a27; padding: 16px 32px; border-radius: 12px; text-decoration: none; font-weight: 700; font-size: 16px; display: inline-block;">
                                Open Dashboard
                            </a>
                        </div>
                    </div>
                </body>
                </html>
                """
                msg.attach(MIMEText(html, 'html'))
                server.sendmail(username, user_email, msg.as_string())
                print(f"SUCCESS: Email sent to {user_email} via port {port}")
                return True
        except Exception as e:
            print(f"DEBUG: Port {port} failed: {str(e)}")
            last_error = e
            continue

    print(f"CRITICAL: All ports failed. Last error: {str(last_error)}")
    return False
