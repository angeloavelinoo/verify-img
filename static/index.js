document.getElementById("button-send").addEventListener("click", async (event) => {
    event.preventDefault();
    const fileInput = document.getElementById("file-input");
    const status = document.getElementById("status");
    const downloadLink = document.getElementById("download-link");

    if (fileInput.files.length === 0) {
        status.textContent = "Por favor, selecione uma imagem primeiro.";
        return;
    }

    const formData = new FormData();
    formData.append("image", fileInput.files[0]);

    status.textContent = "Enviando imagem...";
    downloadLink.style.display = "none";  

    try {
        const response = await fetch("http://127.0.0.1:5000/upload", {
            method: "POST",
            body: formData
        });

        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            downloadLink.href = url;
            downloadLink.download = "imagem_processada.png";
            downloadLink.style.display = "inline";  
            status.textContent = "Imagem processada com sucesso. Clique no link para baixar.";
        } else {
            status.textContent = "Erro ao processar a imagem.";
        }
    } catch (error) {
        status.textContent = "Erro ao enviar a imagem.";
    }
});
