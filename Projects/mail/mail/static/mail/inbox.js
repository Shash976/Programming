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
  document.querySelector('#email-view').style.display = 'none';

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
    })
    load_mailbox('sent')
    return false;
  }
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3><br/><ul id="emails"></ul>`;
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => { 
      // Print emails
      emails.forEach(email=> {
        console.log(email);
        const newM = document.createElement('div');
        newM.className = 'email'
        newM.innerHTML = `<li>${email.sender}:  ${email.subject}  (${email.timestamp})</li>`;
        if (email.read==true) {
          newM.style.background = 'gray';
        } else {
          newM.style.border = '1px solid black'
          newM.style.background = 'white';
        }
        newM.onclick  = () => {
          load_email(email.id)
        }
      });
    });
}

function load_email(email_id) {
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'block';

  fetch(`/emails/${email_id}`)
  .then(response => response.json())
  .then(email => {
    document.querySelector('#email-view').innerHTML = `<h3>${email.subject}</h3><br/><div id="email"></div>`;
    console.log(email)
    document.querySelector('#email').innerHTML = `<h5>From: ${email.sender} <br/> To: ${email.recipients} <br/></h5><p>${email.body}</p>`
  })
  fetch(`/emails/${email_id}`, {
    method: 'PUT',
    body: JSON.stringify({
        read: true
    })
  })

}