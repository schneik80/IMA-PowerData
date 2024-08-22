function getDateString() {
    const today = new Date();
    const date = `${today.getDate()}/${today.getMonth() + 1}/${today.getFullYear()}`;
    const time = `${today.getHours()}:${today.getMinutes()}:${today.getSeconds()}`;
    return `${date}, Time: ${time}`;
}

function sendInfoToFusion() {
    const args = {
        formInputValue: document.getElementById("formInput").value,
        timeStamp: getDateString()
    };

    // Send the data to Fusion as a JSON string. The return value is a Promise.
    adsk.fusionSendData("formMessage", JSON.stringify(args))
        .then((result) =>
            document.getElementById("returnValue").innerHTML = `${result}`
        );

}

function updateMessage(messageData) {
    // Update Message div with the data passed in.
    document.getElementById("stringMessage").innerHTML =
        `${messageData.message}`;
}


function updateSelection(messageData) {
    // Update Selection div with the data passed in.
    document.getElementById("selectionMessage").innerHTML =
        `<b>Name</b>: ${messageData.selection_name} <br/>` +
        `<b>Object Type</b>: ${messageData.selection_type}`;
}


window.fusionJavaScriptHandler = {
    handle: function (action, messageString) {
        try {
            // Message is sent from the add-in as a JSON string.
            const messageData = JSON.parse(messageString);
            if (action === "updateMessage") {
                updateMessage(messageData);
            } else if (action === "updateSelection") {
                updateSelection(messageData);
            } else if (action === "debugger") {
                debugger;
            } else {
                return `Unexpected command type: ${action}`;
            }
        } catch (e) {
            console.log(e);
            console.log(`Exception caught with command: ${action}, data: ${data}`);
        }
        return "OK";
    },
};
