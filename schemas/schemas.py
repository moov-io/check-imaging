from typing import Optional, List
from dataclasses import dataclass
from pydantic import BaseModel

@dataclass
class Amount(BaseModel):
    numeric: float
    written: str

@dataclass
class Party(BaseModel):
    name: str
    address: Optional[str] = None

@dataclass
class Bank(BaseModel):
    name: str
    code: Optional[str] = None

@dataclass
class Memo(BaseModel):
    text: Optional[str] = None
    notes: Optional[List[str]] = None

@dataclass
class MICR(BaseModel):
    routing_number: str
    account_number: str
    check_number: str

@dataclass
class Check(BaseModel):
    check_number: str
    date: str  # You could also use datetime
    amount: Amount
    payor: Party
    payee: Party
    bank: Bank
    memo: Optional[Memo]
    signature: Optional[str]
    micr: MICR
