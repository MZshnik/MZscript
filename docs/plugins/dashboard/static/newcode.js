const codeType = document.title == "Create new Command" ? "command" : "event";

nameinput = document.getElementsByClassName("name").item(0);
codeinput = document.getElementsByClassName("code").item(0);
if (codeType == "command") {
    nameinput.value = "!help"
    codeinput.value = "$sendMessage[Hello World]"
} else {
    nameinput.value = "message"
    codeinput.value = "$if[$userInfo[bot]] $stop $endif $sendMessage[Hello World]"
}
codeinput.oninput = () => {
    codeinput.style.height = "1px";
    codeinput.style.height = `${codeinput.scrollHeight}px`;
};

document.getElementsByClassName("create-button").item(0).onclick = () => {
    fetch("api/create-code", {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            name: nameinput.value,
            code: codeinput.value,
            type: codeType
        })
    });
};