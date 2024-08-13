document.getElementsByClassName("newcmd").item(0).onclick = () => {
    window.location.href = "/create-command";
};

document.getElementsByClassName("newevn").item(0).onclick = () => {
    window.location.href = "/create-event";
};

function editCode(cmd, type) {
    const name = cmd.parentElement.getElementsByTagName("h2")[0].textContent;
    const code = cmd.parentElement.getElementsByTagName("pre")[0].textContent;

    fetch("edit-code", {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            name: name,
            code: code,
            type: type
        })
    })
    .then(response => response.text())
    .then(data => {
        const newPage = document.implementation.createHTMLDocument();
        newPage.documentElement.innerHTML = data;
        document.documentElement.replaceWith(newPage.documentElement);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}