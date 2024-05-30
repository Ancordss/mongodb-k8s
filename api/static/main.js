document.getElementById('cliente-form').addEventListener('submit', async (event) => {
    event.preventDefault();
    const dni = document.getElementById('cliente-dni').value;
    const nombre = document.getElementById('cliente-nombre').value;
    const apellido = document.getElementById('cliente-apellido').value;
    const direccion = document.getElementById('cliente-direccion').value;
    const telefono = document.getElementById('cliente-telefono').value;
    const email = document.getElementById('cliente-email').value;

    const response = await fetch('/clientes', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ dni, nombre, apellido, direccion, telefono, email }),
    });

    if (response.ok) {
        alert('Cliente agregado exitosamente');
    } else {
        alert('Error al agregar cliente');
    }
});

document.getElementById('asunto-form').addEventListener('submit', async (event) => {
    event.preventDefault();
    const numero_expediente = document.getElementById('asunto-expediente').value;
    const dni_cliente = document.getElementById('asunto-cliente-dni').value;
    const fecha_inicio = document.getElementById('asunto-fecha-inicio').value;
    const estado = document.getElementById('asunto-estado').value;

    const cliente = await fetch(`/clientes/${dni_cliente}`).then(res => res.json());
    if (!cliente.dni) {
        alert('Cliente no encontrado');
        return;
    }

    const response = await fetch('/asuntos', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            numero_expediente,
            cliente,
            fecha_inicio,
            estado,
            procuradores: [],
            audiencias: [],
        }),
    });

    if (response.ok) {
        alert('Asunto agregado exitosamente');
    } else {
        alert('Error al agregar asunto');
    }
});

document.getElementById('consulta-cliente-form').addEventListener('submit', async (event) => {
    event.preventDefault();
    const dni = document.getElementById('consulta-cliente-dni').value;

    const response = await fetch(`/clientes/${dni}`);
    const cliente = await response.json();

    const resultDiv = document.getElementById('consulta-cliente-result');
    if (response.ok) {
        resultDiv.innerHTML = `<p>Nombre: ${cliente.nombre} ${cliente.apellido}</p><p>Dirección: ${cliente.direccion}</p><p>Teléfono: ${cliente.telefono}</p><p>Email: ${cliente.email}</p>`;
    } else {
        resultDiv.innerHTML = '<p>Cliente no encontrado</p>';
    }
});

document.getElementById('consulta-asunto-form').addEventListener('submit', async (event) => {
    event.preventDefault();
    const numero_expediente = document.getElementById('consulta-asunto-expediente').value;

    const response = await fetch(`/asuntos/${numero_expediente}`);
    const asunto = await response.json();

    const resultDiv = document.getElementById('consulta-asunto-result');
    if (response.ok) {
        resultDiv.innerHTML = `<p>Cliente: ${asunto.cliente.nombre} ${asunto.cliente.apellido}</p><p>Fecha Inicio: ${asunto.fecha_inicio}</p><p>Estado: ${asunto.estado}</p>`;
    } else {
        resultDiv.innerHTML = '<p>Asunto no encontrado</p>';
    }
});
