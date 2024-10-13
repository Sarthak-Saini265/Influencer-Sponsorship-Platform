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




function open_negot_window() {
    let negot_window = document.querySelector(".negot_window");
    if (negot_window.style.display == "flex") {
        negot_window.style.display = "none";
    }
    else{
        negot_window.style.display = "flex";
    }
}


document.addEventListener('click', function (event) {
    let negot_window = document.querySelector(".negot_window");
    let negotiate_div = document.querySelector(".negotiate_div");
    if (!negotiate_div.contains(event.target) && !negot_window.contains(event.target) && negot_window.style.display != 'none') {
        negot_window.style.display = 'none';
    }
});


function submit_negotiate_form() {
    let negotiate_form = document.querySelector(".negotiate_form");
    negotiate_form.submit();
}


function submit_accept_form(){
    let accept_form = document.querySelector(".accept_form");
    accept_form.submit();
}


function submit_reject_form(){
    let reject_form = document.querySelector(".reject_form");
    reject_form.submit();
}







