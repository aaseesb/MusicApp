const playIcon = document.getElementById('play-button');
const audio = document.getElementById('audio-player');

const progress = document.getElementById('progress');
const currentTime = document.getElementById('current-time');
const duration = document.getElementById('duration');


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

// when metadata has loaded
audio.addEventListener('loadedmetadata', () => {
    // apply max song duration to text and progress bar
    progress.max = audio.duration;
    duration.textContent = format(audio.duration);
});


// check for time updated
audio.addEventListener('timeupdate', () => {
    // update progress bar and time based on amount of song played
    progress.value = audio.currentTime;
    currentTime.textContent = format(audio.currentTime);
});


// check for input in progress bar
progress.addEventListener('input', () => {
    // allow users to change time in song
    audio.currentTime = progress.value;
    currentTime.textContent = format(audio.currentTime);
});

// update play button based on state
playIcon.classList.add('fa');
playIcon.classList.add('fa-play');

// check for play button clicked
playIcon.addEventListener('click', () => {
    if (playIcon.classList.contains('fa-play')) {
        audio.play();
        playIcon.classList.remove('fa','fa-play');
        playIcon.classList.add('fa', 'fa-pause')
    } else {
        audio.pause();
        playIcon.classList.remove('fa','fa-pause')
        playIcon.classList.add('fa','fa-play');
    }
});