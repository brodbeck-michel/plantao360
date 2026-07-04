openapi_tags = [
    {"name": "Health", "description": "Health check endpoints"},
    {
        "name": "Doctors",
        "description": "Gerenciamento de médicos — CRUD completo com paginação, filtros e ordenação.",
    },
    {"name": "Periods", "description": "Period management"},
    {"name": "Shifts", "description": "Shift management"},
]

standard_responses = {
    200: {
        "description": "Operação realizada com sucesso",
        "content": {
            "application/json": {
                "example": {
                    "success": True,
                    "data": {},
                    "meta": {},
                    "errors": [],
                }
            }
        },
    },
    201: {
        "description": "Recurso criado com sucesso",
        "content": {
            "application/json": {
                "example": {
                    "success": True,
                    "data": {"id": 1, "name": "Dr. João", "crm": "12345", "hour_rate": 150.0, "active": True},
                    "meta": {},
                    "errors": [],
                }
            }
        },
    },
    400: {
        "description": "Regra de negócio violada",
        "content": {
            "application/json": {
                "example": {
                    "success": False,
                    "error": {
                        "code": "INVALID_CRM",
                        "message": "CRM inválido (formato: apenas dígitos, 4-10 caracteres)",
                        "details": None,
                    },
                }
            }
        },
    },
    404: {
        "description": "Recurso não encontrado",
        "content": {
            "application/json": {
                "example": {
                    "success": False,
                    "error": {
                        "code": "DOCTOR_NOT_FOUND",
                        "message": "Médico não encontrado",
                        "details": None,
                    },
                }
            }
        },
    },
    409: {
        "description": "Conflito — recurso já existe",
        "content": {
            "application/json": {
                "example": {
                    "success": False,
                    "error": {
                        "code": "DOCTOR_ALREADY_EXISTS",
                        "message": "CRM 12345 já cadastrado",
                        "details": None,
                    },
                }
            }
        },
    },
    422: {
        "description": "Erro de validação (unprocessable entity)",
        "content": {
            "application/json": {
                "example": {
                    "success": False,
                    "errors": ["Nome é obrigatório", "CRM é obrigatório"],
                }
            }
        },
    },
    500: {
        "description": "Erro interno do servidor",
        "content": {
            "application/json": {
                "example": {
                    "success": False,
                    "error": {
                        "code": "INTERNAL_SERVER_ERROR",
                        "message": "Erro interno do servidor",
                        "details": None,
                    },
                }
            }
        },
    },
}

standard_errors = {
    "BusinessRuleError": {
        "value": {
            "status": 400,
            "detail": "Business rule violated",
            "type": "business_rule_error",
        }
    },
    "NotFoundError": {
        "value": {
            "status": 404,
            "detail": "Resource not found",
            "type": "not_found_error",
        }
    },
}
