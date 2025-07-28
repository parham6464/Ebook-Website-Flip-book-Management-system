window.onkeydown = function(evt) {
        if(evt.keyCode == 123 || evt.keyCode == 85 || evt.keyCode == 17 || evt.keyCode == 16 || evt.keyCode == 74 || evt.keyCode == 116 || evt.keyCode == 73 || evt.keyCode == 8 || evt.KeyCode == 13 || evt.KeyCode == 16 || evt.KeyCode == 17 || evt.KeyCode == 83) return false;
e.preventDefault();
    };
    window.onkeypress = function(evt) {
        if(evt.keyCode == 123 || evt.keyCode == 85 || evt.keyCode == 17 || evt.keyCode == 16 || evt.keyCode == 74 || evt.keyCode == 116 || evt.keyCode == 73 || evt.keyCode == 8 || evt.KeyCode == 13 || evt.KeyCode == 16 || evt.KeyCode == 17 || evt.KeyCode == 83) return false;
e.preventDefault();
    };
    window.onkeyup = function(evt) {
        if(evt.keyCode == 123 || evt.keyCode == 85 || evt.keyCode == 17 || evt.keyCode == 16 || evt.keyCode == 74 || evt.keyCode == 116 || evt.keyCode == 73 || evt.keyCode == 8 || evt.KeyCode == 13 || evt.KeyCode == 16 || evt.KeyCode == 17 || evt.KeyCode == 83) return false;
    document.onkeydown = function (e) {
    e = e || window.event;
    if (e.ctrlKey) {
        var c = e.which || e.keyCode;
        switch (c) {
            case 83://Block Ctrl+S
            case 87://Block Ctrl+W 
                e.preventDefault();     
                e.stopPropagation();
            break;
        }
    }
};
    };
function disableF5(e) { if ((e.which || e.keyCode) == 116) e.preventDefault(); };
// $(document).on("keydown", disableF5);