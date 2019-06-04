$(function() {
    var canvas = document.getElementById('canvas');
    var context = canvas.getContext('2d');
    var video = document.getElementById('video');
    var counter = document.getElementById('counter');
    var snap = document.getElementById('snap');
    var save = document.getElementById('save');
    var numOfPhotos = 5;
    var base64imgs = [];
    counter.innerText = numOfPhotos.toString();

    snap.addEventListener("click", function() {
        console.error("snap");
        context.drawImage(video, 0, 0, 640, 480);
        base64imgs.push(canvas.toDataURL());
        numOfPhotos--;
        counter.innerText = numOfPhotos.toString();
        if(numOfPhotos <= 0){
            video.hidden = true;
            counter.style.display = 'none';
            snap.hidden = true;
            document.getElementById('id_pic1').value = base64imgs[0];
            document.getElementById('id_pic2').value = base64imgs[1];
            document.getElementById('id_pic3').value = base64imgs[2];
            document.getElementById('id_pic4').value = base64imgs[3];
            document.getElementById('id_pic5').value = base64imgs[4];
            save.hidden = false;
        }
    });

    if(navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({ video: true }).then(function(stream) {
            try {
              video.srcObject = stream;
            }
            catch (error) {
              video.src = window.URL.createObjectURL(stream);
            }
            video.play();
        });
    }
});