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
        document.querySelector('#camera_btn').innerText = '開啟鏡頭'
    }else{
        videoTrack.enabled = true
        document.getElementById('camera_btn').style.backgroundColor = 'white'
        document.getElementById('camera_btn').style.boxShadow = '0 0 10px white'
        document.querySelector('#camera_btn').innerText = '闗閉鏡頭'
    }
}

let toggleMic = async () => {
    let audioTrack = localStream.getTracks().find(track => track.kind === 'audio')

    if(audioTrack.enabled){
        audioTrack.enabled = false
        document.getElementById('mic_btn').style.backgroundColor = 'rgb(255, 80, 80)'
        document.getElementById('mic_btn').style.boxShadow = '0 0 10px rgb(255, 80, 80)'
        document.querySelector('#mic_btn').innerText = '開啟麥克風'
    }else{
        audioTrack.enabled = true
        document.getElementById('mic_btn').style.backgroundColor = 'white'
        document.getElementById('mic_btn').style.boxShadow = '0 0 10px white'
        document.querySelector('#mic_btn').innerText = '闗閉麥克風'
    }
}

document.getElementById('camera_btn').addEventListener('click', toggleCamera)
document.getElementById('mic_btn').addEventListener('click', toggleMic)

init()