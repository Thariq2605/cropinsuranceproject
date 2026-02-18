from fraud_system.pipeline import run_pipeline

image_path = r"C:\Users\moham\Downloads\OIP (2).jpeg"

result = run_pipeline(image_path)

print("FINAL RESULT")
print("----------------")
for key, value in result.items():
    print(f"{key} : {value}")
