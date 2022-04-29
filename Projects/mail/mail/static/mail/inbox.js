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
  //
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
        const newM = document.createElement('div');
        newM.className = 'email'
        newM.innerHTML = `<li><div class='mail'><p class="details">${email.sender}:  ${email.subject}  (${email.timestamp})</p></div><button class="archive">Archive</button></li>`;
        archive = newM.querySelector('.archive');
        archive.style.display = 'none';
        newM.querySelector('.details').style.float = 'none';
        // Check for read email
        if (email.read==true) {
          newM.style.background = 'gray';
        } else {
          newM.style.border = '1px solid black'
          newM.style.background = 'white';
        };
        // Check Mailbox
        // Archiving Emails
        archive_email(newM, email.id, mailbox)
        newM.querySelector('.mail').addEventListener('click', () => load_email(email.id));
        document.querySelector('#emails').append(newM);
      });
    });
};

function archive_email(element, email_id, mailbox){
  element.addEventListener('mouseover', () => {
    element.querySelector('.archive').style.display = 'block';
    element.querySelector('.details').style.float = 'left';
    element.style.background = '#bdbbbb';
    if (mailbox == 'archive') {
      element.querySelector('.archive').innerHTML = 'Unarchive';
    }
    element.querySelector('.archive').addEventListener('click', () => {
      if (mailbox == 'archive') {
        fetch(`/emails/${email_id}`, {
          method: 'PUT',
          body: JSON.stringify({
            archived: false
          })
        })
      } else {
        fetch(`/emails/${email_id}`, {
          method: 'PUT',
          body: JSON.stringify({
            archived: true
          })
        })
      }
      element.style.animationPlayState = 'running';
      element.addEventListener('animationend', () => {
        element.remove()
      })
    });
  });
  element.addEventListener('mouseout', () => {
    element.querySelector('.archive').style.display = 'none';
    element.querySelector('.details').style.float = 'none';
    element.style.background = 'gray';
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
    document.querySelector('#email').innerHTML = `<h5>From: ${email.sender} <br/> To: ${email.recipients} <br/></h5><br><p>${email.body}</p>`
  })
  fetch(`/emails/${email_id}`, {
    method: 'PUT',
    body: JSON.stringify({
        read: true
    })
  }) 
}
