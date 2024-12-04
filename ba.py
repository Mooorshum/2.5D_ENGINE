for i in range(64):  # 64 combinations
    bits = f"{i:06b}"  # Convert to 6-bit binary
    conditions = " && ".join([f"V(OA_{j}) == {bit}" for j, bit in enumerate(bits)])
    print(f"// {bits}")
    print(f"if ({conditions}) begin")
    print(f"    V_delta = 0;")
    print("end")










    