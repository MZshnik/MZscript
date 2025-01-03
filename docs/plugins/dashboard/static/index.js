document.getElementsByClassName("newcmd").item(0).onclick = () => {
    window.location.href = "/create-command";
};

document.getElementsByClassName("newevn").item(0).onclick = () => {
    window.location.href = "/create-event";
};

function editCode(cmd, type) {
    const name = cmd.parentElement.getElementsByTagName("h2")[0].textContent;
    const code = cmd.parentElement.getElementsByTagName("pre")[0].textContent;
    const queryParams = new URLSearchParams();
    queryParams.append('name', name);
    queryParams.append('code', code);
    queryParams.append('type', type);
    window.location.href = `edit-code?${queryParams.toString()}`;
}