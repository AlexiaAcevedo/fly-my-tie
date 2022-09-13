function favorite(element) {
    if (element.src == 'imgs/like-icon-black.png') {
        element.src = "imgs/like-icon.png"
    } else if (element.src == 'imgs/like-icon.png') {
        element.src = "imgs/like-icon-black.png"
    }
}

// function unfavorite(element) {
//     element.src = "flask_app/static/imgs/like-icon-black.png"
// }