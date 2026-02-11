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
    # Reload env to pick up latest changes
    load_dotenv()
    
    server_host = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    server_port = int(os.getenv("SMTP_PORT", 587))
    username = os.getenv("SMTP_USERNAME")
    password = os.getenv("SMTP_PASSWORD")
    frontend_url = os.getenv("FRONTEND_URL", "https://vrikshafrontend.vercel.app")

    if not username or not password:
        print("Email not sent: SMTP credentials not configured in environment variables.")
        return False

    try:
        # Create message container
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Vriksha Command Center - Access Granted"
        msg['From'] = f"Vriksha Admin <{username}>"
        msg['To'] = user_email

        # Create the HTML body
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
                        You’ve been granted access to the <b>Vriksha Command Center</b> by your CEO. 
                        You can now track project progress, manage deals, and collaborate with the team on the dashboard.
                    </p>
                </div>

                <div style="text-align: center; margin-bottom: 30px;">
                    <a href="{frontend_url}" style="background: linear-gradient(135deg, #a8e6cf 0%, #dcedc1 100%); color: #2d5a27; padding: 16px 32px; border-radius: 12px; text-decoration: none; font-weight: 700; font-size: 16px; display: inline-block; box-shadow: 0 10px 20px rgba(129, 199, 132, 0.2);">
                        Open Dashboard
                    </a>
                </div>

                <div style="border-top: 1px solid #f1f5f9; padding-top: 20px; text-align: center;">
                    <p style="font-size: 14px; color: #b2bec3;">
                        Login using your registered email: <b>{user_email}</b>
                    </p>
                    <p style="font-size: 12px; color: #b2bec3; margin-top: 20px;">
                        © 2026 Vriksha Team. All rights reserved.
                    </p>
                </div>
            </div>
        </body>
        </html>
        """

        # Attach HTML
        msg.attach(MIMEText(html, 'html'))

        # Send the email
        with smtplib.SMTP(server_host, server_port) as server:
            server.starttls()
            server.login(username, password)
            server.sendmail(username, user_email, msg.as_string())
            
        print(f"Welcome email successfully sent to {user_email}")
        return True

    except Exception as e:
        print(f"Error sending welcome email: {str(e)}")
        return False
