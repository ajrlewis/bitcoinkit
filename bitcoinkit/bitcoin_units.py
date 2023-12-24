SATOSHIS_PER_BITCOIN = 100_000_000


def bitcoins_to_satoshis(bitcoins):
    return int(bitcoins * SATOSHIS_PER_BITCOIN)


def satoshis_to_bitcoins(satoshis):
    return satoshis / SATOSHIS_PER_BITCOIN


def main():
    bitcoins = 0.5
    satoshis = bitcoins_to_satoshis(bitcoins)
    print(f"{bitcoins} bitcoins is equal to {satoshis:,} satoshis")

    satoshis = 50_000_000
    bitcoins = satoshis_to_bitcoins(satoshis)
    print(f"{satoshis:,} satoshis is equal to {bitcoins} bitcoins")


if __name__ == "__main__":
    main()
