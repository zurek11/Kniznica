$(function(){

    //BLOCKS

    var login = document.getElementById("login");
    var register = document.getElementById("register");
    var news = document.getElementById("news");
    var books = document.getElementById("books");
    var games = document.getElementById("games");
    var fairytales = document.getElementById("fairytales");
    var songs = document.getElementById("songs");

    var voice_input = document.getElementById("voice_input");

    //SONGS

    var login_audio = new Audio('static\\source\\audio\\Prihlasenie.mp3');
    var register_audio = new Audio('static\\source\\audio\\Registracia.mp3');
    var news_audio = new Audio('static\\source\\audio\\Spravicky.mp3');
    var books_audio = new Audio('static\\source\\audio\\Knihy.mp3');
    var games_audio = new Audio('static\\source\\audio\\Hry.mp3');
    var fairytales_audio = new Audio('static\\source\\audio\\Rozpravky.mp3');
    var songs_audio = new Audio('static\\source\\audio\\Pesnicky.mp3');

    //BUTTONS

    var btn_on = document.getElementById("helpOn");
    var btn_off = document.getElementById("helpOff");
    var btn_voice = document.getElementById("btn_voice");

    //LISTENERS

    var loginPlayListener = function () {login_audio.play();};
    var registerPlayListener = function () {register_audio.play();};
    var newsPlayListener = function(){news_audio.play();};
    var booksPlayListener = function(){books_audio.play();};
    var gamesPlayListener = function(){games_audio.play();};
    var fairytalesPlayListener = function(){fairytales_audio.play();};
    var songsPlayListener = function(){songs_audio.play();};

    var loginStopListener = function () {
        login_audio.pause();
        login_audio.currentTime = 0;
    };

    var registerStopListener = function () {
        register_audio.pause();
        register_audio.currentTime = 0;
    };

    var newsStopListener = function(){
        news_audio.pause();
        news_audio.currentTime = 0;
    };

    var booksStopListener = function(){
        books_audio.pause();
        books_audio.currentTime = 0;
    };

    var gamesStopListener = function(){
        games_audio.pause();
        games_audio.currentTime = 0;
    };

    var fairytalesStopListener = function(){
        fairytales_audio.pause();
        fairytales_audio.currentTime = 0;
    };

    var songsStopListener = function(){
        songs_audio.pause();
        songs_audio.currentTime = 0;
    };

    var startDictation = function(){
        voice_input.value = 'Počúvam ...';
        if (window.hasOwnProperty('webkitSpeechRecognition')) {

          var recognition = new webkitSpeechRecognition();
          console.log(recognition.lang);
          recognition.continuous = false;
          recognition.interimResults = false;
          recognition.lang = "sk";
          recognition.start();

          recognition.onresult = function(e) {
            voice_input.value = e.results[0][0].transcript;
            if(e.results[0][0].transcript === 'prihlásenie'){
                window.location.href = '/detska-kniznica/login';
            }
            else if(e.results[0][0].transcript === 'registrácia'){
                window.location.href = '/detska-kniznica/register';
            }
            else {
                voice_input.value = 'Rozprávaj';
            }
            recognition.stop();
          };

          recognition.onerror = function() {
              voice_input.value = 'Rozprávaj';
              recognition.stop();
          }
        }
    };

    //CODE

    if(Cookies.get('help')===undefined){Cookies.set('help', 'on');}

    $('[data-toggle="tooltip"]').tooltip();
    $(".side-nav .collapse").on("hide.bs.collapse", function() {
        $(this).prev().find(".fa").eq(1).removeClass("fa-angle-right").addClass("fa-angle-down");
    });
    $('.side-nav .collapse').on("show.bs.collapse", function() {
        $(this).prev().find(".fa").eq(1).removeClass("fa-angle-down").addClass("fa-angle-right");
    });


    btn_voice.addEventListener("click", startDictation);

    btn_on.addEventListener("click", function(){
        Cookies.set('help', 'on');

        login.addEventListener("mouseenter", loginPlayListener);
        register.addEventListener("mouseenter", registerPlayListener);
        news.addEventListener("mouseenter", newsPlayListener);
        books.addEventListener("mouseenter", booksPlayListener);
        games.addEventListener("mouseenter", gamesPlayListener);
        fairytales.addEventListener("mouseenter", fairytalesPlayListener);
        songs.addEventListener("mouseenter", songsPlayListener);

        login.addEventListener("mouseout", loginStopListener);
        register.addEventListener("mouseout", registerStopListener);
        news.addEventListener("mouseout", newsStopListener);
        books.addEventListener("mouseout", booksStopListener);
        games.addEventListener("mouseout", gamesStopListener);
        fairytales.addEventListener("mouseout", fairytalesStopListener);
        songs.addEventListener("mouseout", songsStopListener);
    });

    btn_off.addEventListener("click", function(){
        Cookies.set('help', 'off');

        login.removeEventListener("mouseenter", loginPlayListener);
        register.removeEventListener("mouseenter", registerPlayListener);
        news.removeEventListener("mouseenter", newsPlayListener);
        books.removeEventListener("mouseenter", booksPlayListener);
        games.removeEventListener("mouseenter", gamesPlayListener);
        fairytales.removeEventListener("mouseenter", fairytalesPlayListener);
        songs.removeEventListener("mouseenter", songsPlayListener);

        login.removeEventListener("mouseout", loginStopListener);
        register.removeEventListener("mouseout", registerStopListener);
        news.removeEventListener("mouseout", newsStopListener);
        books.removeEventListener("mouseout", booksStopListener);
        games.removeEventListener("mouseout", gamesStopListener);
        fairytales.removeEventListener("mouseout", fairytalesStopListener);
        songs.removeEventListener("mouseout", songsStopListener);
    });
});