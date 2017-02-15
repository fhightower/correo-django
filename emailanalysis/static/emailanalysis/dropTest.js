Dropzone.autoDiscover = false;

var myDropzone = new Dropzone(".dropzone", {
  // url: "{% url 'emailanalysis:submit_file' %}",
  addRemoveLinks: true,
  thumbnailWidth: "80",
  thumbnailHeight: "80",
  dictCancelUpload: "Cancel",
  parallelUploads: 100,
  autoProcessQueue: false
});

myDropzone.element.querySelector("button[type=submit]").addEventListener("click", function(e) {
      // Make sure that the form isn't actually being sent.
    myDropzone.processQueue();
    // $.ajax({
    //     type: "POST",
    //     url: "http://localhost:8000/email/import/submitFile",
    //     dataType: "json",
    //     async: true,
    //     data: {},
    //     success: function (json_data) {
    //         alert(json_data)
    //     },
    //     error: function(json_data) {
    //         console.log("error", json_data);
    //     }
    // });
});

// Dropzone.options.myAwesomeDropzone = { // The camelized version of the ID of the form element

//   autoProcessQueue: false,
//   uploadMultiple: true,
//   parallelUploads: 100,
//   maxFiles: 100,

//   // The setting up of the dropzone
//   init: function() {
//     var myDropzone = this;

//   //   // First change the button to actually tell Dropzone to process the queue.
//     this.element.querySelector("button[type=submit]").addEventListener("click", function(e) {
//       // Make sure that the form isn't actually being sent.
//       console.log("here");
//       e.preventDefault();
//       e.stopPropagation();
//       myDropzone.processQueue();
//     });

//   //   // Listen to the sendingmultiple event. In this case, it's the sendingmultiple event instead
//   //   // of the sending event because uploadMultiple is set to true.
//     // this.on("sendingmultiple", function() {
//     //   // Gets triggered when the form is actually being sent.
//     //   // Hide the success button or the complete form.
//     // });
//     this.on("successmultiple", function(files, response) {
//       // Gets triggered when the files have successfully been sent.
//       // Redirect user or notify of success.
//       console.log("here", files);
//       console.log("resp", response);
//     });
//   //   this.on("errormultiple", function(files, response) {
//   //     // Gets triggered when there was an error sending the files.
//   //     // Maybe show form again, and notify user of error
//   //   });
//   }
// }