let black_overlay = document.getElementsByClassName('black_overlay');
let black_overlay_flag = document.getElementsByClassName('black_overlay_flag');
let black_overlay_sp = document.getElementsByClassName('black_overlay_sp');

for (let i = 0; i < black_overlay.length; i++) {
    black_overlay[i].addEventListener('click', function (event) {
        event.stopPropagation();
        counter = black_overlay[i].getAttribute('counter');
        let flag_btn = document.getElementsByClassName('flag_btn')[counter - 1];
        let ban_btn = document.getElementsByClassName('ban_btn')[counter - 1];
        let username = flag_btn.getAttribute('username');
        if (!flag_btn.contains(event.target) && !ban_btn.contains(event.target)) {
            window.location.href = `http://127.0.0.1:5000/influencer/${username}`;
        }
    })
}

for (let i = 0; i < black_overlay_sp.length; i++) {
    black_overlay_sp[i].addEventListener('click', function (event) {
        event.stopPropagation();
        counter = black_overlay_sp[i].getAttribute('counter');
        let flag_btn_sp = document.getElementsByClassName('flag_btn_sp')[counter - 1];
        let ban_btn = document.getElementsByClassName('ban_btn')[counter - 1];
        let username = flag_btn_sp.getAttribute('username');
        if (!flag_btn_sp.contains(event.target) && !ban_btn.contains(event.target)) {
            window.location.href = `http://127.0.0.1:5000/sponsor/${username}`;
        }
    })
}

for (let i = 0; i < black_overlay_flag.length; i++) {
    black_overlay_flag[i].addEventListener('click', function (event) {
        event.stopPropagation();
        counter = black_overlay_flag[i].getAttribute('counter');
        let flag_btn_flag = document.getElementsByClassName('flag_btn_flag')[counter - 1];
        let ban_btn_flag = document.getElementsByClassName('ban_btn_flag')[counter - 1];
        let username = flag_btn_flag.getAttribute('username');
        if (!flag_btn_flag.contains(event.target) && !ban_btn_flag.contains(event.target)) {
            window.location.href = `http://127.0.0.1:5000/influencer/${username}`;
        }
    })
}

let black_overlay_flag_sp = document.getElementsByClassName('black_overlay_flag_sp');
for (let i = 0; i < black_overlay_flag_sp.length; i++) {
    black_overlay_flag_sp[i].addEventListener('click', function (event) {
        event.stopPropagation();
        counter = black_overlay_flag_sp[i].getAttribute('counter');
        let flag_btn_flag_sp = document.getElementsByClassName('flag_btn_flag_sp')[counter - 1];
        let ban_btn_flag = document.getElementsByClassName('ban_btn_flag')[counter - 1];
        let username = flag_btn_flag_sp.getAttribute('username');
        if (!flag_btn_flag_sp.contains(event.target) && !ban_btn_flag.contains(event.target)) {
            window.location.href = `http://127.0.0.1:5000/sponsor/${username}`;
        }
    })
}

let black_overlay_ban = document.getElementsByClassName('black_overlay_ban');
for (let i = 0; i < black_overlay_ban.length; i++) {
    black_overlay_ban[i].addEventListener('click', function (event) {
        event.stopPropagation();
        counter = black_overlay_ban[i].getAttribute('counter');
        let flag_btn_ban = document.getElementsByClassName('flag_btn_ban')[counter - 1];
        let ban_btn_flag = document.getElementsByClassName('ban_btn_flag')[counter - 1];
        let username = flag_btn_ban.getAttribute('username');
        if (!flag_btn_ban.contains(event.target) && !ban_btn_flag.contains(event.target)) {
            window.location.href = `http://127.0.0.1:5000/influencer/${username}`;
        }
    })
}

let black_overlay_ban_sp = document.getElementsByClassName('black_overlay_ban_sp');
for (let i = 0; i < black_overlay_ban_sp.length; i++) {
    black_overlay_ban_sp[i].addEventListener('click', function (event) {
        event.stopPropagation();
        counter = black_overlay_ban_sp[i].getAttribute('counter');
        let flag_btn_ban_sp = document.getElementsByClassName('flag_btn_ban_sp')[counter - 1];
        let ban_btn_flag = document.getElementsByClassName('ban_btn_flag')[counter - 1];
        let username = flag_btn_ban_sp.getAttribute('username');
        if (!flag_btn_ban_sp.contains(event.target) && !ban_btn_flag.contains(event.target)) {
            window.location.href = `http://127.0.0.1:5000/sponsor/${username}`;
        }
    })
}











