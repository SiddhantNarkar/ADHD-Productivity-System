window.addEventListener('scroll', function () {
    const nav = document.getElementById('mainNavbar');
    const navLinks = document.querySelectorAll(".nav-link.hover-white");
    const loginBtn = document.querySelector(".nav-login-btn");

    if (window.scrollY > 50) {
        nav.style.background = "white";
        nav.style.boxShadow = "0 2px 10px rgba(0,0,0,0.1)";

        navLinks.forEach(link => link.style.color = "black");
        loginBtn.style.color = "black";
    } else {
        nav.style.background = "transparent";
        nav.style.boxShadow = "none";

        navLinks.forEach(link => link.style.color = "white");
        loginBtn.style.color = "white";
    }
});
