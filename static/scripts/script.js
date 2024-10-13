const images = [
    'https://raw.githubusercontent.com/Sarthak-Saini265/image_storage/main/background_3.jpg?raw=true',
    'https://raw.githubusercontent.com/Sarthak-Saini265/image_storage/main/2d-graphic-colorful-wallpaper-with-grainy-gradients.jpg?raw=true',
    'https://raw.githubusercontent.com/Sarthak-Saini265/image_storage/main/background_4.jpg?raw=true',
    'https://raw.githubusercontent.com/Sarthak-Saini265/image_storage/main/background-gradient-lights.jpg?raw=true',
];

const images2 = [
    'https://raw.githubusercontent.com/Sarthak-Saini265/image_storage/main/2d-graphic-colorful-wallpaper-with-grainy-gradients.jpg?raw=true',
    'https://raw.githubusercontent.com/Sarthak-Saini265/image_storage/main/background-7-blur.jpg?raw=true',
    'https://raw.githubusercontent.com/Sarthak-Saini265/image_storage/main/background-gradient-lights.jpg?raw=true',
    'https://raw.githubusercontent.com/Sarthak-Saini265/image_storage/main/background_3.jpg?raw=true',
    'https://raw.githubusercontent.com/Sarthak-Saini265/image_storage/main/canyon_blur.jpg?raw=true',
    'https://raw.githubusercontent.com/Sarthak-Saini265/image_storage/main/background_4.jpg?raw=true',
]

const containers = document.querySelectorAll('.ongoing_campaign_div');
const ad_containers = document.querySelectorAll('.trending_ad_div');

let imageIndex = 0;

for (let i = 0; i < containers.length; i++) {
    containers[i].style.backgroundImage = `linear-gradient(rgba(0, 0, 0, 0.15), rgba(0, 0, 0, 0.3)), url(${images[imageIndex]})`;
    imageIndex = (imageIndex + 1) % images.length;
}

imageIndex = 0;

for (let i = 0; i < ad_containers.length; i++) {
    ad_containers[i].style.backgroundImage = `linear-gradient(rgba(0, 0, 0, 0.15), rgba(0, 0, 0, 0.3)), url(${images2[imageIndex]})`;
    imageIndex = (imageIndex + 1) % images2.length;
}







// document.addEventListener("DOMContentLoaded", function() {
//     const toggleSwitch = document.getElementById("toggle-switch");
//     const previewDiv = document.querySelector(".preview");

//     toggleSwitch.addEventListener("change", function() {
//         if (toggleSwitch.checked) {
//             previewDiv.style.display = "flex";
//         } else {
//             previewDiv.style.display = "none";
//         }
//     });
// });


divs = document.getElementsByClassName("ongoing_campaign_div");

// function previewfill(event){
//     let dummy = document.querySelector(".dummy_text");
//     let heading = document.querySelector(".overlay_heading");
//     let description = document.querySelector(".overlay_description");
//     let end_date = document.querySelector(".overlay_end_date");
//     let company = document.querySelector(".overlay_company");


//     dummy.innerHTML = '';
//     let list = event.currentTarget.getAttribute('info').split(',');
//     heading.innerHTML = list[0];
//     description.innerHTML = list[1];
//     end_date.innerHTML = 'Ends on: <span>' + list[2] + '</span>';
//     company.innerHTML = 'by: <span>' + list[3] + '</span>';
// }


// for (let i = 0; i < divs.length; i++) {
//     divs[i].addEventListener('click', previewfill);
// }


function div_link(event) {
    let id = event.currentTarget.getAttribute('campaign_id');
    window.location.href = `http://127.0.0.1:5000/campaign/${id}`;
}

for (let i = 0; i < divs.length; i++) {
    divs[i].addEventListener('click', div_link);
}




function give_url(event) {
    let username = event.currentTarget.getAttribute('username');
    window.location.href = `http://127.0.0.1:5000/influencer/${username}`
}

let image_container = document.querySelectorAll('.infl_image');

for (let i = 0; i < image_container.length; i++) {
    image_container[i].addEventListener('click', give_url)
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


