const upload_overlay = document.getElementsByClassName('image_upload')[0];
const black_overlay = document.getElementsByClassName('black_overlay')[0];

function upload_overlay_trigger() {
    upload_overlay.style.display = "flex";
    black_overlay.style.display = "block";
}

black_overlay.addEventListener('click', function () {
    upload_overlay.style.display = "none";
    black_overlay.style.display = "none";
})

let img_upload_form = document.getElementById('img_url_form');
let profile_pic = document.querySelector('.profile_pic')
let input_url = document.getElementById('image_url')
let hidden_image_url = document.getElementById('hidden_image_url')
console.log(profile_pic.src)

function handleFormSubmit(event) {

    event.preventDefault();
    const imageUrl = document.getElementById("image_url").value;
    localStorage.setItem("imageUrl", imageUrl);
    profile_pic.src = imageUrl;
    upload_overlay.style.display = "none";
    black_overlay.style.display = "none";
    hidden_image_url.value = imageUrl;
    return false;
}

