"use strict";


const randomSpace = function (elem, span) {
    let spaces = Math.floor(Math.random() * 3)
    let spaceString = " "
    elem.innerHTML = spaceString.repeat(spaces)
    setTimeout(() => {
        elem.innerHTML = ""
    }, 300);
};


window.addEventListener('load', () => {

    let body = document.querySelector("body");
    let allInputSpaceElem = document.getElementsByClassName('input-space');
    let timeDisplay = document.querySelector('.current-time');
    let changeViewElem = document.getElementsByClassName('change-background');
    let allClassesNames = [
        "matrix-simple",
        "white-black-text",
        "gray-theme",
        "orange-brown",
        "matrix-green",
    ]
    let classIndex = 0;

    setInterval(() => {
        let randomSeconds = Math.floor((Math.random() * 2) + 1)
        let randomEleNum = Math.floor(Math.random() * allInputSpaceElem.length)
        randomSpace(allInputSpaceElem[randomEleNum], randomSeconds)
    }, 400);


    setInterval(() => {
        let today = new Date();
        let time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
        console.log(time);
        timeDisplay.innerHTML = time;
    }, 1000);


    for (let index = 0; index < changeViewElem.length; index++) {

        const element = changeViewElem[index];
        element.addEventListener('click', () => {

            body.classList.remove("matrix-green")
            body.classList.remove(allClassesNames[classIndex - 1])
            body.classList.add(allClassesNames[classIndex]);

            if (classIndex < allClassesNames.length) {
                classIndex = classIndex + 1;
            } else {
                classIndex = 0;
            }
        
        });
    }
})
