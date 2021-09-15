let offers = document.getElementsByClassName('offer')

function onClickRow(event) {
    let target = event.target.parentNode
    console.log(event)
    console.log(event.target)
    let id = target.getElementsByClassName('offer-id')[0]
    let server = target.getElementsByClassName('offer-server')[0]
    let username = target.getElementsByClassName('offer-username')[0]
    let price = target.getElementsByClassName('offer-price')[0]
    let quantity = target.getElementsByClassName('offer-quantity')[0]
    let date = target.getElementsByClassName('offer-date')[0]

}

Array.from(offers).forEach((offer) => {
    offer.addEventListener('click', onClickRow);
});