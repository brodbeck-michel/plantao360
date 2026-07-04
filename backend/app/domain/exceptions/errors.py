class BusinessRuleError(Exception):
    def __init__(self, detail: str = "Regra de negócio violada"):
        self.detail = detail
        self.status_code = 400
        self.error_type = "business_rule_error"
        super().__init__(self.detail)


class NotFoundError(Exception):
    def __init__(self, detail: str = "Recurso não encontrado"):
        self.detail = detail
        self.status_code = 404
        self.error_type = "not_found_error"
        super().__init__(self.detail)


class ConflictError(Exception):
    def __init__(self, detail: str = "Conflito de dados"):
        self.detail = detail
        self.status_code = 409
        self.error_type = "conflict_error"
        super().__init__(self.detail)


class UnauthorizedError(Exception):
    def __init__(self, detail: str = "Não autorizado"):
        self.detail = detail
        self.status_code = 401
        self.error_type = "unauthorized_error"
        super().__init__(self.detail)
