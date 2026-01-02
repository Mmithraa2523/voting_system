import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import List, Optional
from datetime import datetime
import threading
from flask import current_app
from flask_mail import Mail, Message

class EmailService:
    def __init__(self, mail_instance: Mail = None):
        self.mail = mail_instance

    def _send_email_async(self, app, msg):
        """Send email in a separate thread"""
        try:
            with app.app_context():
                self.mail.send(msg)
                app.logger.info(f"Email sent successfully to {msg.recipients}")
        except Exception as e:
            app.logger.error(f"Failed to send email: {str(e)}")

    def send_vote_confirmation(self, voter_email: str, voter_name: str, 
                             choice: str, audit_ref: str) -> bool:
        """Send vote confirmation email to voter"""
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            subject = "Your vote has been recorded"
            body = f"""Dear {voter_name},

Your vote has been successfully recorded in the Smart Voting System.

Vote Details:
- Choice: {choice}
- Reference ID: {audit_ref}
- Timestamp: {timestamp}

Thank you for participating in the democratic process.

Best regards,
Election Commission"""

            msg = Message(
                subject=subject,
                recipients=[voter_email],
                body=body
            )

            # Send asynchronously
            app = current_app._get_current_object()
            thread = threading.Thread(target=self._send_email_async, args=(app, msg))
            thread.daemon = True
            thread.start()

            return True

        except Exception as e:
            current_app.logger.error(f"Error sending vote confirmation: {str(e)}")
            return False

    def send_auth_failure_alert(self, voter_id_input: str, voter_email: str,
                              distance: float, snapshot_path: str,
                              ip_address: str, user_agent: str) -> bool:
        """Send authentication failure alert with photo attachment"""
        try:
            timestamp_utc = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
            timestamp_local = datetime.now().strftime("%Y-%m-%d %H:%M:%S Local")

            subject = f"ALERT: Face authentication failure for Voter ID {voter_id_input}"

            body = f"""SECURITY ALERT - AUTHENTICATION FAILURE

A face authentication attempt has failed for the following voter:

Voter ID: {voter_id_input}
Distance Score: {distance:.4f}
Timestamp (UTC): {timestamp_utc}
Timestamp (Local): {timestamp_local}
IP Address: {ip_address}
User Agent: {user_agent}

A photo of the authentication attempt has been captured and is attached to this email.

Please investigate this incident immediately.

Best regards,
Smart Voting System Security"""

            # Send to election commissioner
            commissioner_email = current_app.config.get('ALERT_RECIPIENT')
            recipients = [commissioner_email]

            # Also send to voter if email is available
            if voter_email:
                recipients.append(voter_email)

            msg = Message(
                subject=subject,
                recipients=recipients,
                body=body
            )

            # Attach snapshot if available
            if snapshot_path and os.path.exists(snapshot_path):
                with current_app.open_resource(snapshot_path, 'rb') as fp:
                    msg.attach(
                        filename=f"auth_failure_{voter_id_input}_{timestamp_utc.replace(' ', '_').replace(':', '-')}.jpg",
                        content_type="image/jpeg",
                        data=fp.read()
                    )

            # Send asynchronously
            app = current_app._get_current_object()
            thread = threading.Thread(target=self._send_email_async, args=(app, msg))
            thread.daemon = True
            thread.start()

            return True

        except Exception as e:
            current_app.logger.error(f"Error sending auth failure alert: {str(e)}")
            return False

    def send_auth_success(self, voter_email: str, voter_name: str) -> bool:
        """Send authentication success email to voter"""
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            subject = "Authentication Successful - Smart Voting System"
            body = f"""Dear {voter_name},

You have successfully authenticated with the Smart Voting System using face recognition.

Authentication Details:
- Timestamp: {timestamp}
- Status: VERIFIED

You may now proceed to cast your vote.

Best regards,
Election Commission"""

            msg = Message(
                subject=subject,
                recipients=[voter_email],
                body=body
            )

            # Send asynchronously
            app = current_app._get_current_object()
            thread = threading.Thread(target=self._send_email_async, args=(app, msg))
            thread.daemon = True
            thread.start()

            return True

        except Exception as e:
            current_app.logger.error(f"Error sending auth success email: {str(e)}")
            return False

    def send_test_email(self, recipient: str) -> bool:
        """Send a test email to verify configuration"""
        try:
            subject = "Smart Voting System - Email Configuration Test"
            body = """This is a test email to verify that the Smart Voting System email configuration is working correctly.

If you receive this email, the system is properly configured to send notifications.

Best regards,
Smart Voting System"""

            msg = Message(
                subject=subject,
                recipients=[recipient],
                body=body
            )

            # Send synchronously for testing
            self.mail.send(msg)
            return True

        except Exception as e:
            current_app.logger.error(f"Error sending test email: {str(e)}")
            return False