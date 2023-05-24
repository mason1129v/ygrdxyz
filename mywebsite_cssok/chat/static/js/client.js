let localStream;

let init = async () => {
    localStream = await navigator.mediaDevices.getUserMedia({video:true, audio:true})
    document.getElementById('user').srcObject = localStream
}

init()