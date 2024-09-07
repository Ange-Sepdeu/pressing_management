$(document).ready(function() {
    $('#promoVideo').on('ended', function() {
        this.currentTime = 0;
        this.play();
    });
});