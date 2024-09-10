# Remove 'example.' from the filename and replace necessary values with yours

# Email configuration
email_config = dict(
    sender_address = 'email@email.com',
    sender_password = 'password',
    sender_smtp_server = 'some-server.com',
    sender_smtp_port = 587
)
# Email message text
email_text = dict(
    subject = 'Closest appointment',
    body_start = '',
    sent_from = 'sender_email@email.com',
    sent_to = 'receiver_email@email.com'
)
# Info to navigate website with
site_attributes = dict(
    send_mail_if_year = 2024,
    check_for_doctor_name = 'Name Lastname'
)