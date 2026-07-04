from app.domain.rules.business_rules import BusinessRuleCode

ERROR_MESSAGES: dict[BusinessRuleCode, str] = {
    BusinessRuleCode.RN_01_SHIFT_REQUIRES_DOCTOR: (
        "Todo plantão deve possuir ao menos um médico."
    ),
    BusinessRuleCode.RN_02_SPLIT_MUST_CLOSE_PERIOD: (
        "Divisão de plantão só pode ocorrer em período fechado."
    ),
    BusinessRuleCode.RN_03_NO_OVERLAPPING: (
        "Não é permitido sobreposição de plantões para o mesmo médico."
    ),
    BusinessRuleCode.RN_04_EXTRA_REQUIRES_JUSTIFICATION: (
        "Plantão extra requer justificativa."
    ),
    BusinessRuleCode.RN_05_CLOSED_PERIOD_IMMUTABLE: (
        "Período fechado não pode ser alterado."
    ),
    BusinessRuleCode.RN_06_DOCTOR_SOFT_DELETE: (
        "Médico com plantões vinculados não pode ser removido permanentemente."
    ),
}
