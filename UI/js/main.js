const data = {};
function handleInput(e) {
    data[e.name] = e.value;
}
function submitData() {
    alert(JSON.stringify(data));
    //console.log("redirect");
    window.location = "C:/Raaz(D)/Trinity/AA/second-breakfast/UI/preferences.html";
}

const signupData ={};
function handleSignupInput(e){
    signupData[e.name] = e.value;
}

function submitSignupData() {
    /*fetch('http://127.0.0.1:5000/second-breakfast/show-recipe/')
    .then(response => response.text())
    .then(data => console.log(data))*/
    //alert(JSON.stringify(signupData));
}
