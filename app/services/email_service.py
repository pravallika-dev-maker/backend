import os
from dotenv import load_dotenv
import resend

load_dotenv()

def send_welcome_email(user_email, user_name):
    """
    Sends a premium welcome email to a newly authorized user using Resend API.
    This bypasses Railway's SMTP port restrictions by using HTTP instead.
    """
    print(f"DEBUG: Starting Resend email process for {user_email}")
    
    # Get Resend API credentials
    api_key = os.getenv("RESEND_API_KEY")
    from_email = os.getenv("RESEND_FROM_EMAIL", "onboarding@resend.dev")
    frontend_url = os.getenv("FRONTEND_URL", "https://vrikshafrontend.vercel.app")

    if not api_key:
        print("CRITICAL: RESEND_API_KEY not found in environment variables!")
        print("ACTION: Add RESEND_API_KEY to your Railway Variables.")
        return False

    try:
        # Set the API key
        resend.api_key = api_key
        
        # Create the premium HTML email
        html_content = f"""
        <html>
        <body style="font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background-color: #f0f4f0; padding: 40px; margin: 0;">
            <div style="max-width: 600px; margin: 0 auto; background: white; border-radius: 24px; padding: 40px; box-shadow: 0 10px 30px rgba(0,0,0,0.05); border: 1px solid #e2e8f0;">
                <div style="text-align: center; margin-bottom: 30px;">
                    <h1 style="color: #2d3436; font-size: 28px; font-weight: 800; letter-spacing: -0.04em; margin: 0;">Vriksha Command Center</h1>
                    <p style="color: #636e72; font-size: 16px; margin-top: 8px; margin-bottom: 0;">Internal Project & Deal Tracking System</p>
                </div>
                
                <div style="margin-bottom: 30px;">
                    <p style="font-size: 18px; font-weight: 600; color: #2d3436; margin-bottom: 12px;">Hi {user_name},</p>
                    <p style="font-size: 16px; line-height: 1.6; color: #636e72; margin: 0;">
                        You've been granted access to the <strong style="color: #2d3436;">Vriksha Command Center</strong> by your CEO. 
                        You can now track project progress, manage deals, and collaborate with the team on the dashboard.
                    </p>
                </div>

                <div style="text-align: center; margin: 32px 0;">
                    <a href="{frontend_url}" style="display: inline-block; background: linear-gradient(135deg, #a8e6cf 0%, #81c784 100%); color: #1b5e20; padding: 16px 32px; border-radius: 12px; text-decoration: none; font-weight: 700; font-size: 16px; box-shadow: 0 4px 12px rgba(129, 199, 132, 0.3);">
                        Open Dashboard →
                    </a>
                </div>

                <div style="border-top: 1px solid #f1f5f9; padding-top: 20px; margin-top: 32px;">
                    <p style="font-size: 14px; color: #b2bec3; text-align: center; margin: 8px 0;">
                        Login using your registered email: <strong style="color: #636e72;">{user_email}</strong>
                    </p>
                    <p style="font-size: 12px; color: #b2bec3; text-align: center; margin: 20px 0 0 0;">
                        © 2026 Vriksha Team. All rights reserved.
                    </p>
                </div>
            </div>
        </body>
        </html>
        """

        print(f"DEBUG: Sending email via Resend API...")
        
        # Send email using Resend
        params = {
            "from": from_email,
            "to": [user_email],
            "subject": "Vriksha Command Center - Access Granted",
            "html": html_content,
        }
        
        response = resend.Emails.send(params)
        
        print(f"SUCCESS: Email sent to {user_email} via Resend!")
        print(f"DEBUG: Resend response: {response}")
        return True
        
    except Exception as e:
        import traceback
        print(f"CRITICAL: Resend email error: {str(e)}")
        print(traceback.format_exc())
        return False
