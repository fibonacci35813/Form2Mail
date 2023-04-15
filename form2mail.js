function sendEmails() {
  var form = FormApp.openById('1lIVPga_WwaHiqheTJbaH_b3iwfU6RuPb0hmSi242Zs8'); // added the script ID, which is the ID of the form
  var formResponses = form.getResponses();
  var emailAddresses = getEmailAddresses(formResponses);
  var emailTemplate = getEmailTemplate(); // Get the email template text
  
  for (var i = 0; i < emailAddresses.length; i++) {
    var email = emailAddresses[i];
    print(email);
    var message = createMessage(email, emailTemplate);
    sendEmail(message);
  }
}

function getEmailAddresses(responses) {
  var emailAddresses = [];
  for (var i = 0; i < responses.length; i++) {
    var response = responses[i];
    var itemResponses = response.getItemResponses();
    for (var j = 0; j < itemResponses.length; j++) {
      var itemResponse = itemResponses[j];
      var title = itemResponse.getItem().getTitle();
      if (title == 'Email') { // Added Email to the title of your Form question that asks for email address
        emailAddresses.push(itemResponse.getResponse());
      }
    }
  }
  return emailAddresses;
}

function getEmailTemplate() {
  // Replace this with your own email template
  var template = 'Dear [NAME],\n\nThank you for submitting the form. We will review your responses and get back to you soon.\n\nBest regards,\n[SENDER NAME]';
  return template;
}

function createMessage(to, template) {
  var name = to.split('@')[0]; // Extract name from email address
  var body = template.replace('[NAME]', name).replace('Satyam Kumar', 'John Doe'); // Replace placeholders with actual values
  var message = {
    to: to,
    subject: 'Thank you for submitting the form',
    htmlBody: body
  };
  return message;
}

function sendEmail(message) {
  var thread = GmailApp.sendEmail(message.to, message.subject, message.htmlBody);
  Logger.log('Message sent to ' + message.to + ', Thread ID: ' + thread.getId());
}

