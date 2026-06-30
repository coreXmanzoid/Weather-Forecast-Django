/*=========================================================
                Navbar Scroll Effect
=========================================================*/

const navbar = document.querySelector(".custom-navbar");

window.addEventListener("scroll", () => {

    if (window.scrollY > 60) {

        navbar.style.background = "rgba(15,23,42,0.95)";
        navbar.style.padding = "10px 0";
        navbar.style.boxShadow = "0 10px 25px rgba(0,0,0,.15)";

    }

    else {

        navbar.style.background = "rgba(13,110,253,.25)";
        navbar.style.padding = "15px 0";
        navbar.style.boxShadow = "none";

    }

});


/*=========================================================
                Smooth Scrolling
=========================================================*/

document.querySelectorAll('a[href^="#"]').forEach(anchor => {

    anchor.addEventListener("click", function (e) {

        const target = document.querySelector(this.getAttribute("href"));

        if (!target) return;

        e.preventDefault();

        target.scrollIntoView({

            behavior: "smooth"

        });

    });

});


/*=========================================================
                Fade In Animation
=========================================================*/

const observer = new IntersectionObserver((entries) => {

    entries.forEach(entry => {

        if (entry.isIntersecting) {

            entry.target.classList.add("show");

        }

    });

}, {

    threshold: 0.15

});


document.querySelectorAll("section").forEach(section => {

    section.classList.add("hidden");

    observer.observe(section);

});


/*=========================================================
                Active Navbar Link
=========================================================*/

const sections = document.querySelectorAll("section");
const navLinks = document.querySelectorAll(".navbar-nav .nav-link");

window.addEventListener("scroll", () => {

    let current = "";

    sections.forEach(section => {

        const sectionTop = section.offsetTop - 120;
        const sectionHeight = section.clientHeight;

        if (pageYOffset >= sectionTop) {

            current = section.getAttribute("id");

        }

    });

    navLinks.forEach(link => {

        link.classList.remove("active");

        if (current && link.getAttribute("href") === "#" + current) {

            link.classList.add("active");

        }

    });

});


/*=========================================================
                Back To Top Button
=========================================================*/

const topButton = document.createElement("button");

topButton.innerHTML = '<i class="bi bi-arrow-up"></i>';

topButton.id = "backToTop";

document.body.appendChild(topButton);

topButton.style.display = "none";


window.addEventListener("scroll", () => {

    if (window.scrollY > 300) {

        topButton.style.display = "flex";

    }

    else {

        topButton.style.display = "none";

    }

});


topButton.addEventListener("click", () => {

    window.scrollTo({

        top: 0,
        behavior: "smooth"

    });

});


/*=========================================================
                Footer Copyright Year
=========================================================*/

const footerText = document.querySelector(".footer .text-center p");

if (footerText) {

    footerText.innerHTML =
        `© ${new Date().getFullYear()} Weather Forecast | Made with ❤️ using Django & OpenWeather API`;

}


/*=========================================================
                Page Loaded Animation
=========================================================*/

window.addEventListener("load", () => {

    document.body.classList.add("loaded");

});