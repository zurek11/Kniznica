$(function() {
    var canvas = document.getElementById('canvas');
    var context = canvas.getContext('2d');
    var btn_camera = document.getElementById('btn_camera');
    var video = document.getElementById('video');
    var btn_login_camera = document.getElementById('btn_login_camera');
    var loading = document.getElementById('loading');
    var div_video = document.getElementById('div_video');
    var menu_login_camera = document.getElementById('menu_login_camera');
    var loaders = document.getElementsByClassName('loader');
    var loader = loaders[0];
    var base64img;

    btn_camera.addEventListener("click", function() {
        document.getElementById('name').hidden = true;
        document.getElementById('password').hidden = true;
        document.getElementById('menu_camera').hidden = true;
        document.getElementById('menu_login').hidden = true;
        document.getElementById('main-img').hidden = true;
        div_video.style.display = 'block';
        menu_login_camera.style.display = 'block';
    });

    btn_login_camera.addEventListener("click", function() {
        context.drawImage(video, 0, 0, 640, 480);
        base64img = canvas.toDataURL();
        document.getElementById('id_pic1').value = base64img;
        menu_login_camera.style.display = 'none';
        div_video.style.display = 'none';
        loading.style.display = 'block';
        loader.style.display = 'block';
    });

    if(navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({ video: true }).then(function(stream) {
            try {
              video.srcObject = stream;
            } catch (error) {
              video.src = window.URL.createObjectURL(stream);
            }
            video.play();
        });
    }
});