let dashboard = document.querySelector(".dashboard");
let content = document.querySelector(".content");
document.addEventListener('DOMContentLoaded', function () {
    content.style.height = `${(dashboard.clientHeight + 45)}px`;
});


const explore_div = document.getElementById("explore_div")
const explore_overlay = document.getElementsByClassName("explore_overlay")[0]
const explore_arrow = explore_div.querySelector(".explore_arrow");

console.log(explore_arrow);

explore_div.addEventListener("click", function () {
    if (explore_overlay.style.display == "none") {
        explore_overlay.style.display = "block";
        console.log(explore_overlay.style.display);
        explore_arrow.style.transform = "rotate(180deg)";
    } else {
        explore_overlay.style.display = "none";
        console.log(explore_overlay.style.display);
        explore_arrow.style.transform = "rotate(0deg)";
    }

});


document.addEventListener('click', function (event) {
    if (!explore_overlay.contains(event.target) && !explore_div.contains(event.target) && explore_overlay.style.display == 'block') {
        explore_overlay.style.display = 'none';
        explore_arrow.style.transform = 'rotate(0deg)';
    }
});

const explore_overlay_ul = explore_overlay.querySelector("ul");
const explore_overlay_li = explore_overlay_ul.querySelectorAll("li");

for (let i = 0; i < explore_overlay_li.length; i++) {
    explore_overlay_li[i].addEventListener("click", function () {
        window.location.href = "#";
    });
}


const profile_pic_div_nav = document.getElementsByClassName("profile_pic_div_nav")[0];
const profile_overlay = document.getElementsByClassName("profile_overlay")[0];

profile_pic_div_nav.addEventListener("click", function () {
    if (profile_overlay.style.display == "none") {
        profile_overlay.style.display = "block";
        console.log(profile_overlay.style.display);
    } else {
        profile_overlay.style.display = "none";
        console.log(profile_overlay.style.display);
    }

});

document.addEventListener('click', function (event) {
    if (!profile_overlay.contains(event.target) && !profile_pic_div_nav.contains(event.target) && profile_overlay.style.display == 'block') {
        profile_overlay.style.display = 'none';
    }
});



const images = [
    'https://raw.githubusercontent.com/Sarthak-Saini265/image_storage/main/background_3.jpg?raw=true',
    'https://raw.githubusercontent.com/Sarthak-Saini265/image_storage/main/2d-graphic-colorful-wallpaper-with-grainy-gradients.jpg?raw=true',
    'https://raw.githubusercontent.com/Sarthak-Saini265/image_storage/main/background_4.jpg?raw=true',
    'https://raw.githubusercontent.com/Sarthak-Saini265/image_storage/main/background-gradient-lights.jpg?raw=true',
];

let imageIndex = 0;

const containers = document.querySelectorAll('.campaign_div');

for (let i = 0; i < containers.length; i++) {
    containers[i].style.backgroundImage = `linear-gradient(rgba(0, 0, 0, 0.15), rgba(0, 0, 0, 0.3)), url(${images[imageIndex]})`;
    imageIndex = (imageIndex + 1) % images.length;
}


let contracts_btn = document.querySelector(".contracts_btn");
let dashboard_btn = document.querySelector(".dashboard_btn");
let all_charts_div = document.querySelector(".all_charts");
let sp_campaigns_div = document.querySelector(".sp_campaigns");
let dash_heading_div = document.querySelector(".dash_heading_contracts_section_btn");
let dash_heading_div_alternate = document.querySelector(".dash_heading_contracts_section_btn_alternate");
let negotiations_heading = document.querySelector(".negotiations_heading");
let negotiation_contracts_div = document.querySelector(".negotiation_contracts_div");

contracts_btn.addEventListener("click", function () {
    dash_heading_div.style.display = "none";
    dash_heading_div_alternate.style.display = "flex";
    negotiations_heading.style.display = "block";
    negotiation_contracts_div.style.display = "block";
    all_charts_div.style.display = "none";
    sp_campaigns_div.style.display = "none";
});

dashboard_btn.addEventListener("click", function () {
    dash_heading_div.style.display = "flex";
    dash_heading_div_alternate.style.display = "none";
    negotiations_heading.style.display = "none";
    negotiation_contracts_div.style.display = "none";
    all_charts_div.style.display = "block";
    sp_campaigns_div.style.display = "block";
});




document.querySelector('.become_sponsor').addEventListener('click', function (event) {
    event.preventDefault();

    if (confirm("You are about to be logged out. Do you want to continue?")) {
        window.location.href = '/logout?trigger_js_become_sponsor=True';
    }
});





// dashboard.style.height = `${(dashboard.clientHeight + 250)}px`;



function open_negot_window() {
    let negot_window = document.querySelector(".negot_window");
    if (negot_window.style.display == "flex") {
        negot_window.style.display = "none";
    }
    else {
        negot_window.style.display = "flex";
    }
}

let negotiate_div = document.querySelector(".negotiate_div");
if (negotiate_div) {
    document.addEventListener('click', function (event) {
        let negot_window = document.querySelector(".negot_window");
        let negotiate_div = document.querySelector(".negotiate_div");
        if (!negotiate_div.contains(event.target) && !negot_window.contains(event.target) && negot_window.style.display != 'none') {
            negot_window.style.display = 'none';
        }
    });
}














