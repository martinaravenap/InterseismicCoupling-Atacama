import numpy as np

def get_rigidity_profile(depths):
    """
    Calcula el módulo de rigidez (mu) en Pascales basado en la profundidad.
    Referencia: Adaptado para la zona de Atacama (-25° a -30°).
    """
    z = np.abs(depths)
    mu = np.zeros_like(z, dtype=float)
    
    # Perfil refinado para evitar sobreestimación en zona somera
    mu[z < 15] = 25e9   # Corteza superior / Sedimentos consolidados
    mu[(z >= 15) & (z < 40)] = 40e9  # Zona sismogénica principal
    mu[z >= 40] = 60e9  # Manto superior / Reología dúctil
    
    return mu