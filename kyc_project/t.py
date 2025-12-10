from validation_engine import generate_valid_aadhaar, generate_valid_pan, generate_valid_passport

aadhaar = generate_valid_aadhaar()
pan = generate_valid_pan()
passport = generate_valid_passport()

print("Aadhaar :", aadhaar)
print("PAN     :", pan)
print("Passport:", passport)
