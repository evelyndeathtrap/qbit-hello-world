import os
import cudaq
import math
import time
import threading

# Kernel takes a list of phase rotation angles in radians
@cudaq.kernel
def q(angles: list[float]):
    qubits = cudaq.qvector(1)
    
    # 1. Create superposition
    h(qubits[0])
    
    # 2. Apply accumulated phase transformations
    for angle in angles:
        rz(angle, qubits[0])


def qr():
    while True:
        try:
            # Read entropy from /dev/urandom inside host thread
            with open("/dev/urandom", "rb") as f:
                raw_bytes = f.read(16)
            
            # Convert 16 bytes into a list of 16 float angles in range [0, 2*pi)
            angles = [b for b in raw_bytes]
            
            # Sample kernel with valid parameters
            result = cudaq.sample(q, angles, shots_count=1)
            
            time.sleep(0.01)
        except Exception as e:
            print(f"Error in entropy thread: {e}")
            break

# Start background entropy thread
t = threading.Thread(target=qr, daemon=True)
t.start()

# Main thread handles interactive user input
while True:
    try:
        ln = input("")
        if not ln:
            continue
            
        # Convert input string characters into radians
        char_angles = [ord(c)for c in ln]
        
        # Sample kernel with character angles
        result = cudaq.sample(q, char_angles, shots_count=1)
        
    except (EOFError, KeyboardInterrupt):
        break
