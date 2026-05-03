# Scopes por rol según la guía del Taller 3

SCOPES_BY_ROLE = {
    "solicitante": {
        "tickets:crear",
        "tickets:ver_propios",
    },
    "responsable_tecnico": {
        "tickets:ver_propios",
        "tickets:recibir",
        "tickets:asignar",
        "tickets:finalizar",
    },
    "auxiliar": {
        "tickets:ver_propios",
        "tickets:atender",
    },
    "tecnico_especializado": {
        "tickets:ver_propios",
        "tickets:atender",
    },
    "admin": {
        "tickets:crear",
        "tickets:ver_propios",
        "tickets:ver_todos",
        "tickets:recibir",
        "tickets:asignar",
        "tickets:atender",
        "tickets:finalizar",
        "usuarios:gestionar",
    },
}


def get_scopes_for_role(role: str) -> set[str]:
    """Retorna los scopes asignados a un rol específico."""
    return SCOPES_BY_ROLE.get(role, set())
