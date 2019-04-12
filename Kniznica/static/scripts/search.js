$(document).on('click', '.panel-heading span.clickable', function(e){
    var $this = $(this);
	if(!$this.hasClass('panel-collapsed')) {
		$this.parents('.panel').find('.panel-body').slideUp();
		$this.addClass('panel-collapsed');
		$this.find('i').removeClass('glyphicon-chevron-up').addClass('glyphicon-chevron-down');
	} else {
		$this.parents('.panel').find('.panel-body').slideDown();
		$this.removeClass('panel-collapsed');
		$this.find('i').removeClass('glyphicon-chevron-down').addClass('glyphicon-chevron-up');
	}
});

$(function(){
    //BUTTONS
    var search_voice_button = $('#search_voice_button');
    var input_voice_field = $('#input_voice_field');
    var form = $('#search_form');

    var startDictation = function(e){
    	e.preventDefault();

        if (window.hasOwnProperty('webkitSpeechRecognition')) {
			var recognition = new webkitSpeechRecognition();

			recognition.continuous = false;
			recognition.interimResults = false;
			recognition.lang = "sk";
			recognition.start();
			search_voice_button.css('background', '#12459B');

			recognition.onresult = function(e) {
				var interim_transcript = '';
				var final_transcript = '';

				for (var i = event.resultIndex; i < event.results.length; ++i) {
					if (event.results[i].isFinal) {
						final_transcript += event.results[i][0].transcript;
					} else {
						interim_transcript += event.results[i][0].transcript;
					}
				}

				if(final_transcript){
					console.log(final_transcript);
					input_voice_field.val(final_transcript);
					form.submit();
				}
				recognition.stop();
				search_voice_button.css('background', '#062B69');
			};
			recognition.onerror = function() {
				recognition.stop();
				search_voice_button.css('background', '#062B69');
			}
		}
    };
    search_voice_button.on("click", startDictation);
});
