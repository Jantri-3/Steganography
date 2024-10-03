from mpmath import mp

def n_of_pi_decimals(n):
    n = int(n)

    # Set the number of decimal places
    mp.dps = n + 1

    # Store Pi with the set precision
    pi_value = str(mp.pi)

    # Write Pi to a text file
    with open("npi_decimals.txt", "w") as f:
        f.write(pi_value)