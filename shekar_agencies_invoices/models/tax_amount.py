from odoo.exceptions import UserError
from odoo import api, fields, models, _

class SaleOrder(models.Model):
    _inherit = "account.invoice"

    amount_in_words = fields.Char(compute='_calc_amt_in_words')
    z_e_way_bill=fields.Char('E Way Bill',store=True)
    z_number_of_items=fields.Integer("Number of items")

    @api.depends('amount_in_words','amount_total','pricelist_id')
    def _calc_amt_in_words(self):
        for line in self:
            ones = ['zero','One','Two','Three','Four','Five','Six','Seven','Eight','Nine']
            tens = ['zero','Ten','Twenty','Thirty','Fourty','Fifty','Sixty','Seventy','Eighty','Ninety']
            teens = ['Ten','Eleven','Twelve','Thirteen','Fourteen','Fifteen','Sixteen','Seventeen','Eighteen','Ninteen']
            place_values_IND = ['','','Hundred ','Thousand ','','Lakh ','','Crore ','']
            place_values_INTL = ['','','Hundred ','Thousand ','','Hundred ','Million ','','Hundred ','Billion ']

            cur_major = ''
            cur_minor = ''
            
            if line.pricelist_id.currency_id.name == 'USD':
                cur_major = 'US Dollars'
                cur_minor = 'Cents'
            if line.pricelist_id.currency_id.name == 'INR':
                cur_major = 'Rupees'
                cur_minor = 'Paise'
            if line.pricelist_id.currency_id.name == 'AUD':
                cur_major = 'AU Dollars'
                cur_minor = 'Cents'
            if line.pricelist_id.currency_id.name == 'EURO':
                cur_major = 'Euros'
                cur_minor = 'Cents'
            if line.pricelist_id.currency_id.name == 'GBP':
                cur_major = 'Sterling Pounds'
                cur_minor = 'Pence'

            def num_to_wrd_IND(number):
                words=''
                for d in number:
                    d = int(d)
                    words += ones[d]+' '

                words = words.split(' ')
                words.pop()

                for t in range(len(number)-5,-1,-2):
                    words[t] = tens[int(number[t])]
                    if number[t] == '1':
                        words[t] = teens[int(number[t+1])]
                        words[t+1] = ''

                words[len(number)-2] = tens[int(number[len(number)-2])]
                if number[len(number)-2] == '1':
                    words[len(number)-2] = teens[int(number[len(number)-1])]
                    words[len(number)-1] = ''

                words = words[::-1]
                for pl in range(len(words)):
                    if words[pl] == 'zero':
                        words[pl] = ''
                    elif words[pl] == '':
                        words[pl] += place_values_IND[pl]
                    else:
                        words[pl] += ' '+place_values_IND[pl]
                    # if 'Hundred ' in words[pl]:
                    #     if words[pl-1] != '':
                    #         words[pl] += 'and '
                    if words[pl][:-1] in tens and words[pl-1] == '':
                        words[pl-1] += place_values_IND[pl-1]
                words = words[::-1]

                number=''
                for word in words:
                    number += word

                return number

            def num_to_wrd_INTL(number):
                words=''
                for d in number:
                    d = int(d)
                    words += ones[d]+' '

                words = words.split(' ')
                words.pop()

                for t in range(-2,-len(number)-1,-3):
                    words[t] = tens[int(number[t])]
                    if number[t] == '1':
                        words[t] = teens[int(number[t+1])]
                        words[t+1] = ''


                words = words[::-1]
                for pl in range(len(words)):
                    if words[pl] == 'zero':
                        words[pl] = ''
                    elif words[pl] == '':
                        words[pl] += place_values_INTL[pl]
                    else:
                        words[pl] += ' '+place_values_INTL[pl]
                    if 'Hundred ' in words[pl]:
                        if words[pl-1] != '':
                            words[pl] += 'and '
                        if words[pl-2] == '':
                            words[pl-2] = place_values_INTL[pl-2]
                    if words[pl][:-1] in tens and words[pl-1] == '':
                        words[pl-1] += place_values_INTL[pl-1]
                words = words[::-1]

                number=''
                for word in words:
                    number += word

                return number

            number = line.amount_total
            number = str(number)

            number = number.split('.')

            if len(number[1]) == 1:
                number[1] = number[1]+'0'

            number_whole = number_fract = ''

            if line.pricelist_id.currency_id.name == 'INR':
                number_whole = cur_major+" "+num_to_wrd_IND(number[0])
                if number[1] != '00':
                    number_whole += ' and '
                    number_fract = num_to_wrd_IND(number[1])+cur_minor
            else:
                number_whole = cur_major+" "+num_to_wrd_INTL(number[0])
                if number[1] != '00':
                    number_whole += ' and '
                    number_fract = num_to_wrd_INTL(number[1])+cur_minor

            line.amount_in_words = number_whole+number_fract+' Only'