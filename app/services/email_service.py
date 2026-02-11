import os
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

load_dotenv()

def send_welcome_email(user_email, user_name):
    """
    Sends a premium welcome email to a newly authorized user using SendGrid API.
    This bypasses Railway's SMTP port restrictions by using HTTP instead.
    """
    print(f"DEBUG: Starting SendGrid email process for {user_email}")
    
    # Get SendGrid API credentials from environment
    api_key = os.getenv("SENDGRID_API_KEY")
    from_email = os.getenv("FROM_EMAIL", "pravallika@vriksha.ai")
    frontend_url = os.getenv("FRONTEND_URL", "https://vrikshafrontend.vercel.app")

    if not api_key:
        print("CRITICAL: SENDGRID_API_KEY not found in environment variables!")
        print("ACTION: Add SENDGRID_API_KEY to your Railway Variables.")
        return False

    try:
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

        print(f"DEBUG: Sending email via SendGrid API...")
        
        # Create SendGrid message
        message = Mail(
            from_email=from_email,
            to_emails=user_email,
            subject='Vriksha Command Center - Access Granted',
            html_content=html_content
        )
        
        # Initialize client and send
        sg = SendGridAPIClient(api_key)
        response = sg.send(message)
        
        print(f"SUCCESS: Email sent to {user_email} via SendGrid!")
        print(f"DEBUG: SendGrid status code: {response.status_code}")
        return True
        
    except Exception as e:
        import traceback
        print(f"CRITICAL: SendGrid email error: {str(e)}")
        print(traceback.format_exc())
        return False

def send_project_assignment_email(user_email, user_name, project_name, role):
    """
    Sends an email to a user notifying them that they have been added to a new project.
    """
    print(f"DEBUG: Notifying {user_email} of project assignment: {project_name}")
    
    api_key = os.getenv("SENDGRID_API_KEY")
    from_email = os.getenv("FROM_EMAIL", "pravallika@vriksha.ai")
    frontend_url = os.getenv("FRONTEND_URL", "https://vrikshafrontend.vercel.app")

    if not api_key:
        return False

    try:
        html_content = f"""
        <html>
        <body style="font-family: 'Inter', sans-serif; background-color: #f0f4f0; padding: 40px;">
            <div style="max-width: 600px; margin: 0 auto; background: white; border-radius: 24px; padding: 40px; border: 1px solid #e2e8f0;">
                <h1 style="color: #2d3436; text-align: center;">Vriksha Project Assignment</h1>
                <p style="font-size: 16px; color: #636e72;">Hi {user_name},</p>
                <p style="font-size: 16px; line-height: 1.6; color: #636e72;">
                    You have been assigned to a new project: <strong style="color: #2d3436;">{project_name}</strong>.
                </p>
                <div style="background: #f8fafc; padding: 20px; border-radius: 12px; margin: 20px 0;">
                    <p style="margin: 0; color: #475569;"><strong>Role:</strong> {role}</p>
                </div>
                <div style="text-align: center; margin: 30px 0;">
                    <a href="{frontend_url}" style="background: #81c784; color: white; padding: 16px 32px; border-radius: 12px; text-decoration: none; font-weight: 700;">
                        View Project in Dashboard
                    </a>
                </div>
            </div>
        </body>
        </html>
        """
        
        message = Mail(
            from_email=from_email,
            to_emails=user_email,
            subject=f'New Project Assignment: {project_name}',
            html_content=html_content
        )
        
        sg = SendGridAPIClient(api_key)
        sg.send(message)
        print(f"SUCCESS: Assignment email sent to {user_email}")
        return True
    except Exception as e:
        print(f"ERROR: Failed to send assignment email: {e}")
        return False
