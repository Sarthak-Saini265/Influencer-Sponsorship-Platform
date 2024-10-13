const images = [
    'https://raw.githubusercontent.com/Sarthak-Saini265/image_storage/main/2d-graphic-colorful-wallpaper-with-grainy-gradients.jpg?raw=true',
    'https://raw.githubusercontent.com/Sarthak-Saini265/image_storage/main/background-gradient-lights.jpg?raw=true',
    'https://raw.githubusercontent.com/Sarthak-Saini265/image_storage/main/background_3.jpg?raw=true',
    'https://raw.githubusercontent.com/Sarthak-Saini265/image_storage/main/canyon_blur.jpg?raw=true',
    'https://raw.githubusercontent.com/Sarthak-Saini265/image_storage/main/background_4.jpg?raw=true',
    'https://raw.githubusercontent.com/Sarthak-Saini265/image_storage/main/background-gradient-lights.jpg?raw=true',
]

const containers = document.querySelectorAll('.trending_ad_div');

let imageIndex = 0;

for (let i = 0; i < containers.length; i++) {
    containers[i].style.backgroundImage = `linear-gradient(rgba(0, 0, 0, 0.15), rgba(0, 0, 0, 0.3)), url(${images[imageIndex]})`;
    imageIndex = (imageIndex + 1) % images.length;
}










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



document.querySelector('.become_sponsor').addEventListener('click', function (event) {
    event.preventDefault();

    if (confirm("You are about to be logged out. Do you want to continue?")) {
        window.location.href = '/logout?trigger_js_become_sponsor=True';
    }
});








