from solana.keypair import Keypair as SolanaKeypair
from pybip39 import Mnemonic as MM, MnemonicType, Language
from typing import Union
from bip_utils import *
import base58, uuid

        

class Keypair(object):

    def __init__(self, keypair: SolanaKeypair) -> None:
        self._keypair = keypair
    
    def __repr__(self) -> str:
        return self.private_key
    
    @staticmethod
    def generate_mnemonic(strength: int = 128):
        if strength == 128:
            return MM().phrase
        elif strength == 256:
            return MM(MnemonicType.Words24).phrase
    
    @classmethod
    def from_mnemonic(cls, mnemonic_phrase: Union[str, MM]):
        return cls(SolanaKeypair.from_solders(SolanaKeypair.from_secret_key(Bip44.FromSeed(Bip39SeedGenerator(mnemonic_phrase, Bip39Languages.ENGLISH).Generate(""), Bip44Coins.SOLANA).Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).PrivateKey().Raw().ToBytes()).to_solders()))
    
    @classmethod
    def from_byte_array(cls, key: bytes):
        return cls(SolanaKeypair.from_secret_key(key))
    
    @classmethod
    def from_secret_key(cls, key: bytes):
        return cls(SolanaKeypair.from_secret_key(key))
    
    @classmethod
    def random(cls):
        return cls(Keypair())
    
    @classmethod
    def from_solders(cls, keypair: SolanaKeypair):
        return cls(SolanaKeypair.from_solders(keypair))
    
    @classmethod
    def from_base58(cls, seed: str):
        return cls(SolanaKeypair.from_secret_key(base58.b58decode(seed)))
    
    @property
    def to_solders(self):
        return self._keypair.to_solders()
    
    @property
    def to_keypair(self):
        return self._keypair
    
    @property
    def private_key(self):
        return base58.b58encode(self._keypair.secret_key).decode()
    
    @property
    def public_key(self):
        return self._keypair.public_key.to_base58().decode()
    
    @property
    def to_byte_array(self):
        return [LIST for LIST in self._keypair.secret_key]

