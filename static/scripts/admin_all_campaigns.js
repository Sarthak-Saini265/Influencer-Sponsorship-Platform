let black_overlay = document.getElementsByClassName('black_overlay');
let black_overlay_flag = document.getElementsByClassName('black_overlay_flag');

for (let i = 0; i < black_overlay.length; i++) {
    black_overlay[i].addEventListener('click', function (event) {
        event.stopPropagation();
        counter = black_overlay[i].getAttribute('counter');
        let flag_btn = document.getElementsByClassName('flag_btn')[counter - 1];
        let ban_btn = document.getElementsByClassName('ban_btn')[counter - 1];
        let campaign_id = flag_btn.getAttribute('campaign_id');
        if (!flag_btn.contains(event.target) && !ban_btn.contains(event.target)) {
            window.location.href = `http://127.0.0.1:5000/campaign/${campaign_id}`;
        }
    })
}

for (let i = 0; i < black_overlay_flag.length; i++) {
    black_overlay_flag[i].addEventListener('click', function (event) {
        event.stopPropagation();
        counter = black_overlay_flag[i].getAttribute('counter');
        let flag_btn_flag = document.getElementsByClassName('flag_btn_flag')[counter - 1];
        let ban_btn = document.getElementsByClassName('ban_btn')[counter - 1];
        let campaign_id = flag_btn_flag.getAttribute('campaign_id');
        if (!flag_btn_flag.contains(event.target) && !ban_btn.contains(event.target)) {
            window.location.href = `http://127.0.0.1:5000/campaign/${campaign_id}`;
        }
    })
}


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
const ongoing_containers = document.querySelectorAll('.ended_campaign_div');

let imageIndex = 0;

for (let i = 0; i < containers.length; i++) {
    containers[i].style.backgroundImage = `linear-gradient(rgba(0, 0, 0, 0.15), rgba(0, 0, 0, 0.3)), url(${images[imageIndex]})`;
    imageIndex = (imageIndex + 1) % images.length;
}

imageIndex = 0;

for (let i = 0; i < ongoing_containers.length; i++) {
    ongoing_containers[i].style.backgroundImage = `linear-gradient(rgba(0, 0, 0, 0.15), rgba(0, 0, 0, 0.3)), url(${images2[imageIndex]})`;
    imageIndex = (imageIndex + 1) % images2.length;
}







