niche_images = [
    'https://fiverr-res.cloudinary.com/q_auto,f_auto,w_255,dpr_2.0/v1/attachments/generic_asset/asset/7ead3b2056987e6fa3aad69cf897a50b-1690383161247/ai-artists-2x.png',
    'https://fiverr-res.cloudinary.com/q_auto,f_auto,w_255,dpr_2.0/v1/attachments/generic_asset/asset/7ead3b2056987e6fa3aad69cf897a50b-1690383161257/logo-design-2x.png',
    'https://fiverr-res.cloudinary.com/q_auto,f_auto,w_255,dpr_2.0/v1/attachments/generic_asset/asset/7ead3b2056987e6fa3aad69cf897a50b-1690383161257/wordpress-2x.png',
    'https://fiverr-res.cloudinary.com/q_auto,f_auto,w_550,dpr_1.0/v1/attachments/generic_asset/asset/7ead3b2056987e6fa3aad69cf897a50b-1690383161253/voice-over-2x.png',
    'https://fiverr-res.cloudinary.com/q_auto,f_auto,w_550,dpr_1.0/v1/attachments/generic_asset/asset/7ead3b2056987e6fa3aad69cf897a50b-1690383161245/animated-explainer-2x.png',
    'https://fiverr-res.cloudinary.com/q_auto,f_auto,w_550,dpr_1.0/v1/attachments/generic_asset/asset/7ead3b2056987e6fa3aad69cf897a50b-1690383161249/social-2x.png',
    'https://fiverr-res.cloudinary.com/q_auto,f_auto,w_550,dpr_1.0/v1/attachments/generic_asset/asset/27f914ed7984fdd2d55aa1fb5e74bd6a-1690384243592/seo-2x.png',
    'https://fiverr-res.cloudinary.com/q_auto,f_auto,w_550,dpr_1.0/v1/attachments/generic_asset/asset/7ead3b2056987e6fa3aad69cf897a50b-1690383161236/illustration-2x.png',
    'https://fiverr-res.cloudinary.com/q_auto,f_auto,w_550,dpr_1.0/v1/attachments/generic_asset/asset/7ead3b2056987e6fa3aad69cf897a50b-1690383161247/translation-2x.png',
    'https://fiverr-res.cloudinary.com/q_auto,f_auto,w_550,dpr_1.0/v1/attachments/generic_asset/asset/7ead3b2056987e6fa3aad69cf897a50b-1690383161248/data-entry-2x.png',
    'https://fiverr-res.cloudinary.com/q_auto,f_auto,w_550,dpr_1.0/v1/attachments/generic_asset/asset/7ead3b2056987e6fa3aad69cf897a50b-1690383161238/book-covers-2x.png',
]

const niche_containers = document.querySelectorAll('.niche_div');

let imageIndex = 0;

for (let i = 0; i < niche_containers.length; i++) {
    niche_containers[i].style.backgroundImage = `linear-gradient(rgba(0, 0, 0, 0), rgba(0, 0, 0, 0.3)), url(${niche_images[imageIndex]})`;
    imageIndex = (imageIndex + 1) % niche_images.length;
}


function div_link(event) {
    niche_url = event.currentTarget.getAttribute('niche');
    window.location.href = `http://127.0.0.1:5000/niche/${niche_url.toLowerCase()}`
}

for (let i = 0; i < niche_containers.length; i++) {
    niche_containers[i].addEventListener('click', div_link);
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










