$(document).ready(function () {
        DefaultBox();
  });

function DefaultBox(){

}

var uploadFiles = [];
var input = document.getElementById("drop_box");

input.addEventListener("dragenter",(event)=>{
    event.preventDefault();
    console.log("dragenter");
    console.log(event.target.className);
    if(event.target.className =="dropbox"){
        console.log("dropbox")
        event.target.style.background = "#616161";
    }
});

input.addEventListener("dragover", (event) => {
  //console.log("dragover");
  event.preventDefault();
});

input.addEventListener("dragleave",(event)=>{
    event.preventDefault();

    console.log(event.target.className );
    if(event.target.className =="dropbox"){
        event.target.style.background = "#FFF";
    }
});

input.addEventListener("drop", (event) => {
    event.preventDefault();
    console.log("drop");
    if (event.target.className == "dropbox") {
        event.target.style.background = "#3a3a3a";
    }

    var files = event.dataTransfer?.files;;  //드래그&드랍 항목
    for (var i = 0; i < files.length; i++) {
        var file = files[i];
        var size = uploadFiles.push(file);
        preview(file, size - 1);
    }

});

function preview(file, idx) {
  var reader = new FileReader();
  reader.onload = (function(f, idx) {
    return function(e) {
       changeDropClass();
      var div = '<div class="changeBox" id="changeBox"> \
        <img class="imgBox" src="' + e.target.result + '" title="' + escape(f.name) + '"/> \
      </div>';
      console.log(e.target.result);
      $("#imageBox").append(div);
    };
  })(file, idx);

  reader.readAsDataURL(file);
}

function changeDropClass(){
    document.querySelector('#drop_box').classList.replace('dropbox', 'hidebox');

}
