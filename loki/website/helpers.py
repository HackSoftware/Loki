def get_label(application_opened, is_free):
    if is_free:
        if application_opened:
            return "Кандидатствай"
        return "Кандидатстването е затворетно"
    else:
        if application_opened:
            return "Запиши се"
        return "Записването е затворено"
