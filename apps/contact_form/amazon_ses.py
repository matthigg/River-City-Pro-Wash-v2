def send_email(request_POST):

  import boto3
  from botocore.exceptions import ClientError
  import os

  # Unpack variables
  name, email, phone, message = request_POST['name'], request_POST['email'], request_POST['phone'], request_POST['message']

  # Replace sender@example.com with your "From" address.
  # This address must be verified with Amazon SES.
  SENDER = "<{}>".format(os.environ['RCPW_EMAIL_SENDER'])

  # Replace recipient@example.com with a "To" address. If your account 
  # is still in the sandbox, this address must be verified.
  RECIPIENT = "{}".format(email)

  # If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
  AWS_REGION = "us-east-1"

  # The subject line for the email.
  SUBJECT = "Thank You For Contacting River City Pro Wash!"

  # The email body for recipients with non-HTML email clients.
  BODY_TEXT = ("River City Pro Wash\r\n"
              "Thank You for contacting River City Pro Wash! "
              "A member of our team will contact you as soon as possible. "
              "If you need to contact us immediately, don't hesitate to "
              "call us at (804) 239-6085."
              "Original Message: "
              "Name: {} "
              "Email: {} "
              "Phone: {} "
              "Message: {} ".format(name, email, phone, message)
              )
              
  # The HTML body of the email.
  BODY_HTML = """<html>
  <head></head>
  <body>
    <h1>Thank You For Contacting River City Pro Wash!</h1>
    <p>
      A member of our team will contact you as soon as possible.<br>
      If you need to contact us immediately, don't hesitate to
      call us at (804) 239-6085.
    </p>
    <hr>
    <p>
      <i>Original Message:</i><br>
      Name: {}<br>
      Email: {}<br>
      Phone: {}<br>
      Address: {}<br>
    </p>
  </body>
  </html>
              """.format(name, email, phone, message)

  # The character encoding for the email.
  CHARSET = "UTF-8"

  # Create a new SES resource and specify a region.
  client = boto3.client('ses',region_name=AWS_REGION)

  # Try to send a response email to the person who submitted the contact form.
  try:
    response = client.send_email(
      Destination={
        'ToAddresses': [
          RECIPIENT,
        ],
      },
      Message={
        'Body': {
            'Html': { 'Charset': CHARSET, 'Data': BODY_HTML, },
            'Text': { 'Charset': CHARSET, 'Data': BODY_TEXT, },
          },
          'Subject': { 'Charset': CHARSET, 'Data': SUBJECT, },
        },
        Source=SENDER,
      )
  except ClientError as e:
    print("=== ERROR: User input an invalid email address,", e.response['Error']['Message'])
  else:
    print("Email sent! Message ID:"),
    print(response['MessageId'])

  # Try to send the email to the website owner.
  try:
    response = client.send_email(
      Destination={
        'ToAddresses': [
          os.environ['RCPW_EMAIL_SENDER'],
        ],
      },
      Message={
        'Body': {
            'Html': { 'Charset': CHARSET, 'Data': BODY_HTML, },
            'Text': { 'Charset': CHARSET, 'Data': BODY_TEXT, },
          },
          'Subject': { 'Charset': CHARSET, 'Data': SUBJECT, },
        },
        Source=SENDER,
      )
  except ClientError as e:
    print("=== ERROR: User input an invalid email address,", e.response['Error']['Message'])
  else:
    print("Email sent! Message ID:"),
    print(response['MessageId'])