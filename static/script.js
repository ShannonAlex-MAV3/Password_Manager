

// script for popup form to add new password deta
openpop = document.querySelector("#add-password")
closebtn = document.querySelector(".form-close-btn")
popup = document.querySelector(".form-pop")
formopen = document.querySelector(".form-open")

openpop.addEventListener("click", function(){
    popup.classList.add("form-active");
    formopen.classList.add("pop");
})

closebtn.addEventListener("click", function(){
    popup.classList.remove("form-active");
    formopen.classList.remove("pop");
})



// viewing and hiding the password 
eyes = document.querySelectorAll(".eyes")
passwords = document.querySelectorAll(".pass-field")

for (let i = 0; i < eyes.length; i++){
    eyes[i].addEventListener("click", function(){
        if(passwords[i].type === "password"){
            passwords[i].type = "text"
        }
        else{
            passwords[i].type = "password"
        }
    })
}



// script for popup menu
dot_icons = document.querySelectorAll(".field-menu")
editmenu_area = document.querySelectorAll(".editmenu-area")
editmenu = document.querySelectorAll(".editmenu")

for (let i = 0; i < dot_icons.length; i++){
    dot_icons[i].addEventListener("click", function(e){
        if(getComputedStyle(editmenu[i]).top === "-1000px"){
            
            editmenu_area[i].classList.add("editmenu-pop")
            editmenu[i].classList.add("editmenu-active")
            editmenu[i].style.top = e.y+"px"
            editmenu[i].style.left = e.x+10+"px"

        }
        
        
    })
    
    editmenu_area[i].addEventListener("click", function(){
        editmenu[i].style.top = '-1000px';
        editmenu[i].style.left = '1000px';
        editmenu_area[i].classList.remove("editmenu-pop")
        editmenu[i].classList.remove("editmenu-active")
    })

    
}

// script for popup form for editing existing password details
editbtn = document.querySelectorAll(".edit-btn")
editclosebtn = document.querySelectorAll(".editpass-open .form-pop .form-close-btn")
editpopup = document.querySelectorAll(".editpass-open .form-pop")
editform_open = document.querySelectorAll(".editpass-open")

for (let i = 0; i < editbtn.length; i++){
    editbtn[i].addEventListener("click", function(){
        editpopup[i].classList.add("form-active");
        editform_open[i].classList.add("pop");
    })
    
    editclosebtn[i].addEventListener("click", function(){
        editpopup[i].classList.remove("form-active");
        editform_open[i].classList.remove("pop");
    })
}


// alert fade
flashmsg = document.querySelector(".alert")
// set time for alert to wait in miliseconds
var time = 4000


if (flashmsg){
    setTimeout(function(){
        setInterval(function() {
            opacity = Number(getComputedStyle(flashmsg).opacity)
            if (opacity > 0){
                opacity = opacity - 0.1
                flashmsg.style.opacity = opacity
            }
        },20);
    },time);
}
