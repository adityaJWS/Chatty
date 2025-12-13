// service.js
// const API_BASE_URL = 'http://127.0.0.1:5000';
const API_BASE_URL = 'https://7rh124s2-5000.inc1.devtunnels.ms'

const ChatService = {
    /**
     * Authenticates a user against the /login endpoint.
     * @param {string} username
     * @param {string} emailId
     * @param {number} password
     * @returns {Promise<object>} response data
     */
    login: async function(username, emailId, password) {
        const response = await fetch(`${API_BASE_URL}/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                'username': username,
                'email-id': emailId,
                'password': password
            })
        });
        return response.json();
    },

    /**
     * Fetches all messages from the /get_messages endpoint.
     * @returns {Promise<Array<object>>} An array of message objects.
     */
    fetchMessages: async function() {
        // This hits the /get_messages endpoint
        const response = await fetch(`${API_BASE_URL}/get_messages`);
        if (!response.ok) {
            throw new Error('Failed to fetch messages');
        }
        // Flask returns the array of messages directly
        return response.json();
    },

    /**
     * Sends a new message to the /send_message endpoint via POST request.
     * @param {string} messageText
     * @returns {Promise<object>} response data including the new record
     */
    sendMessageToServer: async function(messageText) {
        // This hits the /send_message endpoint
        const response = await fetch(`${API_BASE_URL}/send_message`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: messageText })
        });
        
        if (!response.ok) {
            throw new Error('Failed to send message');
        }
        return response.json();
    }
};
