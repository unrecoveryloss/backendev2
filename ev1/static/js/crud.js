// Funciones JavaScript para operaciones CRUD
document.addEventListener('DOMContentLoaded', function () {
    // Inicializar tooltips de Bootstrap
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});

// Función para mostrar mensajes de éxito/error
function showMessage(message, type = 'success') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    alertDiv.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;

    document.body.appendChild(alertDiv);

    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.parentNode.removeChild(alertDiv);
        }
    }, 5000);
}

// Función para limpiar formularios
function clearForm(formId = 'usuarioForm') {
    const form = document.getElementById(formId);
    if (form) {
        form.reset();
        // Limpiar clases de validación
        const inputs = form.querySelectorAll('.is-invalid');
        inputs.forEach(input => input.classList.remove('is-invalid'));
    }
}

// Función para aplicar filtros de búsqueda
function applyFilters() {
    const searchInput = document.getElementById('searchInput');
    const filterSelect = document.getElementById('filterSelect');

    if (!searchInput) return;

    const search = searchInput.value;
    const filter = filterSelect ? filterSelect.value : '';

    const params = new URLSearchParams();
    if (search) params.append('search', search);
    if (filter) params.append('filter', filter);

    // Obtener la URL actual sin parámetros
    const currentUrl = window.location.pathname;
    window.location.href = currentUrl + '?' + params.toString();
}

// Función para exportar a Excel (placeholder)
function exportToExcel() {
    showMessage('Función de exportación a Excel en desarrollo', 'info');
}

// Funciones específicas para usuarios
function editUsuario(id) {
    window.location.href = `/accounts/crud/usuarios/edit/${id}/`;
}

function deleteUsuario(id) {
    showDeleteModal('usuario', id, '¿Está seguro de que desea eliminar este usuario?');
}

// Funciones específicas para categorías
function editCategoria(id) {
    window.location.href = `/accounts/crud/categorias/edit/${id}/`;
}

function deleteCategoria(id) {
    showDeleteModal('categoria', id, '¿Está seguro de que desea eliminar esta categoría?');
}

// Funciones específicas para productos
function editProducto(id) {
    window.location.href = `/accounts/crud/productos/edit/${id}/`;
}

function deleteProducto(id) {
    showDeleteModal('producto', id, '¿Está seguro de que desea eliminar este producto?');
}

// Funciones específicas para proveedores
function editProveedor(id) {
    window.location.href = `/accounts/crud/proveedores/edit/${id}/`;
}

function deleteProveedor(id) {
    showDeleteModal('proveedor', id, '¿Está seguro de que desea eliminar este proveedor?');
}

// Funciones específicas para clientes
function editCliente(id) {
    window.location.href = `/accounts/crud/clientes/edit/${id}/`;
}

function deleteCliente(id) {
    showDeleteModal('cliente', id, '¿Está seguro de que desea eliminar este cliente?');
}

// Función genérica para mostrar modal de confirmación de eliminación
function showDeleteModal(type, id, message) {
    const modal = document.getElementById('deleteModal');
    const modalBody = modal.querySelector('.modal-body');
    const confirmBtn = document.getElementById('confirmDelete');

    if (!modal) {
        console.error('Modal de eliminación no encontrado');
        return;
    }

    modalBody.innerHTML = message;

    // Configurar el botón de confirmación
    confirmBtn.onclick = function () {
        performDelete(type, id);
        bootstrap.Modal.getInstance(modal).hide();
    };

    // Mostrar el modal
    const bsModal = new bootstrap.Modal(modal);
    bsModal.show();
}

// Función para realizar la eliminación
function performDelete(type, id) {
    const deleteUrl = `/accounts/crud/${type}s/delete/${id}/`;

    fetch(deleteUrl, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCSRFToken(),
            'Content-Type': 'application/json',
        },
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showMessage(data.message, 'success');
                // Recargar la página después de un breve delay
                setTimeout(() => {
                    location.reload();
                }, 1000);
            } else {
                showMessage(data.message || 'Error al eliminar el elemento', 'danger');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showMessage('Error de conexión. Intente nuevamente.', 'danger');
        });
}

// Función para obtener el token CSRF
function getCSRFToken() {
    const token = document.querySelector('[name=csrfmiddlewaretoken]');
    return token ? token.value : '';
}

// Función para validar formularios
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return false;

    const requiredFields = form.querySelectorAll('[required]');
    let isValid = true;

    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            field.classList.add('is-invalid');
            isValid = false;
        } else {
            field.classList.remove('is-invalid');
        }
    });

    return isValid;
}

// Función para enviar formularios con AJAX
function submitForm(formId, successCallback) {
    const form = document.getElementById(formId);
    if (!form) return;

    if (!validateForm(formId)) {
        showMessage('Por favor, complete todos los campos requeridos', 'warning');
        return;
    }

    const formData = new FormData(form);
    const action = form.action;

    fetch(action, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': getCSRFToken(),
        },
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showMessage(data.message, 'success');
                if (successCallback) successCallback();
                clearForm(formId);
            } else {
                showMessage(data.message || 'Error al procesar la solicitud', 'danger');
                // Mostrar errores de validación
                if (data.errors) {
                    Object.keys(data.errors).forEach(field => {
                        const input = form.querySelector(`[name="${field}"]`);
                        if (input) {
                            input.classList.add('is-invalid');
                            const feedback = input.nextElementSibling || document.createElement('div');
                            feedback.className = 'invalid-feedback';
                            feedback.textContent = data.errors[field][0];
                            if (!input.nextElementSibling) {
                                input.parentNode.appendChild(feedback);
                            }
                        }
                    });
                }
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showMessage('Error de conexión. Intente nuevamente.', 'danger');
        });
}

// Event listeners para formularios
document.addEventListener('DOMContentLoaded', function () {
    // Interceptar envío de formularios SOLO si no tienen su propia validación
    const forms = document.querySelectorAll('form[id$="Form"]');
    forms.forEach(form => {
        // Verificar si el formulario ya tiene su propio event listener
        const hasCustomValidation = form.hasAttribute('data-custom-validation');

        if (!hasCustomValidation) {
            form.addEventListener('submit', function (e) {
                e.preventDefault();
                submitForm(form.id, function () {
                    // Recargar la página después de crear/editar exitosamente
                    setTimeout(() => {
                        location.reload();
                    }, 1000);
                });
            });
        }
    });

    // Limpiar validación al escribir en campos
    const inputs = document.querySelectorAll('input, select, textarea');
    inputs.forEach(input => {
        input.addEventListener('input', function () {
            this.classList.remove('is-invalid');
        });
    });
});
