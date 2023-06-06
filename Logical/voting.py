candidates = {'A':0, 'B':0,}

def voting(name):
    if name in candidates.keys():
        candidates[name] += 1
        return True
    else:
        return False
    
def winner():
    max_votes = max(candidates.values())
    winners_list = [key for key in candidates.keys() if candidates[key] == max_votes]
    print("winners")
    for winner in winners_list:
        print(winner,'\n')
        
voting('A')
voting('B')
voting('B')
voting('A')
voting('B')

winner()

