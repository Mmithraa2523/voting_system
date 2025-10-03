"""
Email service using Resend integration for sending notifications
"""
import os
import requests
from typing import Optional
from datetime import datetime
from flask import current_app


class ResendEmailService:
    """Email service using Resend API"""
    
    def __init__(self):
        self.hostname = os.environ.get('REPLIT_CONNECTORS_HOSTNAME')
        self.x_replit_token = None
        
        # Get authentication token
        if os.environ.get('REPL_IDENTITY'):
            self.x_replit_token = 'repl ' + os.environ.get('REPL_IDENTITY')
        elif os.environ.get('WEB_REPL_RENEWAL'):
            self.x_replit_token = 'depl ' + os.environ.get('WEB_REPL_RENEWAL')
        
        self.connection_settings = None
    
    def _get_credentials(self):
        """Fetch Resend API credentials from Replit connectors"""
        if not self.hostname or not self.x_replit_token:
            current_app.logger.warning("Resend not configured - email notifications disabled")
            return None
        
        try:
            response = requests.get(
                f'https://{self.hostname}/api/v2/connection?include_secrets=true&connector_names=resend',
                headers={
                    'Accept': 'application/json',
                    'X_REPLIT_TOKEN': self.x_replit_token
                }
            )
            response.raise_for_status()
            data = response.json()
            
            if data.get('items') and len(data['items']) > 0:
                self.connection_settings = data['items'][0]
                return {
                    'api_key': self.connection_settings['settings'].get('api_key'),
                    'from_email': self.connection_settings['settings'].get('from_email')
                }
            
            current_app.logger.warning("Resend connection not found")
            return None
            
        except Exception as e:
            current_app.logger.error(f"Failed to get Resend credentials: {str(e)}")
            return None
    
    def _send_email(self, to_email: str, subject: str, html_body: str, text_body: str) -> bool:
        """Send email using Resend API"""
        credentials = self._get_credentials()
        
        if not credentials or not credentials.get('api_key'):
            current_app.logger.warning("Cannot send email - Resend not configured")
            return False
        
        try:
            response = requests.post(
                'https://api.resend.com/emails',
                headers={
                    'Authorization': f"Bearer {credentials['api_key']}",
                    'Content-Type': 'application/json'
                },
                json={
                    'from': credentials.get('from_email', 'Smart Voting System <onboarding@resend.dev>'),
                    'to': [to_email],
                    'subject': subject,
                    'html': html_body,
                    'text': text_body
                }
            )
            
            if response.status_code == 200:
                current_app.logger.info(f"Email sent successfully to {to_email}")
                return True
            else:
                current_app.logger.error(f"Failed to send email: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            current_app.logger.error(f"Error sending email: {str(e)}")
            return False
    
    def send_vote_confirmation(self, voter_email: str, voter_name: str, 
                              choice: str, audit_ref: str) -> bool:
        """Send vote confirmation email to voter"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        subject = "Your vote has been recorded"
        
        text_body = f"""Dear {voter_name},

Your vote has been successfully recorded in the Smart Voting System.

Vote Details:
- Choice: {choice}
- Reference ID: {audit_ref}
- Timestamp: {timestamp}

Thank you for participating in the democratic process.

Best regards,
Election Commission"""

        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 8px;">
                <h2 style="color: #28a745;">✓ Vote Recorded Successfully</h2>
                <p>Dear {voter_name},</p>
                <p>Your vote has been successfully recorded in the Smart Voting System.</p>
                
                <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
                    <h3 style="margin-top: 0;">Vote Details:</h3>
                    <ul style="list-style: none; padding: 0;">
                        <li><strong>Choice:</strong> {choice}</li>
                        <li><strong>Reference ID:</strong> {audit_ref}</li>
                        <li><strong>Timestamp:</strong> {timestamp}</li>
                    </ul>
                </div>
                
                <p>Thank you for participating in the democratic process.</p>
                <p style="margin-top: 30px;">Best regards,<br><strong>Election Commission</strong></p>
            </div>
        </body>
        </html>
        """
        
        return self._send_email(voter_email, subject, html_body, text_body)
    
    def send_auth_failure_alert(self, voter_id_input: str, voter_email: str,
                               distance: float, snapshot_path: str,
                               ip_address: str, user_agent: str) -> bool:
        """Send authentication failure alert"""
        timestamp_utc = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        timestamp_local = datetime.now().strftime("%Y-%m-%d %H:%M:%S Local")
        
        subject = f"ALERT: Face authentication failure for Voter ID {voter_id_input}"
        
        text_body = f"""SECURITY ALERT - AUTHENTICATION FAILURE

A face authentication attempt has failed for the following voter:

Voter ID: {voter_id_input}
Distance Score: {distance:.4f}
Timestamp (UTC): {timestamp_utc}
Timestamp (Local): {timestamp_local}
IP Address: {ip_address}
User Agent: {user_agent}

Please investigate this incident immediately.

Best regards,
Smart Voting System Security"""

        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 2px solid #dc3545; border-radius: 8px; background-color: #fff5f5;">
                <h2 style="color: #dc3545;">⚠️ SECURITY ALERT - AUTHENTICATION FAILURE</h2>
                <p>A face authentication attempt has failed for the following voter:</p>
                
                <div style="background-color: #ffffff; padding: 15px; border-radius: 5px; margin: 20px 0; border-left: 4px solid #dc3545;">
                    <h3 style="margin-top: 0; color: #dc3545;">Incident Details:</h3>
                    <ul style="list-style: none; padding: 0;">
                        <li><strong>Voter ID:</strong> {voter_id_input}</li>
                        <li><strong>Distance Score:</strong> {distance:.4f}</li>
                        <li><strong>Timestamp (UTC):</strong> {timestamp_utc}</li>
                        <li><strong>Timestamp (Local):</strong> {timestamp_local}</li>
                        <li><strong>IP Address:</strong> {ip_address}</li>
                        <li><strong>User Agent:</strong> {user_agent}</li>
                    </ul>
                </div>
                
                <p style="color: #dc3545; font-weight: bold;">Please investigate this incident immediately.</p>
                <p style="margin-top: 30px;">Best regards,<br><strong>Smart Voting System Security</strong></p>
            </div>
        </body>
        </html>
        """
        
        # Send to election commissioner
        commissioner_email = current_app.config.get('ALERT_RECIPIENT')
        if commissioner_email:
            self._send_email(commissioner_email, subject, html_body, text_body)
        
        # Also notify voter if email available
        if voter_email:
            self._send_email(voter_email, subject, html_body, text_body)
        
        return True
    
    def send_auth_success(self, voter_email: str, voter_name: str) -> bool:
        """Send authentication success email to voter"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        subject = "Authentication Successful - Smart Voting System"
        
        text_body = f"""Dear {voter_name},

You have successfully authenticated with the Smart Voting System using face recognition.

Authentication Details:
- Timestamp: {timestamp}
- Status: VERIFIED

You may now proceed to cast your vote.

Best regards,
Election Commission"""

        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 8px;">
                <h2 style="color: #28a745;">✓ Authentication Successful</h2>
                <p>Dear {voter_name},</p>
                <p>You have successfully authenticated with the Smart Voting System using face recognition.</p>
                
                <div style="background-color: #d4edda; padding: 15px; border-radius: 5px; margin: 20px 0; border-left: 4px solid #28a745;">
                    <h3 style="margin-top: 0; color: #155724;">Authentication Details:</h3>
                    <ul style="list-style: none; padding: 0;">
                        <li><strong>Timestamp:</strong> {timestamp}</li>
                        <li><strong>Status:</strong> VERIFIED ✓</li>
                    </ul>
                </div>
                
                <p>You may now proceed to cast your vote.</p>
                <p style="margin-top: 30px;">Best regards,<br><strong>Election Commission</strong></p>
            </div>
        </body>
        </html>
        """
        
        return self._send_email(voter_email, subject, html_body, text_body)
