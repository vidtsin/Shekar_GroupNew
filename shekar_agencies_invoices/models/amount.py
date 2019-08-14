from odoo.exceptions import UserError
from odoo import api, fields, models, _

class AccountInvoice(models.Model):
    _inherit = "account.invoice"
    amount_total_words_2 = fields.Char('amount_in_words',store=True)
    tal1 = fields.Float('tal1',stroe = True)
    strom1 = fields.Char('strom1',store = True,compute = '_geat')
    
    @api.one
    @api.depends('rounded_total','tal1','strom1')
    def _geat(self):
    	cate = str(self.rounded_total)
    	self.amount_total_number_2 = str(cate)
    	self.rounded_total = round(self.rounded_total)
    	self.tal1 = round(self.rounded_total)
    	numbe = str(self.tal1).split('.')
    	money_number = numbe[0]
    	if money_number == 0:
    		return None
    	positions = [None for i in range(4)]
    	key_range = 0
    	one_place = ["","One ", "Two ", "Three ", "Four ","Five ", "Six ", "Seven ", "Eight ", "Nine"]
    	one_ten_place = ["Ten ", "Eleven ", "Twelve ", "Thirteen ", "Fourteen ","Fifteen ", "Sixteen ","Seventeen ", "Eighteen ","Nineteen "]
    	ten_place = ["Twenty ", "Thirty ", "Forty ", "Fifty ","Sixty ", "Seventy ", "Eighty ", "Ninety "]
    	name_of_number = ["Thousand","Lakh","Crore"]
    	money_number_money_text = ''
    	positions[0] = (int)(money_number) % 1000  # unit
    	positions[1] = (int)(money_number)// 1000
    	positions[2] = int(money_number) // 100000
    	positions[1] = int(positions[1]-100*positions[2]) #thasounds
    	positions[3] = int(money_number)//10000000 #crore
    	positions[2] = int(positions[2]-100*positions[3]) #lakh
    	for counter in range(3, 0, -1):
    		if positions[counter] != 0:
    			key_range = counter
    			break
    	for i in range(key_range, -1, -1):
    		if positions[i] == 0:
    			continue
    		ones = positions[i]%10 #ones
    		tens = int(positions[i])//10
    		hundreds = positions[i]//100#hundred
    		tens = tens - 10*hundreds #ten
    		if (hundreds > 0):
    			money_number_money_text += " "+one_place[int(hundreds)]+" "+"Hundred "
    		if (ones > 0 or tens > 0) :
    			if(hundreds > 0 and i == 0):
    				money_number_money_text += " and "
    			if (tens == 0):
    				money_number_money_text += " "+one_place[int(ones)]+" "
    			elif (tens == 1):
    				money_number_money_text += " "+one_ten_place[int(ones)]+" "
    			else:
    				money_number_money_text += " "+ten_place[int(tens -2)] + one_place[int(ones)]+" "
    			if (i != 0):
    				money_number_money_text += " "+name_of_number[int(i - 1)]+" "
    		money_number_money_text = money_number_money_text 
    		self.strom1 = str(money_number_money_text)+" "+"Rupees Only"
