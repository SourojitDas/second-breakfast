const data = {};
function handleInput(e) {
    data[e.name] = e.value;
}
function submitData() {
    alert(JSON.stringify(data)); 
}

const signupData ={};
function handleSignupInput(e){
    signupData[e.name] = e.value;
}

function submitSignupData() {
    alert(JSON.stringify(signupData));
}