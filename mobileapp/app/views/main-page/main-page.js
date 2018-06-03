var observable = require("data/observable");
var observableArray = require("data/observable-array");
var facultyDropDown = new observableArray.ObservableArray('Select a Faculty');
var semesterDropDown = new observableArray.ObservableArray('Select a Semester');
var subjectDropDown = new observableArray.ObservableArray('Select a Subject');
var topicDropDown = new observableArray.ObservableArray('Select a Topic');
var facultyList = ["Anand Sir","Annapoorna ma'am","Basha sir"]
var semesterList = ["1st Semester","2nd Semester", "3rd Semester", "4th Semester"]
var subjectList = ["Algorithms", "Operating systems", "Networks","Physics"]
var topicList = ["Newton's Laws","Kepler's Laws", "Inheritance", "Polymorphism","Abstraction"]
// var Toast = require("nativescript-toast");


var facultySelectedIndex = 0
var semesterSelectedIndex = 0
var subjectSelectedIndex = 0
var topicSelectedIndex = 0
var httpModule = require("http");

var stopRecord = false;
var recordText = "";
const audio = require('nativescript-audio');
var SpeechRecognitionTranscription =  require("nativescript-speech-recognition").SpeechRecognitionTranscription;

var SpeechRecognition = require("nativescript-speech-recognition").SpeechRecognition;
var speechRecognition = new SpeechRecognition();

exports.onPageLoaded = function(args) {
  var page = args.object;
  console.log("Hello World");
  viewModel = new observable.Observable();
  while (facultyDropDown.length > 1)
          facultyDropDown.pop();
  while (semesterDropDown.length > 1)
          semesterDropDown.pop();
  while (subjectDropDown.length > 1)
          subjectDropDown.pop();
  while (topicDropDown.length > 1)
          topicDropDown.pop();
  for(i=0;i<facultyList.length;i++)
  {
  	facultyDropDown.push(facultyList[i])
  }

  for(i=0;i<semesterList.length;i++)
  {
  	semesterDropDown.push(semesterList[i])
  }

  for(i=0;i<subjectList.length;i++)
  {
  	subjectDropDown.push(subjectList[i])
  }

  for(i=0;i<topicList.length;i++)
  {
  	topicDropDown.push(topicList[i])
  }

  viewModel.set("facultyDropDown", facultyDropDown);
  viewModel.set("semesterDropDown", semesterDropDown);
  viewModel.set("subjectDropDown", subjectDropDown);
  viewModel.set("topicDropDown", topicDropDown);
  viewModel.set("selectedFaculty", 0);
  viewModel.set("selectedSemester", 0);
  viewModel.set("selectedSubject", 0);
  viewModel.set("selectedTopic", 0);
  page.bindingContext = viewModel;
};

function onPlay(args) {
	stopRecord = false;
	var temp = args;
	recordText = "";
  // var toast = Toast.makeText("Recording started");
 //  toast.show();
	// console.log("Play")

	speechRecognition.available().then(
     function(available) {
    console.log(available ? "YES!" : "NO");
      }
    );
    speechRecognition.startListening({locale:"en-US", returnPartialResults: false, 
    	onResult: function(transcription) {console.log(transcription.text); recordText = recordText + transcription.text},
    	onBufferReceived: function(buffer) {console.log("onEndOfSpeech")}}).then({ function(started) {
    	console.log("audio"), function(errorMessage) {
    		console.log("error when starting")
    	}
    	}
    }
    );


    // speechRecognition.stopListening().then(function() {
    // 	console.log("stopped")
    // 	if(stopRecord != true)
    // 	{ 
    // 		console.log("ten")
    // 	speechRecognition.startListening({locale:"en-US", returnPartialResults: false, 
    // 	onResult: function(transcription) {console.log(transcription.text)}}).then(function(started) {
    // 	console.log("hi")
    // 	console.log(started)
    // 	console.log("audio")
    // 	}
    // ).then(function(error){
    // 	console.log(error)
    // 	console.log("e")
    // });
    // 	}

    // }).then(function(e){
    // 	console.log("eleven")
    // })
}

exports.dropDownSelectedIndexChangedFaculty = function(args){
	facultySelectedIndex = args.newIndex
}

exports.dropDownSelectedIndexChangedSemester = function(args){
	semesterSelectedIndex = args.newIndex
}

exports.dropDownSelectedIndexChangedSubject = function(args){
	subjectSelectedIndex = args.newIndex
}

exports.dropDownSelectedIndexChangedTopic = function(args){
	topicSelectedIndex = args.newIndex
}

exports.onPause = function(args) {
	console.log("Pause")
}

exports.onStop = function(args) {
	console.log("Stop")
	stopRecord = true;
}

exports.onSubmit = function(args) {
	var context;
	context = JSON.stringify({"faculty": facultyList[facultySelectedIndex-1],
		"semester": semesterList[semesterSelectedIndex-1],
		"subject" : subjectList[subjectSelectedIndex-1],
		"topic" : topicList[topicSelectedIndex-1],
		"session": recordText});
	// console.log(subjectDropDown)
	console.log(context)

	httpModule.request({
		url:"http://192.168.43.167:8000/session",
		method:"POST",
		headers: {"Content-Type": "application/json" },
		content: context,
		// body: context,
	}).then(function(response){
		const result = response.content.toJSON();
		console.log("1ma")
		console.log(result);
},function(e) {
  console.log(e)
});
  console.log("Hello")
	console.log(facultySelectedIndex)

	console.log(recordText)
}

exports.onPlay = onPlay;