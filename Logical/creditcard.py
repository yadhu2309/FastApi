def card_valid(card_no):

    card_no_str = str(card_no)

    if len(card_no_str) < 13 or len(card_no_str) >16:
        return False
    
    if  not (card_no_str.startswith('4') or  card_no_str.startswith('5') or card_no_str.startswith('37') or card_no_str.startswith('6')):
        return False
    
    card_no_list = [int(digit) for digit in card_no_str]

    doubled_card_no = [card_no_list[i] * 2  if i % 2 == 0 else card_no_list[i] for i in range(len(card_no_list))]
    # non_doubled_card_no = []

    total = sum(i if i%10 == i else sum(divmod(i,10)) for i in doubled_card_no)

    if total % 10 == 0: 
        return True
    else:
        return False
    
    

   
if card_valid(4003600000000014):
    print("credit card is valid")
else:
    print("not valid")