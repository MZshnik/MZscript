const codeType = document.title == "Edit command" ? "command" : "event";

document.getElementsByClassName("save-button").item(0).onclick = () => {
    const name = document.getElementsByClassName("name").item(0).value;
    const code = document.getElementsByClassName("code").item(0).value;

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
    });
}