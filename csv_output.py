'''
Morbid curiousity
But is there a way to query vote data over time on the three most recent Cosmos Hub proposals?
Into an excel sheet?
Like which wallets voted on a prop, in order with their staked wallet size?
'''

import os, json


PROPOSAL = '83'
current_dir = os.path.dirname(os.path.realpath(__file__))
csv_dir = os.path.join(current_dir, 'csv')
if not os.path.exists(csv_dir):
    os.makedirs(csv_dir)
os.chdir(current_dir)


# open balances.json, read all values of uatom into a dict
bank = {} # addr: uatom_amt
balances = json.load(open('bank.json'))
for balance in balances.get('balances'):
    '''
    {
      "address": "cosmos1qqqpu6cr8965q9edhpp2t4n3j22vghnzgw62f9",
      "coins": [
        {
          "amount": "9858013",
          "denom": "uatom"
        }
      ]
    },
    '''
    addr = balance.get('address')
    uatom_amt = 0
    for coin in balance.get('coins'):
        if coin.get('denom') == 'uatom':
            uatom_amt = int(coin.get('amount'))
    bank[addr] = uatom_amt
    # break
# print(bank)


staking = {}
delegations = json.load(open('staking.json'))
for delegate in delegations.get('delegations'):
    '''
    {
      "delegator_address": "cosmos1qqqzhvucv6375szzc5mh7n0290fd4j38pv6yaj",
      "shares": "2800.280017113851621861",
      "validator_address": "cosmosvaloper1et77usu8q2hargvyusl4qzryev8x8t9wwqkxfs"
    },
    '''
    # shares = 0.002800
    # 2800.280017113851621861 / 1_000_000 = 0.002800280017113851621861

    addr = delegate.get('delegator_address')
    uatom = int(float(delegate.get('shares'))) / 1_000_000

    if addr not in staking:
        staking[addr] = 0

    staking[addr] += uatom    
    # break

# print(staking)

# open gov.json, read every vote into a dict.
votes = json.load(open('gov.json', 'r'))
# print(votes.keys()) # dict_keys(['deposit_params', 'deposits', 'proposals', 'starting_proposal_id', 'tally_params', 'votes', 'voting_params'])

votes_dict = {} # addr: option
for i, data in enumerate(votes.get('votes')):
    '''
    list of:
    {'option': 'VOTE_OPTION_YES', 'options': [{'option': 'VOTE_OPTION_YES', 'weight': '1.000000000000000000'}], 'proposal_id': '79', 'voter': 'cosmos1qqq22fsralalyq92xl29xv9xxqvtyc2f2r62xe'}
    '''
    if data.get('proposal_id') != PROPOSAL: continue

    vote_option = data.get('option')    
    addr = data.get('voter')

    # print(i, data) 
    votes_dict[addr] = vote_option

    
bank_csv_output = {}
stake_csv_output = {}
for addr, vote_option in votes_dict.items():
    myBank = bank.get(addr, 0) / 1_000_000
    myStake = staking.get(addr, 0) # already in uatom form

    # csv_output.append(f'{addr},{vote_option},{myBank},{myStake}')
    bank_csv_output[addr] = f'{vote_option},{myBank}'
    stake_csv_output[addr] = f'{vote_option},{myStake}'

# save bank to a .csv sorted by mybank
b_file = os.path.join(csv_dir, f'bank_{PROPOSAL}.csv')
with open(b_file, 'w') as f:
    f.write('addr,vote_option,myBank\n')
    for addr, data in sorted(bank_csv_output.items(), key=lambda x: float(x[1].split(',')[1]), reverse=True):
        f.write(f'{addr},{data}\n')

s_file = os.path.join(csv_dir, f'stake_{PROPOSAL}.csv')
with open(s_file, 'w') as f:
    f.write('addr,vote_option,myStake\n')
    for addr, data in sorted(stake_csv_output.items(), key=lambda x: float(x[1].split(',')[1]), reverse=True):
        f.write(f'{addr},{data}\n')
