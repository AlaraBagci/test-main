# Separate logic file to satisfy TDD and Separation of Concerns
def calculate_risk(avg_stress, avg_sleep):
    """
    Determines if a student is at risk based on scenario thresholds.
    High Stress > 4.0 OR Sleep < 5.0 hours.
    """
    if avg_stress >= 4.0:
        return {"status": "Critical", "reason": "High Stress"}
    elif avg_sleep < 5.0:
        return {"status": "Warning", "reason": "Low Sleep"}
    else:
        return {"status": "Good", "reason": "Stable"}