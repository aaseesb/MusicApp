// // when like button is pressed
// document.getElementById('like').addEventListener('click', function () {
//     // prevents users from liking songs if they are not logged in
//     if (!window.username) {
//         event.preventDefault();
//         alert("Please log in to like songs.");
//     }
//     // prevents users from liking songs if they have already liked them
//     const songTitle = window.song.title;  // Get the title of the current song
//     const songArtist = window.song.artist; // Get the artist of the current song

//     // Check if a song with the same title and artist exists in the playlist
//     const songExists = window.playlist.some(song => 
//         song.title === songTitle && song.artist === songArtist
//     );
    
//     if(songExists) {
//         event.preventDefault();
//         alert("You have already liked this song.");
//     }
// });