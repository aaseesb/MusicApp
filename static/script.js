// update play button based on state
const playIcon = document.getElementById('play-button');
const audio = document.getElementById('audio-player');

playIcon.classList.add('fa');
playIcon.classList.add('fa-play');

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