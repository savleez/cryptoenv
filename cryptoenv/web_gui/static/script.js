async function createNewFile() {
  let fileName = prompt("New file name: ").trim();

  if (fileName === "") {
    alert("Please enter a file name.");
    return;
  }

  let password = prompt("File password: ").trim();

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
      let { filename, content } = data;
      let blob = new Blob([content], { type: "text/plain" });
      let url = window.URL.createObjectURL(blob);
      let a = document.createElement("a");
      a.style.display = "none";
      a.href = url;
      a.download = `${filename}.encrypted`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);

      encryptedFileObj.encrypted_content = content;
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

async function decryptAndDisplayContent(encryptedFileObj = null) {
  if (!encryptedFileObj) {
    let password = prompt("File password: ").trim();

    if (password === "") {
      alert("Please enter a password.");
      return;
    }

    // TODO: Fix the open file feature
    const fileInput = document.getElementById("file");

    fileInput.addEventListener("change", (event) => {
      const selectedFile = event.target.files[0]; // Puedes acceder a más archivos si es necesario

      if (selectedFile) {
        const fileName = selectedFile.name;
        console.log(`Archivo seleccionado: ${fileName}`);
      }
    });

    let encryptedFileObj = {
      filename: selectedFile,
      password: password,
    };

    console.log(encryptedFileObj);
  }

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
