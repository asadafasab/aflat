const protocol = window.location.protocol;
const domain1 = window.location.hostname;
const port = window.location.port;

const domain = `${protocol}//${domain1}:${port ? port : ""}`

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
    let comment = document.getElementById("new-comment")

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
            node.className = "subtitle"
            node.innerHTML = comment.value
            comments.insertBefore(node, comments.firstChild)

            node = document.createElement("p")
            node.className = "subtitle pb-0 mb-0"
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

//burger menu
const burger = document.querySelector("#burger")
const navbarMenu = document.querySelector("#nav-menu")
burger.addEventListener("click", () => {
    navbarMenu.classList.toggle("is-active")
})

let checkSignupForm = () => {
    let username = document.getElementById("username_signup")
    let passwd1 = document.getElementById("password_signup1")
    let passwd2 = document.getElementById("password_signup2")
    let msg1 = document.getElementById("msg1")
    let msg2 = document.getElementById("msg2")
    let msgServ = document.getElementById("message-server")

    if (username.value == "") {
        msg1.style.display = "block"
    } else {
        msg1.style.display = "none"
    }
    if (passwd1.value != "" && (passwd1.value === passwd2.value)) {
        msg2.style.display = "none"

        login = {
            username: username.value,
            password: passwd1.value
        }
        if (username.value != "") {
            sendData(domain + "/signup", {
                username: username.value,
                password: passwd1.value
            }).then(res => {
                if (res.ok) {
                    username.value = ""
                    passwd1.value = ""
                    passwd2.value = ""
                    alert("Now you can login.")
                } else {
                    msgServ.innerHTML = res.error
                }
                console.log(res)
            })
        }
    } else {
        msg2.style.display = "block"
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
    let btn = document.getElementById("stonk" + id)
    console.log(btn)
    sendData(domain + "/stonks", {
        post_id: id
    }).then(res => {
        if (res.ok) {
            alert("congrats you've stonked this painting")
            btn.classList.toggle("stonk-active")
        } else {
            alert("something went wrong...")
        }
    })
}

let loadImage = (event) => {
    let output = document.getElementById('upload_image');
    output.src = URL.createObjectURL(event.target.files[0]);
    output.onload = () => {
        URL.revokeObjectURL(output.src) // free memory
    }
}
