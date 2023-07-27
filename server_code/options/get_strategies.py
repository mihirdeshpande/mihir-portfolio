import requests
import time

from bs4 import BeautifulSoup


def get_strategies(budget):
  time.sleep(10);
  return [{'name': 'The Wheel', 'symbol': 'AMC', 'price': 5.49, 'min_investment': 500, 'details': "fgsfjkfsf kjbjkvbs  ghsldk aghfld fn kdlsnfg nld gndf ksn sdgkd fklndg vdf nklnvk ldsnl  angl dk zngkfkn l and lkgn dfkln fg nfkla dsnd kl nf aslnfkdlf asn fkj sdnkfn ange riuerhg ie ahgk bnk fsji oe angk sernk gns dkl  gha kldhg ghse rln egkl aeh rlg esln glk"}, 
          {'name': 'Put Credit Spread', 'symbol': 'AAPL', 'price': 194.27, 'min_investment': 100}, 
          {'name': 'Iron Condor', 'symbol': 'SPY', 'price': 456, 'min_investment': 200}]
  