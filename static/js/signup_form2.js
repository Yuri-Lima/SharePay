function showPassword() {
    var password = document.getElementById('pwd');
    console.log('password', password)
    if (password.type === 'password') {
        password.type = "text";
    }
    else {
        password1.type = "password";
    }
}