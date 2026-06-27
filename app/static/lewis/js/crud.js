//ola
// Cargar lista de moléculas guardadas
function cargarListaStructs() {
    fetch(loadAllStructsUrl)
        .then(res => res.json())
        .then(data => {
            const lista_mol = document.getElementById('moleculeList');
            lista_mol.innerHTML = '';
            data.forEach(g => {
            const opt = document.createElement('div');
            opt.className = "mol-item";
                opt.innerHTML = `
                    <span class="mol-name">${formatFormula(g.name)}</span>
                    <div class="actions">
                        <button onclick="viewMol('${g.name}')">👁</button>
                        <button onclick="deleteMol('${g.id}')">🗑</button>
                    </div>
                `;
            lista_mol.appendChild(opt);
            });
    });
}

// Carga molécula por nombre y la imprime en el "canvas"
function viewMol(name) {
    if (!name) return;
    if (moleculeName === name) return; // ya está cargada
    const url = loadStructUrl.replace(
        "__NAME__",
        encodeURIComponent(name)
    );
    //console.log("Ver molécula:", name);
    
    fetch(url)
        .then(async response => {
        const result = await response.json();
        if (response.status === 400 || response.status === 404) {
            moleculeName = null;
            return alert(`Error al cargar la molécula ${name}.\n${result.message}`);
            return;
        }
        if (!response.ok) {
            // Aquí entrará para códigos 400, 404, 500, etc.
            throw new Error(result.message);
        }
        return result;
    })
        .then(data => {
            // Dibujar nueva molécula
            moleculeName = name;
            title.innerHTML = `Estructura de Lewis de ${formatFormula(name)}`;
            drawMolecule(data.nodes, data.edges);
            setStatus("Esperando entrada", "⏳ Esperando entrada");
        });
}

// Elimina la molécula en base a la id
function deleteMol(id) {
    if (!id) return;
    const url = deleteStructUrl.replace(
        "0",
        encodeURIComponent(id)
    );
    
    fetch(url, {
        method: 'POST',
        headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken
        },
        credentials: "same-origin"
    })
    .then(async response => {
        const result = await response.json();
        if (response.status === 404) {
            moleculeName = null;
            alert(`Error al intentar eliminar la molécula.\n${result.message}`);
            return;
        }
        if (!response.ok) {
            // Aquí entrará para códigos 400, 404, 500, etc.
            throw new Error(result.message);
        }
        return result;
    })
    .then(data => {
        alert(`Molécula eliminada con éxito.`);
        cargarListaStructs();
    });
}

// Manda a guardar la molécula actual en la base de datos
function saveMol() {
    console.log("Guardando molécula:", moleculeName);
    //return
    if (!moleculeName) return;

    fetch(saveStructUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        credentials: "same-origin",
        body: JSON.stringify({
            name: moleculeName
        })
    })
    .then(async response => {
        const result = await response.json();
        if (response.status === 400) {
            alert(`Error al guardar la molécula ${moleculeName}.\n${result.message}`);
            return false;
        }
        if (!response.ok) {
            // Aquí entrará para códigos 400, 404, 500, etc.
            throw new Error(result.message);
        }

        return result;
    })
    .then(data => {
        cargarListaStructs();
        alert(`Molécula ${moleculeName} guardada con éxito.`);
    });
}

/* VALIDACIÓN CONJUNTA CON BACKEND */

// Control de UI de validación de molécula
function validateMolecule() {
    const value = input.value.trim();
    if (!value) {
        setStatus("idle", "⏳ Esperando entrada");
        return;
    }

    setStatus("checking", "⏳ Validando...");

    setTimeout(() => {
        isValidMolecule(value)
        .then(result => {
            CONDITION = result;
            console.log("CONDITION", CONDITION)
            if (CONDITION) {
                setStatus("valid", "✅ Molécula válida");
            } else {
                setStatus("invalid", "❌ Molécula inválida");
            }
            console.log("moleculeName", moleculeName)
        });
        
        

    }, 400);
}

// Valida la molécula con el backend y dibuja la estructura si es válida
function isValidMolecule(text) {
    const regex = /^[A-Z][a-z]?\d*([A-Z][a-z]?\d*)*$/;
    if (regex.test(text) === false) {
        return false;
    }
    return fetch(validateStructUrl, {
        method: 'POST',
        headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken
        },
        credentials: "same-origin",
        body: JSON.stringify({
            name: text
        })
    })
    .then(async response => {
        const result = await response.json();
        if (response.status === 400) {
            alert(`Error al validar la molécula ${text}.\n${result.message}`);
            moleculeName = null;
            return false;
        }
        if (!response.ok) {
            // Aquí entrará para códigos 400, 404, 500, etc.
            throw new Error(result.message);
        }

        return result;
    })
    .then(data => {
        if (!data) {
            return false;
        }
        // Dibujar nueva molécula
        window.moleculeName = text;
        title.innerHTML = `Estructura de Lewis de ${formatFormula(text)}`;
        drawMolecule(data.nodes, data.edges);
        return true;
    });
}


/* ESTADO UI */
function setStatus(state, message) {

    status.textContent = message;

    if (state === "valid") {
        saveBtn.disabled = false;
    } else {
        saveBtn.disabled = true;
    }
}
// Estilo de la molécula con subíndices para los números
function formatFormula(formula) {
    return formula.replace(
        /(\d+)/g,
        '<sub>$1</sub>'
    );
}

cargarListaStructs();
const input = document.getElementById("molInput");
const status = document.getElementById("status");
const saveBtn = document.getElementById("saveBtn");
const validateBtn = document.getElementById("validateBtn");
const title = document.getElementById("title");
title.innerHTML = `Estructura de Lewis de ${formatFormula(moleculeName)}`;


/* EVENTOS */
/* BOTÓN CLICK */
validateBtn.addEventListener("click", validateMolecule);

/* ENTER EN INPUT */
input.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
        validateMolecule();
    }
});