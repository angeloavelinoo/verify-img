document.getElementById("button-send").addEventListener("click", async () => {
    const fileInput = document.getElementById("file-input");
    const status = document.getElementById("status");

    if (fileInput.files.length === 0) {
        status.textContent = "Por favor, selecione uma imagem primeiro.";
        return;
    }

    const formData = new FormData();
    formData.append("image", fileInput.files[0]);

    status.textContent = "Enviando imagem...";

    try {
        const response = await fetch("http://127.0.0.1:5000/upload", {
            method: "POST",
            body: formData
        });

        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const link = document.createElement("a");
            link.href = url;
            link.download = "frames_e_resultado.zip";
            link.click();
            window.URL.revokeObjectURL(url);
            status.textContent = "Imagem processada com sucesso. Download iniciado.";
        } else {
            status.textContent = "Erro ao processar a imagem.";
        }
    } catch (error) {
        status.textContent = "Erro ao enviar a imagem.";
    }
});
