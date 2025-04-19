let currentUserId = null;
let socket = null;
let chattingWith = null;
let isLogin = false;

function toggleAuth() {
    isLogin = !isLogin;
    document.getElementById("authTitle").textContent = isLogin ? "Login" : "Register";
    document.getElementById("authBtn").textContent = isLogin ? "Login" : "Register";
}

async function auth() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    if (isLogin) {
        const formData = new URLSearchParams();
        formData.append("username", username);
        formData.append("password", password);

        const res = await fetch("http://localhost:8000/login", {
            method: "POST",
            headers: {"Content-Type": "application/x-www-form-urlencoded"},
            body: formData
        });

        if (res.ok) {
            const data = await res.json();
            currentUserId = data.user_id;
            document.querySelector(".auth").style.display = "none";
            document.querySelector(".users").style.display = "block";
            loadUsers();
        } else {
            alert("Login failed");
        }

    } else {
        const res = await fetch("http://localhost:8000/register", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({username, password})
        });

        if (res.ok) {
            const data = await res.json();
            currentUserId = data.id;
            document.querySelector(".auth").style.display = "none";
            document.querySelector(".users").style.display = "block";
            loadUsers();
        } else {
            alert("Username already taken");
        }
    }
}



async function loadUsers() {
    const res = await fetch("http://localhost:8000/users");
    const users = await res.json();

    const list = document.getElementById("userList");
    list.innerHTML = "";

    users.forEach(user => {
        if (user.id !== currentUserId) {
            const li = document.createElement("li");
            li.textContent = user.username;
            li.onclick = () => openChat(user);
            list.appendChild(li);
        }
    });
}

function openChat(user) {
    chattingWith = user.id;
    document.querySelector(".chat").style.display = "block";
    document.getElementById("chatWith").textContent = user.username;
    document.getElementById("messages").innerHTML = "";

    if (socket) {
        socket.close();
    }

    socket = new WebSocket(`ws://localhost:8000/ws/${currentUserId}/${chattingWith}`);

    socket.onmessage = (event) => {
        const msg = document.createElement("div");
        msg.className = "message";
        msg.textContent = event.data;
        document.getElementById("messages").appendChild(msg);
        document.getElementById("messages").scrollTop = document.getElementById("messages").scrollHeight;
    };

    socket.onclose = () => {
        console.log("WebSocket disconnected");
    };
}

function sendMessage() {
    const input = document.getElementById("messageInput");
    const message = input.value.trim();
    if (message && socket) {
        socket.send(message);
        input.value = "";
    }
}

