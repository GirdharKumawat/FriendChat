const Roomform = document.getElementById('roomForm');

let createBtn = document.getElementById('createBtn');
let cancelBtn = document.getElementById('cancelBtn');
createBtn.addEventListener('click', () => {
    document.getElementById('joinModal').classList.add('active');
});
cancelBtn.addEventListener('click', () => {
    document.getElementById('joinModal').classList.remove('active');
}
);


Roomform.addEventListener('submit', async (e) => {
    e.preventDefault();
    const roomName = document.getElementById('roomName').value;
    const username = document.getElementById('joinUsername').value;
    
  
    
    const response = await fetch(`/getToken/?room=${roomName}`);

    if (!response.ok) {
        console.error('Failed to get token');
        return;
    }
    const data = await response.json();
   
    let UID = data.UID;
    let Token = data.token;
     
    sessionStorage.setItem('UID', UID);
    sessionStorage.setItem('token', Token);
    sessionStorage.setItem('room', roomName);
    sessionStorage.setItem('name', username);
    window.open('/room/','_self'); 
   
});

 