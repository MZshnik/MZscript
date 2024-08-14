const codeType = document.title == "Edit command" ? "command" : "event";
let codeinput = document.getElementsByClassName("code").item(0);

codeinput.oninput = () => {
    codeinput.style.height = "1px";
    codeinput.style.height = `${codeinput.scrollHeight}px`;
};

document.getElementsByClassName("save-button").item(0).onclick = () => {
    const name = document.getElementsByClassName("name").item(0).value;
    const code = document.getElementsByClassName("code").item(0).value;
    let notif = document.createElement("div");
    notif.className = "notification";

    fetch("api/edit-code", {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            name: name,
            code: code,
            type: codeType
        })
    })
    .then(() => {
        notif.classList.add("good-notif");
        notif.innerHTML = "Saved!";
        document.body.append(notif);
        setTimeout(() => {
            notif.remove();
        }, 3000);
    })
    .catch(() => {
        notif.classList.add("bad-notif");
        notif.innerHTML = "Failed!";
        document.body.append(notif);
        setTimeout(() => {
            notif.remove();
        }, 3000);
    });
}