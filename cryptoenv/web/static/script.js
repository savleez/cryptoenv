async function newFile() {
  let password = prompt("Enter the file password: ");

  try {
    validatePassword(password);
  } catch (error) {
    console.error("Se ha producido un error:", error.message);
    return;
  }

  let response = await fetch("/new_file", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      password: password,
    }),
  });

  displayContent(response);
}

function validatePassword(password) {
  if (!password || password === "") {
    throw new Error("Password must not be empty.");
  }
}

async function openFile() {
  let password = prompt("Enter the file password: ");

  try {
    validatePassword(password);
  } catch (error) {
    console.error("Se ha producido un error:", error.message);
    return;
  }

  let response = await fetch("/open", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      password: password,
    }),
  });

  displayContent(response);
}

async function displayContent(response) {
  let content;

  try {
    if (!response) {
      throw new Error(`Error: ${response}`);
    }

    let data = await response.json();

    if (response.ok) {
      content = data.decrypted_content;
    } else {
      if (data.slug == "file-does-not-exist") {
        content = "Encrypted file does not exist. Try creating a new one.";
      } else if (data.slug == "error-decrypting-file") {
        content = "Error decrypting file. Try again.";
      } else if (data.slug == "file-already-exists") {
        content = "Encrypted file already exists. Try opening it.";
      }
    }
  } catch (error) {
    console.error("Unknown error", error.message);
    return;
  }

  document.getElementById("file-content").value = JSON.stringify(content);
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
