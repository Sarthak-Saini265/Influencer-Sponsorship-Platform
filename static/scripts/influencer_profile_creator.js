document.addEventListener('DOMContentLoaded', () => {
    let add_niche_button = document.querySelector('.add_niche_button');
    const niche_all_divs = document.getElementsByClassName('niche_all_divs')[0];

    function add_niche_div() {
        const new_niche_div = document.createElement('div');
        new_niche_div.classList.add('new_niche_div');

        const new_niche_input = document.createElement('input');
        new_niche_input.type = 'text';
        new_niche_input.name = `niches[]`;
        new_niche_input.placeholder = `Enter a niche`;

        const new_add_button = document.createElement('button');
        new_add_button.type = 'button';
        new_add_button.textContent = '+';
        new_add_button.classList.add('add_niche_button');
        new_add_button.addEventListener('click', add_niche_div);

        new_niche_div.appendChild(new_niche_input);
        new_niche_div.appendChild(new_add_button);
        niche_all_divs.appendChild(new_niche_div);


        const old_add_button = new_niche_div.previousElementSibling.querySelector('.add_niche_button');
        if (old_add_button) {
            old_add_button.removeEventListener('click', add_niche_button);
            old_add_button.remove();
        }
    }

    add_niche_button = document.querySelector('.add_niche_button');
    add_niche_button.addEventListener('click', add_niche_div);
});



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









