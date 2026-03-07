from damageanalysis import crop_damage_analysis
from lossestimation import crop_loss_estimation

# Image path
image_path = r"C:\Users\moham\Downloads\OIP (2).jpeg"

# Step 1: Get damage percentage
damage = crop_damage_analysis(image_path)

# Step 2: Estimate loss from damage
loss = crop_loss_estimation(damage)

# Output
print("Crop Damage (%) :", damage)
print("Crop Loss (%)   :", loss)

