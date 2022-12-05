jQuery(document).ready(function () {
    var $ = jQuery;
    // myrevord -> custom var that hold some methods wa are going to use it to start and stop recording
    var myRecorder = {
      objects: {
        context: null,
        stream: null,
        recorder: null,
      },
      // called each time the record button is pressed
      init: function () {
        // check if the context is initialized or not 
        if (null === myRecorder.objects.context) {
          // if the context is not initialized -> initialize it (context or webkit depending on the browser)
          myRecorder.objects.context = new (window.AudioContext ||
            window.webkitAudioContext)();
        }
      },
      start: function () {
        // options -> allow mic and denied camera
        var options = { audio: true, video: false };
        navigator.mediaDevices
          .getUserMedia(options)
          .then(function (stream) {
            //creare stream and store it locally : it will be used for stop recording
            myRecorder.objects.stream = stream;
            myRecorder.objects.recorder = new Recorder(
              myRecorder.objects.context.createMediaStreamSource(stream),
              { numChannels: 1 }
            );
            myRecorder.objects.recorder.record();
          })
          .catch(function (err) {});
      },
      stop: function (listObject) {
        if (null !== myRecorder.objects.stream) {
          myRecorder.objects.stream.getAudioTracks()[0].stop();
        }
        if (null !== myRecorder.objects.recorder) {
          myRecorder.objects.recorder.stop();
  
          // Validate object
          if (
            null !== listObject &&
            "object" === typeof listObject &&
            listObject.length > 0
          ) {
            // Export the WAV file
            myRecorder.objects.recorder.exportWAV(function (blob) {
              var url = (window.URL || window.webkitURL).createObjectURL(blob);
  
              // Prepare the playback
              var audioObject = $("<audio controls></audio>").attr("src", url);
  
              // Prepare the download link
              var downloadObject = $("<form><a>&#9660;</a></form>")
                .attr("href", url)
                .attr("download", new Date().toUTCString() + ".wav");
  
              // Wrap everything in a row
              var holderObject = $('<div class="row"></div>')
                .append(audioObject)
                .append(downloadObject);
  
              // Append to the list
              listObject.append(holderObject);
            });
          }
        }
      },
    };
  
    // Prepare the recordings list
    var listObject = $('[data-role="recordings"]');
  
    // Prepare the record button
    $('[data-role="controls"] > button').click(function () {
      // Initialize the recorder
      myRecorder.init();
  
      // Get the button state
      // !! -> convert the string into bool
      var buttonState = !!$(this).attr("data-recording");
  
      // Toggle
      if (!buttonState) {
        // start recording
        $(this).attr("data-recording", "true");
        myRecorder.start();
      } else {
        // stop recording
        // empty string refer to false 
        $(this).attr("data-recording", "");
        myRecorder.stop(listObject);
      }
    });
  });
  