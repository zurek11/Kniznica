const arg = process.argv.slice(2);
const fr = require('face-recognition');
const pathToDir = ('..\\..\\faceId\\' + arg.join("\\"));
const pathToJson = ('..\\..\\faceId\\model.json');
console.log(pathToDir);
const image = fr.loadImage(pathToDir);
const fs = require('fs');
const detector = fr.FaceDetector();
const recognizer = fr.FaceRecognizer();
const faceImage = detector.detectFaces(image);

if(faceImage.length > 0){
    fr.saveImage(pathToDir,faceImage[0]);
    if(arg.length > 1){
        const array = [faceImage[0]];
        if (fs.existsSync(pathToJson)) {
            var modelState = require(pathToJson);
            recognizer.load(modelState);
        }
        recognizer.addFaces(array, arg[0]);
        modelState = recognizer.serialize();
        fs.writeFileSync(pathToJson, JSON.stringify(modelState));
    }
}
else {
    console.log("Cannot detect face.");
}