document.addEventListener('DOMContentLoaded', function() {
    const addUserForm = document.getElementById('addUserForm');
    const userTable = document.getElementById('userTable').getElementsByTagName('tbody')[0];

    // Load users when the page loads
    loadUsers();

    // Add user form submission
    addUserForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const username = document.getElementById('username').value;
        addUser(username);
    });

    // Function to load users
    function loadUsers() {
        fetch('http://127.0.0.1:2270/users')
            .then(response => response.json())
            .then(users => {
                console.log(users);
                userTable.innerHTML = '';
                users.forEach(user => {
                    const row = userTable.insertRow();
                    row.innerHTML = `
                        <td>${user.id}</td>
                        <td>${user.name}</td>
                        <td>${user.status==1? 'Active':'Inactive'}</td>
                        <td><button class="delete-btn" onclick="inactivateUser(${user.id})">Inactive</button></td>
                    `;
                });
            });
    }

    // Function to add a user
    window.addUser = function(username, email) {
        fetch('http://127.0.0.1:2270/users', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username}),
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            loadUsers();
            addUserForm.reset();
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    }

    // Function to delete a user
    window.inactivateUser = function(id) {
        fetch(`http://127.0.0.1:2270/users/${id}/inactivate`, {
            method: 'PATCH',  // or 'PUT', depending on your API design
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('Success:', data);
            loadUsers();  // Reload the user list
        })
        .catch((error) => {
            console.error('Error:', error);
            alert('Failed to inactivate user. Please try again.');
        });
    }
});