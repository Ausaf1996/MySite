// Function to toggle the chatbox's visibility
let userId = null;

function formatTime() {
    const now = new Date();
    return now.getHours().toString().padStart(2, '0') + ':' + 
           now.getMinutes().toString().padStart(2, '0') + ':' + 
           now.getSeconds().toString().padStart(2, '0');
}


// Function to get or set the session ID
function getSessionId() {
    fetch('/get-session-id')
    .then(response => response.json())
    .then(data => {
        userId = data.user_id;
    })
    .catch(error => console.error('Error:', error));
}

getSessionId();


function toggleChatbox() {
    var chatbox = document.getElementById("chatbox");
    if (chatbox.style.display === "none" || !chatbox.style.display) {
        chatbox.style.display = "block";
    } else {
        chatbox.style.display = "none";
    }
}


// Updated sendMessage function
function sendMessage() {
    var message = document.getElementById('message-input').value;
    if (message) {
        displayMessage('You: ' + message + ' (' + formatTime() + ')'); // Display user's message with time
        sendMessageToServer(message);
        document.getElementById('message-input').value = ''; // Clear the input field
    }
}


// Function to send the user's message to the server
function sendMessageToServer(message) {
    fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: message, user_id: userId })
    })
    .then(response => response.json())
    .then(data => {
        displayResponse(data.response); // Display the server's response
    })
    .catch(error => {
        console.error('Error:', error);
        displayResponse("Error: Unable to send message."); // Display error message
    });
}

// Function to display a message in the chatbox
function displayMessage(message) {
    var chatboxContent = document.getElementById("chatbox-content");
    if (chatboxContent) {
        chatboxContent.innerHTML += "<p>" + message + "</p>";
        chatboxContent.scrollTop = chatboxContent.scrollHeight; // Scroll to the bottom
    }
}


/* This is for Testemonials */

document.addEventListener("DOMContentLoaded", function() {
    let testimonials = document.querySelectorAll('.testimonial');
    let currentTestimonial = 0;

    function showNextTestimonial() {
        testimonials[currentTestimonial].style.display = 'none';
        currentTestimonial = (currentTestimonial + 1) % testimonials.length;
        testimonials[currentTestimonial].style.display = 'block';
    }

    setInterval(showNextTestimonial, 10000); // Change testimonial every 10000 ms (10 seconds)
    testimonials[currentTestimonial].style.display = 'block'; // Show the first testimonial
});


function displayResponse(message) {
    displayMessage('Server: ' + message + ' (' + formatTime() + ')'); // Include time in the server response
}

document.getElementById('message-input').addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        event.preventDefault(); // Prevent the default action to avoid form submission/refresh
        sendMessage();
    }
});



// Code to hide the chatbox when clicking outside of it
document.addEventListener('click', function(event) {
    var chatbox = document.getElementById("chatbox");
    var chatIcon = document.querySelector('.chatbot-icon');

    if (chatbox.style.display === "block" && !chatbox.contains(event.target) && !chatIcon.contains(event.target)) {
        chatbox.style.display = "none";
    }
});
