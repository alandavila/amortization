#!/usr/bin/env python

import numpy as np

class LowPaymentError(ValueError):
    pass

class Mortgage():

    def __init__(self, principal, anual_rate, monthtly_payment):
        '''
        Input:
        -------
            principal: float. Initial principal/quantity of mortgage
        
            anual_rate: float. Mortgage anual rate
        
            monthtly_payment: float. Amount to be paid per month
        
        Output:
        -------
            morgage class instance that calculates each month's contribution
            to principal and interest accesible via the monthly_int_part and
            monthly_prin_part methods
        '''
        self.anual_rate = anual_rate
        self.payment = monthtly_payment
        self.monthly_rate = self.anual_rate/12
        self.interest_part = [] #list of part of payment used on interest
        self.principal_part = [] #list of part of payment used on principal
        #Calculate interest and principal part over the life of mortgage
        cur_principal = principal
        while cur_principal >= self.payment:
            cur_interest_part = cur_principal*self.monthly_rate
            # monthly payment should be higher than monthly interest
            if (cur_interest_part > self.payment):
                raise LowPaymentError('Select a higher payment or lower rate')
            self.principal_part.append(self.payment - cur_interest_part)
            self.interest_part.append(cur_interest_part)
            cur_principal = cur_principal + cur_interest_part - self.payment
        #final payment to pay off debt
        if cur_principal > 0.0:
            cur_interest_part = cur_principal*self.monthly_rate
            self.principal_part.append(cur_principal)
            self.interest_part.append(cur_interest_part)
            
            
        self.principal_part = np.array(self.principal_part)
        self.interest_part = np.array(self.interest_part)
        
    @classmethod
    def calculatePayment(cls, principal, anual_rate, num_payments):
        '''
        Input:
        -------
            principal: float. Initial principal/quantity of mortgage
        
            anual_rate: float. Mortgage anual rate
        
            num_paymenst: int. Life of the loan in months
        
        Output:
        -------
            morgage class instance that calculates each month's contribution
            to principal and interest accesible via the monthly_int_part and
            monthly_prin_part methods
        '''
        interest = anual_rate/12
        principal = principal
        num_payments = num_payments
        mo_payment = interest*(principal*np.power(1 + \
        interest, num_payments)) / (np.power(1 + interest, num_payments) - 1)
        return cls(principal, anual_rate, mo_payment)        
        
    def monthly_int_part(self):
        '''        
        Returns a numpy array with monthly contribution to interest
        '''
        return self.interest_part
        
    def monthly_prin_part(self):
        '''        
        Returns a numpy array with monthly contribution to principal
        '''        
        return self.principal_part
        
    def total_int(self):
        '''        
        Returns a total interest paid over the life of the loan
        '''
        return self.interest_part.sum(0)

    def total_princ(self):
        '''        
        Returns a total principal paid over the life of the loan
        '''
        return self.principal_part.sum(0)

    def total(self):
        '''        
        Returns a total  paid over the life of the loan
        '''
        return self.principal_part.sum(0) + self.interest_part.sum(0)        
        