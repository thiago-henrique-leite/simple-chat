class DiffieHelman:
  def get_public(private_key): return pow(3, private_key, 353)

  def get_key(public_key, private_key): return pow(public_key, private_key, 353)
