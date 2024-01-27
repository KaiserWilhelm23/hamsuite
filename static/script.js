function saveContact() {
    const callSign = document.getElementById('callSign').value;
    const name = document.getElementById('name').value;
    const country = document.getElementById('country').value;
    const state = document.getElementById('state').value;
    const locality = document.getElementById('locality').value;
    const date = document.getElementById('date').value;
    const time = document.getElementById('time').value;
  
    const contact = {
      callSign,
      name,
      country,
      state,
      locality,
      date,
      time,
    };
  
    // Retrieve existing contacts or initialize an empty array
    const contacts = JSON.parse(localStorage.getItem('contacts')) || [];
  
    // Add the new contact to the array
    contacts.push(contact);
  
    // Save the updated array back to local storage
    localStorage.setItem('contacts', JSON.stringify(contacts));
  
    // Send the contacts to the server
    saveContactsToServer(contacts);
    
    // Optionally, you can clear the form after saving
    document.getElementById('logForm').reset();
  
    // You can add additional logic here, such as displaying a success message
  }
  
  function saveContactsToServer(contacts) {
    fetch('http://localhost:3000/saveContacts', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ contacts }),
    })
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        console.log('Data sent to server:', data);
        // Optionally, you can handle the server response here
      })
      .catch(error => {
        console.error('Error sending data to server:', error);
        // Optionally, you can handle the error here
      });
  }
  
  var map = L.map('map').setView([0, 0], 2);

  // Add a tile layer (you can choose different tile providers)
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© OpenStreetMap contributors'
  }).addTo(map);