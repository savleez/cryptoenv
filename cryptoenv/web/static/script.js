async function createNewFile() {
  let fileName = prompt("New file name: ");

  if (!fileName) {
    return;
  }

  fileName = fileName ? fileName.trim() : fileName;

  if (fileName === "") {
    alert("Please enter a file name.");
    return;
  }

  let password = prompt("File password: ");

  if (!password) {
    return;
  }

  if (password === "") {
    alert("Please enter a password.");
    return;
  }

  let encryptedFileObj = {
    filename: fileName,
    password: password,
  };

  try {
    let response = await fetch("/new_file", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(encryptedFileObj),
    });

    let data = await response.json();

    if (response.ok) {
      let { filename, encrypted_content } = data;
      let blob = new Blob([encrypted_content], { type: "text/plain" });
      let url = window.URL.createObjectURL(blob);
      let a = document.createElement("a");
      a.style.display = "none";
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);

      encryptedFileObj.encrypted_content = encrypted_content;
    } else {
      let errorDetail = data.detail;
      throw Error(errorDetail);
    }
  } catch (error) {
    alert(`An error has occurred. ${error}`);
    return;
  }

  try {
    decryptAndDisplayContent(encryptedFileObj);
  } catch (error) {
    console.error(error);
    alert(`An error occurred. ${error}`);
  }
}

async function openFile() {
  fileInput.click();

  fileInput.addEventListener("change", async (event) => {
    let selectedFile = event.target.files[0];

    if (!selectedFile) {
      return;
    }

    try {
      let fileContent = await readFileContent(selectedFile);

      let password = prompt("File password: ");

      if (!password) {
        return;
      }

      if (password === "") {
        alert("Please enter a password.");
        return;
      }

      let encryptedFileObj = {
        filename: selectedFile.name,
        password: password,
        encrypted_content: fileContent,
      };

      decryptAndDisplayContent(encryptedFileObj);
    } catch (error) {
      alert("Error reading file: " + error);
    }
  });
}

async function decryptAndDisplayContent(encryptedFileObj) {
  try {
    let response = await fetch("/decrypt", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(encryptedFileObj),
    });

    if (response.ok) {
      let data = await response.json();
      let content = data.decrypted_content;

      document.getElementById("file-content").value = content;
    } else {
      alert("Error decrypting file.");
    }
  } catch (error) {
    console.error(error);
    alert("An error occurred.");
  }
}

async function readFileContent(file) {
  return new Promise((resolve, reject) => {
    let fileReader = new FileReader();

    fileReader.addEventListener("load", (event) => {
      let fileContent = event.target.result;
      resolve(fileContent);
    });

    fileReader.addEventListener("error", (event) => {
      reject("Error reading file: " + event.target.error);
    });

    fileReader.readAsText(file);
  });
}
