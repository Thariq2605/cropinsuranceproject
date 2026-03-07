def crop_loss_estimation(damage_percentage):
    """
    Estimate crop yield loss based on visible damage percentage.
    Assumption: Visible crop damage is proportional to yield loss.
    """

    # Safety check
    if damage_percentage < 0:
        damage_percentage = 0
    if damage_percentage > 100:
        damage_percentage = 100

    # Simple proportional estimation
    loss_percentage = damage_percentage

    return float(round(loss_percentage, 2))
