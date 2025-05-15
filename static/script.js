const playIcon = document.getElementById('play-button');
const audioPlayer = document.getElementById('audio-player');
const audioSourceElement = document.getElementById('audio-source');

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
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            title: audioSourceElement.getAttribute('data-title'),
            artist: audioSourceElement.getAttribute('data-artist')
        })
    })
    .then(response => response.json())  
    .then(data => {
        console.log(data);
        // apply audio source to source element
        audioSourceElement.src = data;

        // load audio
        audioPlayer.load()
    })
}

// updates display once audio is loaded
audioPlayer.addEventListener('canplay', () => {
    // once loaded, update play icon from loader to play
    playIcon.classList.remove('fa', 'fa-spinner', 'fa-pulse');
    playIcon.classList.add('fa', 'fa-play');
    
    // retrieve max song duration, apply to text and progress bar
    progress.max = audioPlayer.duration;
    duration.textContent = format(audioPlayer.duration);
});

// when metadata has loaded
//     () => {
//     // apply max song duration to text and progress bar
//     progress.max = audioPlayer.duration;
//     duration.textContent = format(audioPlayer.duration);
// });


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
        audioPlayer.play();
        playIcon.classList.remove('fa','fa-play');
        playIcon.classList.add('fa', 'fa-pause')
    } else {
        audioPlayer.pause();
        playIcon.classList.remove('fa','fa-pause')
        playIcon.classList.add('fa','fa-play');
    }
});