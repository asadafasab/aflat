const domain = "http://192.168.1.5:5000"

let getData = (url) => {
    return fetch(url).then(res => {
        if (res.ok) {
            return res.json()
        } else {
            return {}
        }
    })
        .then(data => data)
        .catch(err => err)
}

let sendData = (url, data) => {
    return fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    }).then(res => res.json())
}

let postComment = () => {
    let comment = document.getElementById("new_comment")

    const urlParams = new URLSearchParams(window.location.search)
    const id = urlParams.get("id")
    if (!comment.value) { return false }
    sendData(domain + "/comment", {
        id: id,
        comment: comment.value,
    }).then(res => {
        if (res.ok) {
            let comments = document.getElementById("comments")
            let date = new Date().toISOString().slice(0, 10)

            let node = document.createElement("p")
            node.className = "comment_comment"
            node.innerHTML = comment.value
            comments.insertBefore(node, comments.firstChild)

            node = document.createElement("p")
            node.className = "comment_title"
            node.innerHTML = "<b>You</b> " + date
            comments.insertBefore(node, comments.firstChild)

            comment.value = ""
        } else {
            alert("Error...")
        }
    })
}
let deleteUser = (username) => {
    console.log(username)
    sendData(domain + "/management", { username: username }).then(res => {
        if (res.ok) {
            let user = document.getElementById(username)
            user.style.display = "none"
        } else {
            alert("Error...")
        }
    })
}


let inputs
let messages

window.addEventListener('load', function () {
    inputs = document.querySelectorAll("#signup_form input")
    messages = document.querySelectorAll(".signup_error")
})

let checkSignupForm = () => {
    if (inputs[0].value == "") {
        messages[0].innerHTML = "Empty username"
        inputs[3].disabled = true
    } else {
        inputs[3].disabled = false
        messages[0].innerHTML = ""
    }
    if (inputs[1].value && inputs[2].value && inputs[1].value === inputs[2].value) {
        messages[1].innerHTML = ""
        inputs[3].disabled = false
    } else {
        inputs[3].disabled = true
        messages[1].innerHTML = "Check passwords"

    }
}

let generate_image = () => {
    let new_image = document.getElementById("generated_img")
    let message = document.getElementById("published")
    getData(domain + "/generate", {}).then(res => {
        new_image.src = res.path + "?" + new Date().getTime()
        message.innerHTML = ""
    })

}


let add_new_image = () => {
    let new_image = document.getElementById("generated_img")
    let message = document.getElementById("published")
    getData(domain + "/publish", {}).then(res => {
        message.innerHTML = "Published"
        new_image.src = ""
    })
}

let stonks = (id) => {
    let btn = document.getElementById("stonks_btn" + id)

    sendData(domain + "/stonks", {
        post_id: id
    }).then(res => {
        if (res.ok) {
            if (btn.classList.contains("stonks_btn")) {
                btn.classList.remove("stonks_btn")
                btn.classList.add("stonks_btn_active")
                alert("congrats you've stonked this painting")
                //TODO pop up
            } else {
                btn.classList.add("stonks_btn")
                btn.classList.remove("stonks_btn_active")
            }
        } else {
            alert("something went wrong...")
        }
    })
}
let stonks_login = () => {
    alert("to do this you must login")
}



let loadImage = (event) => {
    let output = document.getElementById('upload_image');
    output.src = URL.createObjectURL(event.target.files[0]);
    output.onload = () => {
        URL.revokeObjectURL(output.src) // free memory
    }
}