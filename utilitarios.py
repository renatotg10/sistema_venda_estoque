def br_to_float(valor_br):
    """Converte um valor em formato decimal brasileiro (por exemplo, '7,50') para float (por exemplo, 7.5)."""
    return float(valor_br.replace(',', '.'))

def float_to_br(valor_float):
    """Converte um valor float (por exemplo, 7.5) para formato decimal brasileiro (por exemplo, '7,50')."""
    return f"{valor_float:.2f}".replace('.', ',')
