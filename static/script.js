const playIcon = document.getElementById('play-button');
const audioPlayer = document.getElementById('audio-player');

const progress = document.getElementById('progress');
const currentTime = document.getElementById('current-time');
const duration = document.getElementById('duration');

// applies display for playIcon
playIcon.classList.add('fa', 'fa-spinner', 'fa-pulse');

// loads audio after page has loaded
document.addEventListener('DOMContentLoaded', function() {
    loadAudio();
});

function loadAudio() {
    console.log('fetching')
    fetch('/retrieve-audio', {
        method: 'POST', 
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            title: audioPlayer.getAttribute('data-title'),
            artist: audioPlayer.getAttribute('data-artist')
        })
    })
    .then(response => response.json())  
    .then(data => {
        console.log(data);

        audioPlayer.crossOrigin = "anonymous";
        
        // apply audio source to source element
        audioPlayer.src = data.url;

        // load audio
        audioPlayer.load();
        console.log(audioPlayer.readyState);
    })
}

// updates display once audio is loaded
audioPlayer.addEventListener('canplaythrough', () => {
    // once loaded, update play icon from loader to play
    playIcon.classList.remove('fa', 'fa-spinner', 'fa-pulse');
    playIcon.classList.add('fa', 'fa-play');
    
    // retrieve max song duration, apply to text and progress bar
    progress.max = audioPlayer.duration;
    duration.textContent = format(audioPlayer.duration);
});

// format time (without this, it shows as seconds with decimals)
function format(time) {
    // calculate minutes and seconds (rounded down)
    const minutes = Math.floor(time/60);
    const seconds = Math.floor(time%60);

    if (seconds < 10) {
        return `${minutes}:0${seconds}`;

    } else {
        return `${minutes}:${seconds}`;
    }
}

// check for time updated
audioPlayer.addEventListener('timeupdate', () => {
    // update progress bar and time based on amount of song played
    progress.value = audioPlayer.currentTime;
    currentTime.textContent = format(audioPlayer.currentTime);
});

// check for input in progress bar
progress.addEventListener('input', () => {
    // allow users to change time in song
    audioPlayer.currentTime = progress.value;
    currentTime.textContent = format(audioPlayer.currentTime);
});

// check for play button clicked to change icon
playIcon.addEventListener('click', () => {
    if (playIcon.classList.contains('fa-play')) {
        playIcon.classList.remove('fa','fa-play');
        playIcon.classList.add('fa', 'fa-pause')
        audioPlayer.play().then(() => {
            runVisualizer(audioPlayer);
        });
    } else {
        audioPlayer.pause();
        playIcon.classList.remove('fa','fa-pause')
        playIcon.classList.add('fa','fa-play');
    }
});

function runVisualizer() {
    if (!context) {
        var context = new AudioContext();
        var src = context.createMediaElementSource(audioPlayer);
    }
    var analyser = context.createAnalyser();
    
    var canvas = document.getElementById("canvas");
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    var ctx = canvas.getContext("2d");

    src.connect(analyser);
    analyser.connect(context.destination);

    analyser.fftSize = 256;

    var bufferLength = analyser.frequencyBinCount;
    console.log(bufferLength);

    var dataArray = new Uint8Array(bufferLength);

    var WIDTH = canvas.width;
    var HEIGHT = canvas.height;

    var barWidth = (WIDTH / bufferLength) * 2.5;
    var barHeight;
    var x = 0;

        function renderFrame() {
        animationId = requestAnimationFrame(renderFrame);

        x = 0;

        analyser.getByteFrequencyData(dataArray);

        // ctx.fillStyle = "#fff";
        // ctx.fillRect(0, 0, WIDTH, HEIGHT);
        ctx.clearRect(0, 0, WIDTH, HEIGHT);

        for (var i = 0; i < bufferLength; i++) {
            barHeight = dataArray[i];
            
            var r = barHeight + (25 * (i/bufferLength));
            var g = 250 * (i/bufferLength);
            var b = 50;

            // ctx.fillStyle = "rgb(" + r + "," + g + "," + b + ")";
            ctx.fillStyle = "rgb(" + 0 + "," + 0 + "," + 0 + ")"
            ctx.fillRect(x, HEIGHT - barHeight, barWidth, barHeight);

            x += barWidth + 1;
        }
    }

    renderFrame();
}

audioPlayer.addEventListener('error', (e) => {
    const error = audioPlayer.error;
    if (error) {
        console.error("Audio error code:", error.code);
        switch (error.code) {
            case 1: console.error("MEDIA_ERR_ABORTED"); break;
            case 2: console.error("MEDIA_ERR_NETWORK"); break;
            case 3: console.error("MEDIA_ERR_DECODE"); break;
            case 4: console.error("MEDIA_ERR_SRC_NOT_SUPPORTED"); break;
            default: console.error("Unknown error");
        }
    }
});