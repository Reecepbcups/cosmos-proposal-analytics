import os, json

PROPOSAL = '82'

current_dir = os.path.dirname(os.path.abspath(__file__))
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



# avg_staking_balance & average bank balance (in uatom)

staking_sums = 0
bank_sums = 0
total_accounts = 0
for voter in votes_dict.keys():
    total_accounts += 1

    if voter in staking:
        staking_sums += staking[voter]
    if voter in bank:
        bank_sums += bank[voter]


bank_sums = bank_sums / 1_000_000 # in atom

print("AVERAGES FOR PROPOSAL", PROPOSAL)
print('total_accounts', total_accounts)
print('total staking_sums: atom', f"{staking_sums:,}")
print('total bank_sums', f"{bank_sums:,}")

print('avg_staking_amt', f"{staking_sums / total_accounts:,}")
print('average bank balance', f"{bank_sums / total_accounts:,}")
