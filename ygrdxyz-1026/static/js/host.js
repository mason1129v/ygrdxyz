let localStream;

let init = async () => {
    localStream = await navigator.mediaDevices.getUserMedia({video:true, audio:true})
    document.getElementById('user').srcObject = localStream
}

let toggleCamera = async () => {
    let videoTrack = localStream.getTracks().find(track => track.kind === 'video')

    if(videoTrack.enabled){
        videoTrack.enabled = false
        document.getElementById('camera_btn').style.backgroundColor = 'rgb(255, 80, 80)'
        document.getElementById('camera_btn').style.boxShadow = '0 0 10px rgb(255, 80, 80)'
        document.getElementById('camera_btn').style.color = 'white'
        document.querySelector('#camera_btn').innerHTML = '<i class="fa-solid fa-video-slash fa-lg"></i>'
    }else{
        videoTrack.enabled = true
        document.getElementById('camera_btn').style.backgroundColor = 'white'
        document.getElementById('camera_btn').style.boxShadow = '0 0 10px white'
        document.getElementById('camera_btn').style.color = 'black'
        document.querySelector('#camera_btn').innerHTML = '<i class="fa-solid fa-video fa-lg"></i>'
    }
}

let toggleMic = async () => {
    let audioTrack = localStream.getTracks().find(track => track.kind === 'audio')

    if(audioTrack.enabled){
        audioTrack.enabled = false
        document.getElementById('mic_btn').style.backgroundColor = 'rgb(255, 80, 80)'
        document.getElementById('mic_btn').style.boxShadow = '0 0 10px rgb(255, 80, 80)'
        document.getElementById('mic_btn').style.color = 'white'
        document.querySelector('#mic_btn').innerHTML = '<i class="fa-solid fa-microphone-slash fa-lg"></i>'
        
    }else{
        audioTrack.enabled = true
        document.getElementById('mic_btn').style.backgroundColor = 'white'
        document.getElementById('mic_btn').style.boxShadow = '0 0 10px white'
        document.getElementById('mic_btn').style.color = 'black'
        document.querySelector('#mic_btn').innerHTML = '<i class="fa-solid fa-microphone fa-lg"></i>'
    }
}

document.getElementById('camera_btn').addEventListener('click', toggleCamera)
document.getElementById('mic_btn').addEventListener('click', toggleMic)

init()