$(function(){
    //BUTTONS
    var voice_button = document.getElementById("voice");

    var startDictation = function(){
        if (window.hasOwnProperty('webkitSpeechRecognition')) {

          var recognition = new webkitSpeechRecognition();
          console.log(recognition.lang);

          recognition.continuous = false;
          recognition.interimResults = false;
          recognition.lang = "sk";
          recognition.start();
          voice_button.style.background = '#12459B';

          recognition.onresult = function(e) {
            if(e.results[0][0].transcript === 'prihlásenie'){
                window.location.href = '/detska-kniznica/login';
            }
            else if(e.results[0][0].transcript === 'registrácia'){
                window.location.href = '/detska-kniznica/register';
            }
            else if(e.results[0][0].transcript === 'domov'){
                window.location.href = '/detska-kniznica';
            }
            else if(e.results[0][0].transcript === 'správičky'){
                window.location.href = '/detska-kniznica';
            }
            else if(e.results[0][0].transcript === 'knihy'){
                window.location.href = '/detska-kniznica/books';
            }
            else if(e.results[0][0].transcript === 'hry'){
                window.location.href = '/detska-kniznica/games';
            }
            else if(e.results[0][0].transcript === 'rozprávky'){
                window.location.href = '/detska-kniznica/videos';
            }
            else if(e.results[0][0].transcript === 'pesničky'){
                window.location.href = '/detska-kniznica/songs';
            }
            recognition.stop();
            voice_button.style.background = '#062B69';
          };
          recognition.onerror = function() {
              recognition.stop();
              voice_button.style.background = '#062B69';
          }
        }
    };
    voice_button.addEventListener("click", startDictation);
});
