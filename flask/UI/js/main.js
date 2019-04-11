const data = {};
function handleInput(e) {
    data[e.name] = e.value;
}
function submitData() {
    alert(JSON.stringify(data));
    //console.log("redirect");
}

const signupData ={};
function handleSignupInput(e){
    signupData[e.name] = e.value;
}

function submitSignupData() {
    localStorage.setItem('username', signupData.name);
    /* fetch('http://127.0.0.1:5000/second-breakfast/show-recipe/')
        .then(function (response) {
            return response.json();
        })
        .then(function (myJson) {
            localStorage.setItem('imageDataKey', JSON.stringify(myJson));
        }); */
    window.location.href = "file:///C:/Raaz(D)/Trinity/AA/second-breakfast/flask/UI/preferences.html";

}
