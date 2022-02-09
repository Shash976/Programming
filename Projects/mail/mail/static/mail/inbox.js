document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  const submit = document.querySelector('#submit');
  const newEmail = document.querySelector('#compose-subject');
/*
  // Disable submit button by default:
  submit.disabled = true;

  // Listen for input to be typed into the input field
  newEmail.onkeyup = () => {
      if (newEmail.value.length > 0) {
          submit.disabled = false;
      }
      else {
          submit.disabled = true;
      }
  }
*/
  // Listen for submission of form
  document.querySelector('form').onsubmit = () => {
    // Find the task the user just submitted
    let body = document.querySelector('#compose-body').value;
    let subject = document.querySelector('#compose-subject').value;
    let recipients = document.querySelector('#compose-recipients').value;
    console.log(`To: ${recipients}, ${subject} - ${body}`);
    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
          recipients: recipients,
          subject: subject,
          body: body
      })
    })
    .then(response => response.json())
    .then(result => {
        // Print result
        console.log(result);
        if (result.message == 'Email sent successfully.'){
          load_mailbox('inbox')
        }
    })
    return false;
  }
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3><br/><ul id="emails"></ul>`;
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => { 
      // Print emails
      console.log(emails),
      emails.forEach(email=> {
        console.log(email)
        const newLI = document.createElement('li')
        newLI.innerHTML = `${email.subject} - ${email.sender}  ${email.body}`
        document.querySelector('#emails').append(newLI)
      // ... do something else with emails ..
      });
    });
}