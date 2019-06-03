const fr = require('face-recognition');
const recognizer = fr.FaceRecognizer();
const pathToJson = ('../../faceId/model.json');
const pathToImage = ('../../faceId/logged.png');
var recognized_image;
var min = 1;
var index;

recognized_image = fr.loadImage(pathToImage);
const modelState = require(pathToJson);
recognizer.load(modelState);

const predictions = recognizer.predict(recognized_image);
for(var j = 0; j < predictions.length; ++j){
    if(predictions[j].distance < min){
        min = predictions[j].distance;
        index = j;
    }
}

if(min <= 0.6)console.log(predictions[index]);
else console.log("no_logged");
