const SAMPLE = {
    'playlist': 'https://www.youtube.com/playlist?list=PL-osiE80TeTskrapNbzXhwoFUiLCjGgY7',
    'channel': 'https://www.youtube.com/@coreyms/playlists'
}
const playlistInput = document.getElementById('playlistInput')
const channelInput = document.getElementById('channelInput')
const PLAYLIST_TRACKER = document.querySelector('.playlist.statusTracker')
const CHANNEL_TRACKER = document.querySelector('.channel.statusTracker')


function tryExample(mode) {
    if (mode === 'playlist') {
        playlistInput.value = SAMPLE['playlist']
        getStats('playlist')

    } else if (mode === 'channel') {
        channelInput.value = SAMPLE['channel']
        getStats('channel')
    }
}

function getStats(mode) {
    let url, splittedUrl, apiPath

    if (mode === 'playlist') {
        url = playlistInput.value
        splittedUrl = url.split('https://www.youtube.com/')
        apiPath = 'getPlaylistStats'
        CHANNEL_TRACKER.textContent = ''
    } else if (mode === 'channel') {
        url = channelInput.value
        splittedUrl = url.split('https://www.youtube.com/')
        apiPath = 'getChannelStats'
        PLAYLIST_TRACKER.textContent = ''
    }

    // updateStatus('loading')
    const CURRENT_TRACKER = document.querySelector(`.${mode}.statusTracker`)
    CURRENT_TRACKER.textContent = 'Collecting stats...'
    CURRENT_TRACKER.classList.remove('flash')
    fetch(
        `${window.location.origin}/${apiPath}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            url: 'https://www.youtube.com/',
            query: splittedUrl[1]
        })
    })
        .then(response => response.blob())
        .then(blob => {
            const STATUS_BAR = document.querySelector(`.${mode}.statusTracker`)
            STATUS_BAR.textContent = 'Stats collected!'
            STATUS_BAR.classList.add('flash')
            setTimeout(() => {
                STATUS_BAR.classList.remove('flash');
            }, 10000);

            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `Scraped ${mode} ${getDate()}.csv`;
            document.body.appendChild(a);
            a.click();
            a.remove();
        })
}

function getDate() {
    const today = new Date();
    const day = String(today.getDate()).padStart(2, '0');
    const month = String(today.getMonth() + 1).padStart(2, '0'); // Months are 0-based
    const year = today.getFullYear();
    const formattedDate = `${day}-${month}-${year}`;
    return formattedDate
}

function clearInput(mode) {
    if (mode === 'playlist') {
        playlistInput.value = ''
    } else if (mode === 'channel') {
        channelInput.value = ''
    }
}

