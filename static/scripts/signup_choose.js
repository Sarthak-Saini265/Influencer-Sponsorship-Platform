let influencer_div = document.getElementsByClassName('influencer')[0];
let sponsor_div = document.getElementsByClassName('sponsor')[0];

let inf_form = document.getElementById('inf_form');
let sponsor_form = document.getElementById('sponsor_form');


influencer_div.addEventListener('click', function () {
    inf_form.submit()
})

sponsor_div.addEventListener('click', function () {
    sponsor_form.submit()
})

// influencer_div.addEventListener('mouseover', function () {
//     tick_left.style.display = 'block';
// })

// sponsor_div.addEventListener('mouseover', function () {
//     tick_right.style.display = 'block';
// })









