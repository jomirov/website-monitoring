document.getElementById("logout-btn").addEventListener("click", ()=> {
    localStorage.removeItem("access_token");
    window.location.href = "login.html";
})

async function verify_user() {
    response = await fetch("http://localhost:8000/users/me", {
        headers: {"Authorization": `Bearer ${localStorage.getItem("access_token")}`}
    });
    if (response.status == 401) {
        window.location.href = "login.html";
    }
    res = await response.json()
    localStorage.setItem("useremail", res.email);
}