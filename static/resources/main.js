var mainOutput1 = $('#output1');
var mainOutput2 = $('#output2');

function monitorFileChange() {
    $('#predict').click(function () {
        mainOutput1.html('')
        var radios = document.getElementsByName("model");
        for (var i = 0, length = radios.length; i < length; i++) {
            if (radios[i].checked) {
                var checked = radios[i].value;
                $.ajax({
                    url: "/_checked",
                    data: {
                        checked: checked,
                    },
                    type: 'GET'
                });
                break;
            }
        }

        var u = $('#url').val()
        var f = $('#uploadFileElem')[0].files[0];
        if (f == null && !u) {
            mainOutput2.html("<h3>need an image!</h3>")
            return
        };
        if (u && f == null) {
            GetUrl(u);
            return
        }
        if (f !== null) {
            GetFile(f);
            return
        }
    })
}

function GetUrl(u) {
    var image = new Image();
    image.src = u
    mainOutput1.html(image)
    $.ajax({
        url: "/_predict",
        data: {
            url: u,
        },
        type: 'GET',
        beforeSend: function () {
            mainOutput2.html('waiting...')
        },
        success: function (data) {
            if (data.signal == 1) {
                console.log(data)
                mainOutput2.html('It may be:' + data.class + "<br>Probability:")
                for (var i in data.predictions) {
                    mainOutput2.append("<br>" + data.predictions[i].class + ": " + data.predictions[i].prob * 100 + "%");
                }
            }
            else if (data.signal == 2) {
                console.log(data)
                mainOutput2.html("<img  src=\"data:;base64," + data.img_stream + "\">")
            }
        }
    })
}

function GetFile(f) {
    var readfile = new FileReader();
    readfile.readAsDataURL(f);
    readfile.onload = function (e) {
        var image = new Image();
        image.src = this.result
        mainOutput1.html(image)
    }
    var formData = new FormData();
    formData.append('file', f);
    $.ajax({
        url: "/_predict",
        data: formData,
        cache: false,
        processData: false,
        contentType: false,
        type: 'POST',
        beforeSend: function () {
            mainOutput2.html('waiting...')
        },
        success: function (data) {
            if (data.signal == 1) {
                console.log(data)
                mainOutput2.html('It may be:' + data.class + "<br>Probability:")
                for (var i in data.predictions) {
                    mainOutput2.append("<br>" + data.predictions[i].class + ": " + data.predictions[i].prob * 100 + "%");
                }
            }
            else if (data.signal == 2) {
                console.log(data)
                mainOutput2.html("<img  src=\"data:;base64," + data.img_stream + "\">")
            }
        }
    })
}


$(document).ready(function () {
    monitorFileChange();
});