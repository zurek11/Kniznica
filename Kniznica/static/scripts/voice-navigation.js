$(function(){
    var sound_button = $('#sound');
    //ELEMENTS
    var login = document.getElementById("login");
    var register = document.getElementById("register");
    var news = document.getElementById("news");
    var books = document.getElementById("books");
    var games = document.getElementById("games");
    var fairytales = document.getElementById("fairytales");
    var songs = document.getElementById("songs");

    //VOICES
    var login_audio = new Audio('\\static\\source\\audio\\Prihlasenie.mp3');
    var register_audio = new Audio('\\static\\source\\audio\\Registracia.mp3');
    var news_audio = new Audio('\\static\\source\\audio\\Spravicky.mp3');
    var books_audio = new Audio('\\static\\source\\audio\\Knihy.mp3');
    var games_audio = new Audio('\\static\\source\\audio\\Hry.mp3');
    var fairytales_audio = new Audio('\\static\\source\\audio\\Rozpravky.mp3');
    var songs_audio = new Audio('\\static\\source\\audio\\Pesnicky.mp3');

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

    //CODE
    console.log(Cookies.get('help'));

    if(Cookies.get('help')==='off'){
        Cookies.set('help', 'off');
        sound_button.find('span').removeClass('glyphicon-volume-up');
        sound_button.find('span').addClass('glyphicon-volume-off');

        if(login){
         login.removeEventListener("mouseenter", loginPlayListener);
         login.removeEventListener("mouseout", loginStopListener);
        }
        if(register) {
         register.removeEventListener("mouseenter", registerPlayListener);
         register.removeEventListener("mouseout", registerStopListener);
        }
        news.removeEventListener("mouseenter", newsPlayListener);
        books.removeEventListener("mouseenter", booksPlayListener);
        games.removeEventListener("mouseenter", gamesPlayListener);
        fairytales.removeEventListener("mouseenter", fairytalesPlayListener);
        songs.removeEventListener("mouseenter", songsPlayListener);

        news.removeEventListener("mouseout", newsStopListener);
        books.removeEventListener("mouseout", booksStopListener);
        games.removeEventListener("mouseout", gamesStopListener);
        fairytales.removeEventListener("mouseout", fairytalesStopListener);
        songs.removeEventListener("mouseout", songsStopListener);
    }
    else{
        Cookies.set('help', 'on');
        sound_button.find('span').removeClass('glyphicon-volume-off');
        sound_button.find('span').addClass('glyphicon-volume-up');

        if(login){
            login.addEventListener("mouseenter", loginPlayListener);
            login.addEventListener("mouseout", loginStopListener);
        }
        if(register){
            register.addEventListener("mouseenter", registerPlayListener);
            register.addEventListener("mouseout", registerStopListener);
        }
        news.addEventListener("mouseenter", newsPlayListener);
        books.addEventListener("mouseenter", booksPlayListener);
        games.addEventListener("mouseenter", gamesPlayListener);
        fairytales.addEventListener("mouseenter", fairytalesPlayListener);
        songs.addEventListener("mouseenter", songsPlayListener);

        news.addEventListener("mouseout", newsStopListener);
        books.addEventListener("mouseout", booksStopListener);
        games.addEventListener("mouseout", gamesStopListener);
        fairytales.addEventListener("mouseout", fairytalesStopListener);
        songs.addEventListener("mouseout", songsStopListener);
    }

    sound_button.click(function(){
        if (Cookies.get('help')==='off') {
            $(this).find('span').removeClass('glyphicon-volume-off');
            $(this).find('span').addClass('glyphicon-volume-up');
            Cookies.set('help', 'on');

             if(login){
                login.addEventListener("mouseenter", loginPlayListener);
                login.addEventListener("mouseout", loginStopListener);
            }
            if(register){
                register.addEventListener("mouseenter", registerPlayListener);
                register.addEventListener("mouseout", registerStopListener);
            }
            news.addEventListener("mouseenter", newsPlayListener);
            books.addEventListener("mouseenter", booksPlayListener);
            games.addEventListener("mouseenter", gamesPlayListener);
            fairytales.addEventListener("mouseenter", fairytalesPlayListener);
            songs.addEventListener("mouseenter", songsPlayListener);

            news.addEventListener("mouseout", newsStopListener);
            books.addEventListener("mouseout", booksStopListener);
            games.addEventListener("mouseout", gamesStopListener);
            fairytales.addEventListener("mouseout", fairytalesStopListener);
            songs.addEventListener("mouseout", songsStopListener);
        }
        else{
            $(this).find('span').removeClass('glyphicon-volume-up');
            $(this).find('span').addClass('glyphicon-volume-off');
            Cookies.set('help', 'off');

            if(login){
                login.removeEventListener("mouseenter", loginPlayListener);
                login.removeEventListener("mouseout", loginStopListener);
            }
            if(register) {
                register.removeEventListener("mouseenter", registerPlayListener);
                register.removeEventListener("mouseout", registerStopListener);
            }
            news.removeEventListener("mouseenter", newsPlayListener);
            books.removeEventListener("mouseenter", booksPlayListener);
            games.removeEventListener("mouseenter", gamesPlayListener);
            fairytales.removeEventListener("mouseenter", fairytalesPlayListener);
            songs.removeEventListener("mouseenter", songsPlayListener);

            news.removeEventListener("mouseout", newsStopListener);
            books.removeEventListener("mouseout", booksStopListener);
            games.removeEventListener("mouseout", gamesStopListener);
            fairytales.removeEventListener("mouseout", fairytalesStopListener);
            songs.removeEventListener("mouseout", songsStopListener);
        }
    });
});
