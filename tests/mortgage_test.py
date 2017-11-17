# -*- coding: utf-8 -*-
"""
Created on Sun Nov 12 18:17:06 2017

@author: alan
"""
#add mortgage package to sys.path
import context 
#import morgage.py module form mortgage package
from mortgage import mortgage
import numpy as np
import unittest

class GoodInput(unittest.TestCase):
    
    known_input = ( (100000, 0.05, 1500, 117396.57),
                    (100000, 0.00, 1500, 100000),
                    (123456, 0.00, 333, 123456),
                    (200000, 0.05, 1500, 292542.74)
                  )
    
    def test_known_totals(self):
        '''mortgage should calculate correct totals '''
        
        for prin, rate, monthly_pay, total in self.known_input:
            mort_instance = mortgage.Mortgage(prin, rate, monthly_pay)
            self.assertEqual(total,mort_instance.total().round(2))
            
    def test_total_is_principal_plus_interest(self):
        '''total mortgage paid has to equal total interest paid
        plus totat princiapl paid'''
        for prin, rate, monthly_pay, total in self.known_input:
            mort_instance = mortgage.Mortgage(prin, rate, monthly_pay)
            total = mort_instance.total()
            total_int = mort_instance.total_int()
            total_princ = mort_instance.total_princ()
            self.assertEqual(total,(total_int + total_princ))
        
class BadInputCannotPay(unittest.TestCase):
    
    def test_too_low_payment(self):
        '''Mortgage should fail if planned monthly payment is too low
        to actually ever pay the mortgage'''
        self.assertRaises(mortgage.LowPaymentError,\
                          mortgage.Mortgage, 100000, 0.05, 400)
        
    def test_too_high_rate(self):
        '''Mortgage should fail if rate is too high for the planned monthly
        payment
        '''
        self.assertRaises(mortgage.LowPaymentError,\
                          mortgage.Mortgage, 100000, 0.2,1500)
                          
class CalcPaymentKnownValues(unittest.TestCase):
    
    known_input = ((100000, 0.05, 360, 536.82),
                   (100000, 0.05, 180, 790.79)
                  )
    def test_payment_class(self):
        '''
        creating and instance with calculatePayment should get the 
        right monthly payment
        '''
        for prin, rate, num_payments, true_monthly in self.known_input:
            mort_instance =\
            mortgage.Mortgage.calculatePayment(prin, rate, num_payments)
            self.assertEqual(true_monthly, mort_instance.payment.round(2))        
        
class CalclPaymentsClass(unittest.TestCase):
    
    def test_calcpayments_class(self):
        '''
        creating a mortgage instance giving number of payments or giving
        monthly payment corresponting to that number of payment should 
        generate identical instances
        '''
        for loan in range(100000,500000,50000):
            for rate in np.arange(0.025, 0.06, 0.05):
                for length in [360, 180]:
                    mortgage_by_length = \
                    mortgage.Mortgage.calculatePayment(loan,rate,length)
                    mortgage_by_amount = \
                    mortgage.Mortgage(loan,rate, mortgage_by_length.payment)
                    calculated_length = \
                    len(mortgage_by_amount.monthly_int_part())
                    self.assertEqual(length, calculated_length)

class TestPrincipalMethod(unittest.TestCase):
    
    def test_total_princ(self):
        '''
        The total principal paid over the life of the loan should match
        the initial loan amount
        '''
        for loan in np.arange(100000.0, 500000, 50000.25):
            mortgage_by_length = \
            mortgage.Mortgage.calculatePayment(loan,0.05,360)
            mortgage_by_amount = \
            mortgage.Mortgage(loan,0.05, mortgage_by_length.payment)
            self.assertEqual(loan, mortgage_by_amount.total_princ().round(2))
            self.assertEqual(loan, mortgage_by_length.total_princ().round(2))           

if __name__ == '__main__':
    unittest.main()
