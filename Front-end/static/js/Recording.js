//webkitURL is deprecated but nevertheless
URL = window.URL || window.webkitURL;

var gumStream; //stream from getUserMedia()
var recorder; //WebAudioRecorder object
var input; //MediaStreamAudioSourceNode  we'll be recording
var encodingType; //holds selected encoding for resulting audio (file)
var encodeAfterRecord = true; // when to encode

var success = document.getElementsByClassName("success");
var fails = document.getElementsByClassName("fail");
// shim for AudioContext when it's not avb.
var AudioContext = window.AudioContext || window.webkitAudioContext;
var audioContext; //new audio context to help us record

var encodingTypeSelect = document.getElementById("encodingTypeSelect");
var recordButton = document.getElementById("recordButton");
var stopButton = document.getElementById("stopButton");
var timer = document.getElementById("timer");
//add events to those 2 buttons
recordButton.addEventListener("click", startRecording);
stopButton.addEventListener("click", stopRecording);

function startRecording() {
  console.log("startRecording() called");

  /*
		Simple constraints object, for more advanced features see
		https://addpipe.com/blog/audio-constraints-getusermedia/
	*/

  var constraints = { audio: true, video: false };

  /*
    	We're using the standard promise based getUserMedia() 
    	https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia
	*/

  navigator.mediaDevices
    .getUserMedia(constraints)
    .then(function (stream) {
      /*
			create an audio context after getUserMedia is called
			sampleRate might change after getUserMedia is called, like it does on macOS when recording through AirPods
			the sampleRate defaults to the one set in your OS for your playback device

		*/
      audioContext = new AudioContext();

      //update the format
      // document.getElementById("formats").innerHTML =
      //   "Format: 2 channel " +
      //   encodingTypeSelect.options[encodingTypeSelect.selectedIndex].value +
      //   " @ " +
      //   audioContext.sampleRate / 1000 +
      //   "kHz";

      //assign to gumStream for later use
      gumStream = stream;

      /* use the stream */
      input = audioContext.createMediaStreamSource(stream);

      //stop the input from playing back through the speakers
      //input.connect(audioContext.destination)

      //get the encoding
      encodingType =
        encodingTypeSelect.options[encodingTypeSelect.selectedIndex].value;

      //disable the encoding selector
      encodingTypeSelect.disabled = true;

      recorder = new WebAudioRecorder(input, {
        workerDir: "static/js/", // must end with slash
        encoding: encodingType,
        numChannels: 2, //2 is the default, mp3 encoding supports only 2
        onEncoderLoading: function (recorder, encoding) {
          // show "loading encoder..." display
        },
        onEncoderLoaded: function (recorder, encoding) {
          // hide "loading encoder..." display
        },
      });

      recorder.onComplete = function (recorder, blob) {
        createDownloadLink(blob, recorder.encoding);
        encodingTypeSelect.disabled = false;
      };

      recorder.setOptions({
        timeLimit: 120,
        encodeAfterRecord: encodeAfterRecord,
        ogg: { quality: 0.5 },
        mp3: { bitRate: 160 },
      });

      //start the recording process
      recorder.startRecording();
    })
    .catch(function (err) {
      //enable the record button if getUSerMedia() fails
      recordButton.disabled = false;
      stopButton.disabled = true;
      console.log(err);
    });

  //disable the record button
  recordButton.disabled = true;
  stopButton.disabled = false;
}

function stopRecording() {
  console.log("stopRecording() called");

  //stop microphone access
  gumStream.getAudioTracks()[0].stop();

  //disable the stop button
  stopButton.disabled = true;
  recordButton.disabled = false;

  //tell the recorder to finish the recording (stop recording + encode the recorded audio)
  recorder.finishRecording();
}

async function createDownloadLink(blob, encoding) {
  var url = URL.createObjectURL(blob);
  let file = new File([blob], "file.wav");
  console.log(file);
  const formData = new FormData();

  var h = document.getElementById("result");
  formData.append("file", file);

  await axios
    .post("/predict", formData)
    .then(async (res) => {
      //await location.reload(true);
      location.reload(true);
      console.log(res.data, res.statusText);
      //h.innerHTML = res.data;

      //var img = document.createElement("img");
      //img.src = "static/images/spectro.png";
      //document.getElementById("chartContainer").appendChild(img);
      if (res.data == 0 || res.statusText == "other") {
        document.getElementById("success").style.display = "none";
        document.getElementById("fail").style.display = "block";
      } else {
        document.getElementById("success").style.display = "block";
        document.getElementById("fail").style.display = "none";
      }
    })
    .catch((e) => {
      console.log(e);
    });
  var au = document.createElement("audio");
  var li = document.createElement("li");
  var link = document.createElement("a");

  //add controls to the <audio> element
  au.controls = true;
  au.src = url;

  //link the a element to the blob
  link.href = url;
  link.download = new Date().toISOString() + "." + encoding;
  link.innerHTML = link.download;

  //add the new audio and a elements to the li element
  li.appendChild(au);
  li.appendChild(link);

  //add the li element to the ordered list
  recordingsList.appendChild(li);
}

// let timerId;

// recordButton.addEventListener('click', function() {
// 	setInterval(function() {
// 		let date = new Date;
// 		console.log(date.getMinutes() + ' ' + date.getSeconds());
// 	}, 1000);
// });

// stopButton.addEventListener('click', function() {
// 	clearInterval(timerId);
// });

(i = 0), (a = 0);
var min = 0;
recordButton.onclick = () => {
  if (a == 0) {
    a = a + 1;
    sec = setInterval(start, 60);
    function start() {
      timer.innerHTML = "0" + min + " : " + i;
      i++;
      if (i == 60) {
        min++;
        i = 0;
      }
    }
  }
};

stopButton.onclick = () => {
  clearInterval(sec);
  i = 0;
  a = 0;
  min = 0;

  timer.innerHTML = "00 : " + 00;
};
